import pygame, datetime
pygame.init()

tools = ('brush', 'rectangle', 'square', 'circle', 'righttriangle', 'equilateraltriangle', 'eraser', 'line', 'fill_tool', 'text_tool')

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

def fill_tool(surface, x1, y1, fill_color):
    width, height = surface.get_size()
    target_color = surface.get_at((x1, y1))
    if target_color == fill_color:
        return

    border = [(x1, y1)]
    while border:
        x, y = border.pop()
        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        curr_color = surface.get_at((x, y))

        if curr_color != target_color:
            continue

        surface.set_at((x, y), fill_color)

        border.append((x + 1, y))
        border.append((x - 1, y))
        border.append((x, y + 1))
        border.append((x, y - 1))

def save_image(surface):
    time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    name = f"picture_{time}.png"
    pygame.image.save(surface, name)

class Text_tool:
    def __init__(self):
        self.active = False
        self.text = ""
        self.pos = (0, 0)
        self.font = pygame.font.SysFont("comicsansms", 27)

    def activate(self, pos):
        self.active = True
        self.pos = pos
        self.text = ""

    def keydown(self, event):
        if event.key == pygame.K_RETURN:
            return "confirm"
        elif event.key == pygame.K_ESCAPE:
            self.active = False
            return "cancel"
        else:
            self.text += event.unicode
        return "typing"

    def draw_preview(self, screen, color):
        if self.active:
            text_surface = self.font.render(self.text, True, color)
            screen.blit(text_surface, self.pos)

    def finalize(self, surface, color):
        if self.text:
            text_surface = self.font.render(self.text, True, color)
            surface.blit(text_surface, self.pos)
        self.active = False