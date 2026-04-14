import pygame
from clock import TheClock

pygame.init()

size = 800
screen = pygame.display.set_mode((size, size))
clock = pygame.time.Clock()
clock_face = pygame.image.load("clockface.jpg")
clock_face = pygame.transform.scale(clock_face, (size, size))

center = (size // 2, size // 2)

the_clock = TheClock(center, size)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    screen.blit(clock_face, (0, 0))
    
    the_clock.draw(screen)

    pygame.display.flip()
    clock.tick(15)

pygame.quit()