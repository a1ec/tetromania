from enum import Enum
from config import SCREEN_WIDTH, SCREEN_HEIGHT
import pygame
from pygame import Rect, Surface

GRID_OPACITY = 24 # 0-255 Alpha value
CELL_SIZE_PIXELS = 12
GRID_COLS = 10
GRID_ROWS = 20 # 20 visible
GRID_ROWS_HIDDEN = 0
CENTRE_SCREEN_X = SCREEN_WIDTH / 2
GRID_WIDTH_PIXELS = CELL_SIZE_PIXELS * GRID_COLS
GRID_HEIGHT_PIXELS = CELL_SIZE_PIXELS * GRID_ROWS
GRID_HEIGHT_PIXELS_VISIBLE = CELL_SIZE_PIXELS * (GRID_ROWS - GRID_ROWS_HIDDEN)
GRID_X0 = int(CENTRE_SCREEN_X - (GRID_WIDTH_PIXELS / 2))
GRID_X0 = 0
GRID_CENTRE_SCREEN_DEST_RECT = pygame.Rect(GRID_X0, 0, 
                                           GRID_WIDTH_PIXELS,
                                           GRID_HEIGHT_PIXELS)
GRID_VISIBLE_SRC_RECT = pygame.Rect(0, GRID_ROWS_HIDDEN * CELL_SIZE_PIXELS, 
                                    GRID_WIDTH_PIXELS,
                                    GRID_HEIGHT_PIXELS)

class Color(Enum):
    DARK_GREY = (26, 31, 40)
    DARK_BLUE = (44, 44, 127)
    GREEN = (47, 230, 23)
    RED = (232, 18, 18)
    ORANGE = (226, 116, 17)
    YELLOW = (237, 234, 4)
    PURPLE = (166, 0, 247)
    CYAN = (21, 204, 209)
    BLUE = (13, 64, 216)
    WHITE = (255, 255, 255)
    LIGHT_BLUE = (59, 85, 162)
    MAGENTA = (255, 0, 255)
    BLACK = (0, 0, 0)

DARK_GREY = (26, 31, 40)
DARK_BLUE = (44, 44, 127)
GREEN = (47, 230, 23)
RED = (232, 18, 18)
ORANGE = (226, 116, 17)
YELLOW = (237, 234, 4)
PURPLE = (166, 0, 247)
CYAN = (21, 204, 209)
BLUE = (13, 64, 216)
WHITE = (255, 255, 255)
LIGHT_BLUE = (59, 85, 162)
MAGENTA = (255, 0, 255)
BLACK = (0, 0, 0)

COLORS = [DARK_GREY, DARK_BLUE, GREEN, RED, ORANGE, YELLOW,
         PURPLE, CYAN, BLUE, WHITE, LIGHT_BLUE, MAGENTA, BLACK]

#COLORS = {color: i for i, color in enumerate(Color)}

BG_COLOR = DARK_GREY
FG_COLOR = WHITE

def draw_crosshatch(surface, color, crosshatch_size=1):
    width, height = surface.get_size()
    for i in range(0, width, crosshatch_size):
        for j in range(0, height, crosshatch_size):
            if (i + j) % (2 * crosshatch_size) == 0:
                pygame.draw.rect(surface, color, (i, j, crosshatch_size, crosshatch_size))

def fill_cell(grid_x, grid_y, color, surface, x_offset=0, y_offset=0):
    'Draw a filled cell on a Surface'
    pygame.draw.rect(surface, COLORS[color] + (255, ),
                     pygame.Rect(x_offset + grid_x * CELL_SIZE_PIXELS, 
                                 y_offset + grid_y * CELL_SIZE_PIXELS,
                                 CELL_SIZE_PIXELS, CELL_SIZE_PIXELS))