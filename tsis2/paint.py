import pygame, sys
from tools import *
import datetime
pygame.init()

BLUE = (38, 191, 255)
PINK = (255, 151, 242)
YELLOW = (255, 235, 101) #adding the colors
GREEN = (0, 213, 57)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIDTH = 900
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #creating the display
screen.fill(WHITE)
base_layer = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("Paint game")
COLOR = BLACK #default color
clock = pygame.time.Clock()
LMBpressed = False
THICKNESS = 5 #initial thickness of the tool

TOOL = tools[0]

currX, currY, prevX, prevY = 0, 0, 0, 0

def draw_figure(surface, color, points): #tools
    points = prevX, prevY, currX, currY
    if TOOL == 'brush':
        pygame.draw.line(screen, COLOR, (prevX, prevY), (currX, currY), THICKNESS)
    elif TOOL == 'eraser':
        pygame.draw.circle(screen, WHITE, (currX, currY), THICKNESS)
    elif TOOL == 'rectangle':
        pygame.draw.rect(screen, COLOR, calculate_rect(prevX, prevY, currX, currY), THICKNESS)
    elif TOOL == 'rhombus':
        pygame.draw.polygon(screen, COLOR, calculate_rhombus(prevX, prevY, currX, currY), THICKNESS)
    elif TOOL == 'square':
        pygame.draw.rect(screen, COLOR, calculate_square(prevX, prevY, currX, currY), THICKNESS)
    elif TOOL == 'circle':
        center, radius = calculate_circle(prevX, prevY, currX, currY)
        pygame.draw.circle(screen, COLOR, center, radius, THICKNESS)
    elif TOOL == 'righttriangle':
        pygame.draw.polygon(screen, COLOR, calculate_right_triangle(prevX, prevY, currX, currY), THICKNESS)
    elif TOOL == 'equilateraltriangle':
        pygame.draw.polygon(screen, COLOR, calculate_equilateral_triangle(prevX, prevY, currX, currY), THICKNESS)
    elif TOOL == 'line':
        pygame.draw.line(screen, COLOR, (prevX, prevY), (currX, currY), THICKNESS)

text_tool = Text_tool()

#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMBpressed = True
            prevX = event.pos[0]
            prevY = event.pos[1]
            if TOOL == 'fill_tool':
                fill_tool(screen, prevX, prevY, COLOR)
                base_layer.blit(screen, (0, 0))
            if TOOL == 'text_tool':
                text_tool.activate(event.pos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                TOOL = 'text_tool'
            if TOOL == 'text_tool' and text_tool.active:
                result = text_tool.keydown(event)
                if result == "confirm":
                    text_tool.finalize(base_layer, COLOR)
                elif result == "cancel":
                    text_tool.active = False
                    screen.blit(base_layer, (0, 0))
        if TOOL == 'text_tool':
            text_tool.draw_preview(screen, COLOR)

        if event.type == pygame.MOUSEMOTION:
            if LMBpressed:
                currX = event.pos[0]
                currY = event.pos[1]
                if TOOL == 'brush':
                    pygame.draw.line(screen, COLOR, (prevX, prevY), (currX, currY), THICKNESS)
                    base_layer.blit(screen, (0, 0))
                    prevX = currX
                    prevY = currY
                elif TOOL == 'eraser':
                    pygame.draw.circle(screen, WHITE, (currX, currY), THICKNESS)
                    base_layer.blit(screen, (0, 0))
                elif TOOL == 'line':
                    screen.blit(base_layer, (0, 0))
                    pygame.draw.line(screen, COLOR, (prevX, prevY), (currX, currY), THICKNESS)
                else:
                    screen.blit(base_layer, (0, 0))
                    draw_figure(screen, COLOR, (prevX, prevY, currX, currY))

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False
            currX = event.pos[0]
            currY = event.pos[1]
            if TOOL == 'line':
                screen.blit(base_layer, (0, 0))
                pygame.draw.line(screen, COLOR, (prevX, prevY), (currX, currY), THICKNESS)
            else:
                draw_figure(screen, COLOR, (prevX, prevY, currX, currY))
            base_layer.blit(screen, (0, 0))

        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_EQUALS:
                THICKNESS += 1
            if event.key == pygame.K_MINUS:
                THICKNESS -= 1
            if event.key == pygame.K_q:
                THICKNESS = 2
            if event.key == pygame.K_a:
                THICKNESS = 5
            if event.key == pygame.K_z:
                THICKNESS = 10
            if event.key == pygame.K_c: #tool that clears everything
                screen.fill(WHITE)
                base_layer.fill(WHITE)
            if event.key == pygame.K_b: #pressing the following buttons to change the color 
                COLOR = BLUE
            if event.key == pygame.K_p:
                COLOR = PINK
            if event.key == pygame.K_g:
                COLOR = GREEN
            if event.key == pygame.K_y:
                COLOR = YELLOW
            if event.key == pygame.K_h:
                COLOR = BLACK
            if event.key == pygame.K_1:
                TOOL = 'brush'
            if event.key == pygame.K_2:
                TOOL = 'rectangle'
            if event.key == pygame.K_3:
                TOOL = 'square'
            if event.key == pygame.K_4:
                TOOL = 'rhombus'
            if event.key == pygame.K_5:
                TOOL = 'circle'
            if event.key == pygame.K_6:
                TOOL = 'righttriangle'
            if event.key == pygame.K_7:
                TOOL = 'equilateraltriangle'
            if event.key == pygame.K_8:
                TOOL = 'eraser'
            if event.key == pygame.K_9:
                TOOL = 'line'
            if event.key == pygame.K_0:
                TOOL = 'fill_tool'
            if event.key == pygame.K_s and event.mod and pygame.KMOD_LCTRL:
                save_image(base_layer)
            
    small_font = pygame.font.SysFont("comicsansms", 20)
    pygame.draw.rect(screen, (224,255,255), (0, 0, WIDTH, 140))
    text = small_font.render("COLORS: B - blue, P - pink, Y - yellow, G - green, H - black", True, BLACK)
    screen.blit(text, (10, 10))
    text2 = small_font.render("TOOLS: 1 - brush, 2 - rectangle, 3 - square, 4 - rhombus, 5 - circle, 6 - right triangle,", True, BLACK)
    screen.blit(text2, (10, 35))
    text3 = small_font.render("7 - equilateral triangle, 8 - eraser, 9 - line, 0 - fill tool, C - clear, Ctrl+S - save, T - text", True, BLACK)
    screen.blit(text3, (10, 60))
    text4 = small_font.render("SIZE: Q - 2px, A - 5px, Z - 10px, + and -", True, BLACK)
    screen.blit(text4, (10, 85))
    pygame.display.flip()
    clock.tick(60)