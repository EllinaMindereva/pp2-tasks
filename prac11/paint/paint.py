import pygame, sys

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
base_layer = pygame.Surface((WIDTH, HEIGHT)) #base_layer
pygame.display.set_caption("Paint game")
COLOR = BLACK #default color
clock = pygame.time.Clock()
screen.fill(WHITE)
LMBpressed = False
THICKNESS = 5 #initial thickness of the tool

tools = ('brush', 'rectangle', 'square', 'circle', 'righttriangle', 'equilateraltriangle', 'eraser')
TOOL = tools[0]

def calculate_rect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2)) #getting rectangle coordinates

def calculate_square(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(x1 - x2)) #getting square coordinates

def calculate_rhombus(x1, y1, x2, y2):
    width  = abs(x1 - x2)
    height = abs(y1 - y2)
    left_x = min(x1, x2)
    top_y  = min(y1, y2)

    top_point = (left_x + width // 2, top_y)
    rigth_point = (left_x + width, top_y + height // 2)
    bottom_point = (left_x + width // 2, top_y + height)
    left_point = (left_x, top_y + height // 2)
    return (top_point, rigth_point, bottom_point, left_point) #getting rhombus coordinates

def calculate_circle(x1, y1, x2, y2):
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    radius = min(abs(x2 - x1), abs(y2 - y1)) // 2 #getting circle coordinates
    return (center_x, center_y), radius

def calculate_right_triangle(x1, y1, x2, y2): #getting right triangle coordinates
    width  = abs(x1 - x2)
    height = abs(y1 - y2)
    left_x = min(x1, x2)
    top_y  = min(y1, y2)

    a = (left_x, top_y)
    b = (left_x + width, top_y + height)
    c = (left_x, top_y + height)
    return (a, b, c)

def calculate_equilateral_triangle(x1, y1, x2, y2): #getting equilateral triangle coordinates
    width  = abs(x1 - x2)
    height = ((width)*(3**1/2))/2
    left_x = min(x1, x2)
    top_y  = min(y1, y2)

    a = (left_x + width // 2, top_y)
    b = (left_x, top_y + height)
    c = (left_x + width, top_y + height)
    return (a, b, c)

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
                else:
                    screen.blit(base_layer, (0, 0))
                    draw_figure(screen, COLOR, (prevX, prevY, currX, currY))

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False
            currX = event.pos[0]
            currY = event.pos[1]
            draw_figure(screen, COLOR, (prevX, prevY, currX, currY))
            base_layer.blit(screen, (0, 0))

        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_EQUALS:
                THICKNESS += 1
            if event.key == pygame.K_MINUS:
                THICKNESS -= 1
            if event.key == pygame.K_c: #tool that clears everything
                screen.fill(WHITE)
                base_layer.fill(WHITE)
            if event.key == pygame.K_b: #pressing the following buttons to change the color and tools
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
            
    small_font = pygame.font.SysFont("comicsansms", 20) #font
    pygame.draw.rect(screen, (224,255,255), (0, 0, WIDTH, 110))
    text = small_font.render("COLORS: B - blue, P - pink, Y - yellow, G - green, H - black", True, BLACK) #instructions
    screen.blit(text, (10, 10))
    text2 = small_font.render("TOOLS: 1 - brush, 2 - rectangle, 3 - square, 4 - rhombus, 5 - circle, 6 - right triangle, \n7 - equilateral triangle, 8 - eraser, C - clear", True, BLACK)
    screen.blit(text2, (10, 35))
    pygame.display.flip()
    clock.tick(60)