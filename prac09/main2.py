import pygame
from ball import Ball

pygame.init()

w = 800
h = 600
screen = pygame.display.set_mode((w, h))

clock = pygame.time.Clock()

ball = Ball(x = w // 2, y = h // 2, radius = 25, step = 20, width = w, height = h)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ball.move_up()
            elif event.key == pygame.K_DOWN:
                ball.move_down()
            elif event.key == pygame.K_LEFT:
                ball.move_left()
            elif event.key == pygame.K_RIGHT:
                ball.move_right()

    screen.fill((255, 255, 255))
    ball.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()