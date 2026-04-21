import pygame, sys
from pygame.locals import *  
import random, time

pygame.init()
WIDTH = 400
HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT)) #creating the display
screen.fill((255, 255, 255))
pygame.display.set_caption("Racer game")

clock = pygame.time.Clock()
clock.tick(60)
#creating the font settings
font = pygame.font.SysFont("comicsansms", 60)
small_font = pygame.font.SysFont("comicsansms", 20)
game_over = font.render("Game Over", True, (0, 0, 0))

background = pygame.image.load("AnimatedStreet.png")

pygame.mixer.music.load("background.wav") #background music on repeat
pygame.mixer.music.play(-1)
#creating the class for a blue car for player
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.bottom > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, WIDTH - 40 ), 0)
#creating a red car for enemies
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < WIDTH:
            if keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

    def get_coordinates(self):
        return self.rect.top, self.rect.left

player = Player()
enemy = Enemy()

enemies = pygame.sprite.Group()
enemies.add(enemy)
all_sprites = pygame.sprite.Group()
all_sprites.add(player, enemy)

INC_SPEED = pygame.USEREVENT + 1 #increasing the speed as the score gets higher
pygame.time.set_timer(INC_SPEED, 1000)

coin = pygame.image.load("thecoin.png") #adding the coins that appear randomly
COINX, COINY = random.randint(40, WIDTH - 40), 0

while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background, (0, 0))
    scores = small_font.render(f"Score: {str(SCORE)}", True, (0, 0, 0)) #counting the score
    screen.blit(scores, (10, 10))
    coins = small_font.render(f"Coins: {str(COINS)}", True, (0, 0, 0)) #an attempt to count the coins
    screen.blit(coins, (10, 40))

    screen.blit(coin, (COINX, COINY))

    COINY += SPEED
    if COINY > HEIGHT:
        COINX, COINY = random.randint(40, WIDTH - 40), 0

    if COINY > 560:
        COINS += 1

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()
    
    if pygame.sprite.spritecollideany(player, enemies): #game over if player hits the enemy
        pygame.mixer.Sound("crash.wav").play()
        time.sleep(1)
        screen.fill((255, 0, 0))
        screen.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    clock.tick(60)