import gfx
from gfx import BLOCK_SIZE, GRID_OPACITY, COLORS, FG_COLOR
from config import SCREEN_RESOLUTION, ORIGIN

import pygame

class Block:
    def __init__(self, grid):
        self.x = 0
        self.y = 0
        self.new_x = None
        self.new_y = None 
        self.width = 1
        self.height = 1
        self.color = 2
        self.grid = grid

    def place(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx=0, dy=0):
        self.new_x = self.x + dx
        if not self.has_hit_sides():
            self.x = self.new_x
        self.new_y = self.y + dy
        if not self.has_hit_bottom():
            self.y = self.new_y

    def draw(self):
        self.grid.outline_cell(self.x, self.y, self.color)

    def set_color(self, color):
        self.color = color

    def cycle_color(self):
        self.color += 1
        self.color %= len(COLORS)

    def set_down(self):
        self.grid.set_cell(self.x, self.y, self.color)

    def has_hit_sides(self):
        if self.new_x < 0 or self.new_x + self.width > self.grid.width:
            return True
        return False

    def has_hit_bottom(self):
        if self.new_y + self.height > self.grid.height:
            return True
        return False


class Grid:
    def __init__(self, width, height, lines_opacity=GRID_OPACITY):
        self.width = width
        self.height = height
        self.cells = None
        self.surface = pygame.Surface(SCREEN_RESOLUTION)
        self.overlay = pygame.Surface(SCREEN_RESOLUTION, pygame.SRCALPHA)
        self.lines_opacity = lines_opacity
        self.init_overlay()
        self.clear_cells()

    def init_overlay(self, grid_size=BLOCK_SIZE, color=FG_COLOR, opacity=GRID_OPACITY):
        'Draws a translucent grid onto a surface'
        opacity = (opacity, )
        # Draw the grid lines on the grid surface
        for y in range(0, self.height * grid_size + grid_size, grid_size):
            if y != 0:
                y -= 1
            pygame.draw.line(self.overlay, color + opacity, (0, y), (self.width * grid_size, y), 1)
        for x in range(0, self.width * grid_size + grid_size, grid_size):
            if x != 0:
                x -= 1
            pygame.draw.line(self.overlay, color + opacity, (x, 0), (x, self.height * grid_size), 1)

    def set_cell(self, x, y, color):
        'Sets grid value to a color (non-zero)'
        self.cells[y][x] = color

    def clear_cells(self):
        'Clears all grid elements to zero'
        self.cells = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def draw_cells(self):
        'Draw all the cells in the grid'
        y = 0
        for line in self.cells:
            x = 0
            for color in line:
                self.fill_cell(x, y, color)
                x += 1
            y += 1

    def fill_cell(self, x, y, color):
        'Draw a filled block on the surface'
        pygame.draw.rect(self.surface,
                         COLORS[color] + (255, ),
                         pygame.Rect(x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def outline_cell(self, x, y, color):
        'Draw an unfilled block on the surface'
        pygame.draw.rect(self.surface,
                         COLORS[color] + (255, ),
                         pygame.Rect(x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def get_centre(self):
        return int(self.width/2), int(self.height/2)

    def draw_overlay(self):
        self.surface.blit(self.overlay, ORIGIN)

    def draw(self):
        self.draw_cells()
        self.draw_overlay()

