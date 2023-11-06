from enum import Enum
from config import SCREEN_WIDTH, SCREEN_HEIGHT
import pygame
from pygame import Rect, Surface

GRID_OPACITY = 64 # 0-255 Alpha value
GRID_WIDTH = 20
BLOCK_SIZE = 16 #int(SCREEN_WIDTH / GRID_WIDTH)
GRID_HEIGHT = 16 #int(SCREEN_HEIGHT / BLOCK_SIZE)

class Color(Enum):
    DARK_BLUE = (44, 44, 127)
    DARK_GREY = (26, 31, 40)
    GREEN = (47, 230, 23)
    RED = (232, 18, 18)
    ORANGE = (226, 116, 17)
    YELLOW = (237, 234, 4)
    PURPLE = (166, 0, 247)
    CYAN = (21, 204, 209)
    BLUE = (13, 64, 216)
    WHITE = (255, 255, 255)
    LIGHT_BLUE = (59, 85, 162)

DARK_BLUE = (44, 44, 127)
DARK_GREY = (26, 31, 40)
GREEN = (47, 230, 23)
RED = (232, 18, 18)
ORANGE = (226, 116, 17)
YELLOW = (237, 234, 4)
PURPLE = (166, 0, 247)
CYAN = (21, 204, 209)
BLUE = (13, 64, 216)
WHITE = (255, 255, 255)
LIGHT_BLUE = (59, 85, 162)

COLORS = [DARK_BLUE, GREEN, RED, ORANGE, YELLOW,
         PURPLE, CYAN, BLUE, WHITE, DARK_GREY,
         LIGHT_BLUE]

#COLORS = {color: i for i, color in enumerate(Color)}

BG_COLOR = DARK_BLUE
FG_COLOR = WHITE

def fill_cell(grid_x, grid_y, color, surface):
    'Draw a filled block on the surface'
    pygame.draw.rect(surface, COLORS[color] + (255, ),
                     pygame.Rect(grid_x*BLOCK_SIZE, grid_y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))