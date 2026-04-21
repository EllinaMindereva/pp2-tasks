import pygame, sys
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #creating the dislay
pygame.display.set_caption("Paint game")
BLUE = (38, 191, 255)
PINK = (255, 151, 242)
YELLOW = (255, 235, 101) #adding the colors
GREEN = (0, 213, 57)
BLACK = (0, 0, 0)
COLOR = BLUE

clock = pygame.time.Clock()
clock.tick(60)

LMBpressed = False
THICKNESS = 5 #initial thickness of the tool

currX = 0
currY = 0
prevX = 0
prevY = 0
#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #to draw a line when the mouse button is pressed
            LMBpressed = True
            currX = event.pos[0]
            currY = event.pos[1]
            prevX = event.pos[0]
            prevY = event.pos[1]
        if event.type == pygame.MOUSEMOTION: #track mouse motion to draw a line
            if LMBpressed:
                currX = event.pos[0]
                currY = event.pos[1]
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1: #mouse button up to finish the line
            LMBpressed = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_EQUALS: #if we press "=" button, it will make the line thicker
                THICKNESS += 1
            if event.key == pygame.K_MINUS: #and if "-" it will be thinner
                THICKNESS -= 1
            if event.key == pygame.K_c: #eraser, it erases everything
                screen.fill(BLACK)
            if event.key == pygame.K_b: #pressing the following buttons to change the color 
                COLOR = BLUE
            if event.key == pygame.K_p:
                COLOR = PINK
            if event.key == pygame.K_g:
                COLOR = GREEN
            if event.key == pygame.K_y:
                COLOR = YELLOW
            if event.key == pygame.K_r:  #draw a rectangle (random place and random size)
                pygame.draw.rect(screen, COLOR, (random.randint(10, 500), random.randint(10, 500), random.randint(10, 500), random.randint(10, 500)), THICKNESS)
            if event.key == pygame.K_o: #draw a circle (random place and random size)
                pygame.draw.circle(screen, COLOR, (random.randint(10, 400), random.randint(10, 400)), random.randint(10, 100), THICKNESS)


    if LMBpressed:
        pygame.draw.line(screen, COLOR, (prevX, prevY), (currX, currY), THICKNESS) #drawing a line
    
    small_font = pygame.font.SysFont("comicsansms", 20)
    text = small_font.render("B - blue, P - pink, Y - yellow, G - green, C - eraser, R - rectangle, O - circle", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    prevX = currX
    prevY = currY

    pygame.display.flip() #updating the screen
