import pygame as py
import random
import json
import os
from config import *

class Game:
    def __init__(self, username, pb):
        self.username = username #getting the info
        self.pb = pb
        self.settings = self.load_settings()

        self.score = 0
        self.level = 1
        self.game_over = False #initial state
   
        self.snake_dir = (0, 0) #creating snake
        self.snake_head = py.Rect(0, 0, CELL_SIZE - 2, CELL_SIZE - 2)
        self.snake_head.center = (SIZE // 2 + 20, SIZE // 2 + 20)
        self.segments = [self.snake_head.copy()]
        self.length = 1
 
        self.food = py.Rect(0, 0, CELL_SIZE - 2, CELL_SIZE - 2)
        self.poison = py.Rect(0, 0, CELL_SIZE - 2, CELL_SIZE - 2) #creating food, poison and powerup
        self.powerup = py.Rect(0, 0, CELL_SIZE - 2, CELL_SIZE - 2)
        
        self.obstacles = []
        self.food_weight = 1
        self.powerup_type = None
        #timers
        self.time_prev = 0
        self.current_step = INITIAL_SPEED
        self.food_spawn_time = py.time.get_ticks()
        self.pwr_spawn_time = py.time.get_ticks()
        self.pwr_active_until = 0
        #flags
        self.shield_active = False
        self.pwr_on_field = False
        
        self.spawn_food() #initial spawns
        self.spawn_poison()

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        return {"snake_color": COLOR_SNAKE_DEFAULT, "grid_overlay": True, "sound": True}

    def get_valid_pos(self): #finds a random position not occupied by obstacles or the snake
        range_data = get_grid_range()
        while True:
            pos = [random.randrange(*range_data), random.randrange(*range_data)]
            temp_rect = py.Rect(0, 0, CELL_SIZE - 2, CELL_SIZE - 2)
            temp_rect.center = pos
            #check collisions with obstacles or snake body
            if any(obs.colliderect(temp_rect) for obs in self.obstacles):
                continue
            if any(seg.colliderect(temp_rect) for seg in self.segments):
                continue
            return pos

    def spawn_food(self):
        self.food.center = self.get_valid_pos()
        self.food_weight = random.choices([1, 2, 3], weights=FOOD_WEIGHTS)[0]
        self.food_spawn_time = py.time.get_ticks()

    def spawn_poison(self):
        self.poison.center = self.get_valid_pos()

    def spawn_powerup(self):
        if not self.pwr_on_field:
            self.powerup.center = self.get_valid_pos()
            self.powerup_type = random.choice([PWR_SPEED, PWR_SLOW, PWR_SHIELD])
            self.pwr_spawn_time = py.time.get_ticks()
            self.pwr_on_field = True

    def handle_level_up(self):
        self.level += 1
        self.current_step = max(MIN_SPEED, INITIAL_SPEED - (self.level * SPEED_INCREMENT)) #increase base speed
        
        if self.level >= 3: #creating the obstacles at level 3 and more
            self.obstacles = []
            for _ in range(self.level + 2):
                new_obs = py.Rect(0, 0, CELL_SIZE - 2, CELL_SIZE - 2)
                new_obs.center = self.get_valid_pos()
                if not new_obs.colliderect(self.snake_head.inflate(CELL_SIZE*4, CELL_SIZE*4)):
                    self.obstacles.append(new_obs)

    def update(self):
        now = py.time.get_ticks()

        if self.pwr_on_field and now - self.pwr_spawn_time > POWERUP_TIMER: #powerup disappear with time
            self.pwr_on_field = False

        if self.pwr_active_until > 0 and now > self.pwr_active_until: #effects disappear with time
            self.pwr_active_until = 0
            #reset speed to current level speed
            self.current_step = max(MIN_SPEED, INITIAL_SPEED - (self.level * SPEED_INCREMENT))

        if now - self.food_spawn_time > FOOD_TIMER: #food disapper with time 
            self.spawn_food()

        if now - self.time_prev > self.current_step: #movement
            self.time_prev = now
            if self.snake_dir != (0, 0):
                self.snake_head.move_ip(self.snake_dir)
                self.segments.append(self.snake_head.copy())
                self.segments = self.segments[-self.length:]

        #collisions with obstacles or walls
        hit_wall = (self.snake_head.left < 0 or self.snake_head.right > SIZE or self.snake_head.top < 0 or self.snake_head.bottom > SIZE)
        hit_obs = any(self.snake_head.colliderect(obs) for obs in self.obstacles)
        hit_self = any(self.snake_head.colliderect(seg) for seg in self.segments[:-1])

        if hit_wall or hit_obs or hit_self:
            if self.shield_active:
                self.shield_active = False #saves 1 time
                #pushes back if hits the wall
                if hit_wall:
                    self.snake_head.move_ip([-d for d in self.snake_dir])
            else:
                self.game_over = True

        #collision with objects
        if self.snake_head.colliderect(self.food):
            self.score += self.food_weight
            self.length += self.food_weight
            if self.score // LEVEL_UP_THRESHOLD >= self.level:
                self.handle_level_up()
            self.spawn_food()
            if random.random() < 0.3: self.spawn_powerup() # 30% chance to spawn pwr

        if self.snake_head.colliderect(self.poison):
            self.length -= 2
            if self.length <= 1:
                self.game_over = True
            else:
                self.segments = self.segments[-self.length:]
                self.spawn_poison()

        if self.pwr_on_field and self.snake_head.colliderect(self.powerup):
            self.apply_powerup(self.powerup_type)
            self.pwr_on_field = False

    def apply_powerup(self, ptype):
        now = py.time.get_ticks()
        if ptype == PWR_SPEED:
            self.current_step = 60
            self.pwr_active_until = now + POWERUP_EFFECT_DURATION
        elif ptype == PWR_SLOW:
            self.current_step = 350
            self.pwr_active_until = now + POWERUP_EFFECT_DURATION
        elif ptype == PWR_SHIELD:
            self.shield_active = True

    def draw(self, screen, snake_color):
        #draw food with different colors depending on weight
        f_colors = {1: COLOR_FOOD_1, 2: COLOR_FOOD_2, 3: COLOR_FOOD_3}
        py.draw.rect(screen, f_colors.get(self.food_weight), self.food)
        #draw poison
        py.draw.rect(screen, COLOR_POISON, self.poison)
        #draw powerup
        if self.pwr_on_field:
            p_color = (255, 255, 255) #white for speed
            if self.powerup_type == PWR_SLOW: p_color = (150, 0, 255) #purple
            if self.powerup_type == PWR_SHIELD: p_color = (0, 255, 255) #cyan
            py.draw.ellipse(screen, p_color, self.powerup)

        #drawing obstacles
        for obs in self.obstacles:
            py.draw.rect(screen, COLOR_WALL, obs)

        #drawing snake
        for i, seg in enumerate(self.segments):
            color = snake_color
            if self.shield_active and i == len(self.segments) - 1:
                color = (0, 255, 255) # Head glows cyan if shield is up
            py.draw.rect(screen, color, seg)