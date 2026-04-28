import pygame as py
#screen settings
SIZE = 800
CELL_SIZE = 40
GRID_WIDTH = SIZE // CELL_SIZE 
GRID_HEIGHT = SIZE // CELL_SIZE
FPS = 60
#colors
COLOR_BG = (20, 20, 20)
COLOR_SNAKE_DEFAULT = (127, 255, 0)
COLOR_TEXT = (255, 255, 255)
COLOR_FOOD_1 = (255, 99, 71)   # Tomato Red
COLOR_FOOD_2 = (0, 191, 255)   # Deep Sky Blue
COLOR_FOOD_3 = (255, 215, 0)   # Gold
COLOR_POISON = (139, 0, 0)     # Dark Red
COLOR_WALL = (70, 70, 70)      # Grey
COLOR_UI_BG = (50, 50, 50)

INITIAL_SPEED = 200   #delay in ms (lower is faster)
SPEED_INCREMENT = 10 #how much faster it gets per level
MIN_SPEED = 60  #speed cap
LEVEL_UP_THRESHOLD = 4 #points needed to level up

#timers
FOOD_TIMER = 5000 #normal food 5 sec
POWERUP_TIMER = 8000 #power-up disappears after 8 sec
POWERUP_EFFECT_DURATION = 5000 #speed or slow effect for 5 sec

#weights of a normal food
FOOD_WEIGHTS = [70, 20, 10]

SETTINGS_FILE = "settings.json"

#power ups
PWR_SPEED = "SPEED"
PWR_SLOW = "SLOW"
PWR_SHIELD = "SHIELD"

#drawing the grid
def get_grid_range():
    return (CELL_SIZE // 2, SIZE - CELL_SIZE // 2, CELL_SIZE)