import pygame, sys
import random

pygame.init() #initialization of all modules

LIGHTBLUE = (224,255,255)
PALEBLUE = (175,238,238)
RED = (255, 0, 0)
DARKGREEN = (0,100,0) #colors
LIGHTGREEN = (50,205,50)
DARKGRAY = (47,79,79)

WIDTH = 600
HEIGHT = 600
CELL = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #creating the display
pygame.display.set_caption("Snake game") 

SCORE = 0
LEVEL = 1

clock = pygame.time.Clock()
FPS = 5 #to control the speed
font = pygame.font.SysFont("comicsansms", 20) #font

def draw_grid():
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, PALEBLUE, (i * CELL, j * CELL, CELL, CELL), 1) #creating the grid

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x}, {self.y}"

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

        if self.body[0].x > WIDTH // CELL - 1: #right border check
            self.body[0].x = 0
        if self.body[0].x < 0:
            self.body[0].x = WIDTH // CELL - 1 #left border check
        if self.body[0].y > HEIGHT // CELL - 1: #bottom border check
            self.body[0].y = 0
        if self.body[0].y < 0:
            self.body[0].y = HEIGHT // CELL - 1 #top border check

    def draw(self): #creating the snake
        head = self.body[0]
        pygame.draw.rect(screen, DARKGREEN, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, LIGHTGREEN, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food): #check if snake eats the food
        global SCORE
        global LEVEL
        global FPS
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            weight = food.generate_random_weight()
            for _ in range(weight):
                tail = self.body[-1]
                self.body.append(Point(tail.x, tail.y)) 
            food.generate_random_pos()
            food.generate_random_weight()
            SCORE += weight
            if SCORE // 10 >= LEVEL:
                LEVEL += 1
                FPS += 1

class Food: 
    def __init__(self):
        self.pos = Point(9, 9)
        self.weight = random.randint(1, 3)
        self.food_spawn_time = pygame.time.get_ticks()

    def draw(self):
        pygame.draw.rect(screen, RED, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL)) #drawing food

    def generate_random_pos(self):
        self.pos.x = random.randint(0, WIDTH // CELL - 1)
        self.pos.y = random.randint(0, HEIGHT // CELL - 1)

    def generate_random_weight(self):
        self.weight = random.randint(1, 3) #random weight for the food, it can be 1, 2 or 3
        return self.weight

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.food_spawn_time >= 7000: #spawn timer
            self.generate_random_pos()
            self.generate_random_weight()
            self.food_spawn_time = current_time

food = Food()
snake = Snake()
#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.dx = 1
                snake.dy = 0
            elif event.key == pygame.K_LEFT:
                snake.dx = -1
                snake.dy = 0
            elif event.key == pygame.K_DOWN:
                snake.dx = 0
                snake.dy = 1
            elif event.key == pygame.K_UP:
                snake.dx = 0
                snake.dy = -1

    screen.fill(LIGHTBLUE)

    draw_grid()
    pygame.draw.rect(screen, DARKGRAY, (0, 0, 110, 70))

    snake.move()
    snake.check_collision(food)
    food.update()

    snake.draw()
    food.draw()

    score = font.render(f"Score: {str(SCORE)}", True, (255, 255, 255)) #text for score and level
    screen.blit(score, (10, 10))
    level = font.render(f"Level: {str(LEVEL)}", True, (255, 128, 000))
    screen.blit(level, (10, 30))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()