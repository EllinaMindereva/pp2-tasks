import pygame, sys
import random

pygame.init()

SIZE = 600
CELL = 30
SCORE = 0
LEVEL = 1
screen = pygame.display.set_mode((SIZE, SIZE)) #creating the display
screen.fill((0, 0, 0))
pygame.display.set_caption("Snake game") 
clock = pygame.time.Clock()
FPS = 5
clock.tick(FPS)
RANGE = (CELL // 2, SIZE - CELL // 2, CELL) #range for the random
get_random_pos = lambda: [random.randrange(*RANGE), random.randrange(*RANGE)] #getting the random position

snake = pygame.rect.Rect([0, 0, CELL - 2, CELL - 2])
snake.center = get_random_pos()
length = 1
segments = [snake.copy()]
snake_dir = (0, 0)
time, time_step = 0, 110    #time_step is the delay between snake steps in ms

food = snake.copy()
food.center = get_random_pos()

font = pygame.font.SysFont("comicsansms", 20)

while True: #creating the game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #event to quit the game
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: #events to push the buttons
            if event.key == pygame.K_UP:
                snake_dir = (0, - CELL)
            if event.key == pygame.K_DOWN:
                snake_dir = (0, CELL)
            if event.key == pygame.K_LEFT:
                snake_dir = (- CELL, 0)
            if event.key == pygame.K_RIGHT:
                snake_dir = (CELL, 0)

        screen.fill((0, 0, 0))
        
        eating_itself = pygame.Rect.collidelist(snake, segments[:-1]) != -1
        if snake.left < 0 or snake.right > SIZE or snake.top < 0 or snake.bottom > SIZE or eating_itself: #checking the borders and if the snake eats itself
            snake.center, food.center = get_random_pos(), get_random_pos()
            length, snake_dir = 1, (0, 0)
            segments = [snake.copy()]
            SCORE = 0
            LEVEL = 1

        if snake.center == food.center: #checking if snake eats the food
            food.center = get_random_pos()
            length += 1
            SCORE += 1
            if SCORE % 4 == 0:
                LEVEL += 1
                FPS += 1


        #adding the score and level
        score = font.render(f"Score: {str(SCORE)}", True, (255, 255, 255))
        screen.blit(score, (10, 10))
        level = font.render(f"Level: {str(LEVEL)}", True, (255, 128, 000))
        screen.blit(level, (10, 30))

        pygame.draw.rect(screen, (255, 255, 0), food) #drawing the food

        for segment in segments:
            pygame.draw.rect(screen, (0, 255, 255), segment) #drawing the snake
        #moving the snake
        time_now = pygame.time.get_ticks() 
        if time_now - time > time_step:
            time = time_now
            snake.move_ip(snake_dir)
            segments.append(snake.copy())
            segments = segments[-length:]

        pygame.display.flip()
        clock.tick(60)