import pygame, sys
from pygame.locals import *  
import random, time

pygame.init()
WIDTH = 400
HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0
N = 50 #the number needed to increase the speed

screen = pygame.display.set_mode((WIDTH, HEIGHT)) #creating the display
screen.fill((255, 255, 255))
pygame.display.set_caption("Racer game")

clock = pygame.time.Clock()
#creating the font settings
font = pygame.font.SysFont("comicsansms", 60)
small_font = pygame.font.SysFont("comicsansms", 20)
game_over = font.render("Game Over", True, (0, 0, 0))

background = pygame.image.load("AnimatedStreet.png")

pygame.mixer.music.load("background.wav") #background music on repeat
pygame.mixer.music.play(-1)

class Enemy(pygame.sprite.Sprite): #enemy car
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

class Player(pygame.sprite.Sprite): #player car
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

class Coin(pygame.sprite.Sprite): #coins
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("thecoin.png")
        self.rect = self.image.get_rect()
        self.weight = 1 
        self.spawn()
    
    def spawn(self):
        self.weight = random.randint(1, 5) #random weight between 1 and 5
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH - 40 ), 0)


    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > HEIGHT: #respawn coins when they are off the screen
            self.spawn()

player = Player()
enemy = Enemy()
coin = Coin()

enemies = pygame.sprite.Group()
enemies.add(enemy)
coin_group = pygame.sprite.Group()
coin_group.add(coin)
all_sprites = pygame.sprite.Group()
all_sprites.add(player, enemy, coin)
#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background, (0, 0))
    scores = small_font.render(f"Score: {str(SCORE)}", True, (0, 0, 0)) #counting the score
    screen.blit(scores, (10, 10))
    coins = small_font.render(f"Coins: {str(COINS)}", True, (0, 0, 0)) 
    screen.blit(coins, (10, 40))

    if pygame.sprite.spritecollideany(player, coin_group):
        COINS += coin.weight
        if COINS // N > (COINS - coin.weight) // N: #check the number of coins to increase the speed
            SPEED += 1
        coin.spawn()

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

    pygame.display.flip() #update the screen
    clock.tick(60)