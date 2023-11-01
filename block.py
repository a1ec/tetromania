import gfx
from gfx import BLOCK_SIZE, GRID_OPACITY, COLORS, FG_COLOR, BG_COLOR
from config import SCREEN_RESOLUTION, ORIGIN

import pygame

class Block:
    def __init__(self, block_grid):
        self.x = 0
        self.y = 0
        self.color = 2
        self.block_grid = block_grid

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

    def draw(self):
        self.block_grid.draw_block_outline(self.x, self.y, self.color)

    def cycle_color(self):
        self.color += 1
        self.color %= len(COLORS)

    def set_down(self):
        self.block_grid.set_block(self.x, self.y, self.color)

    def is_in_grid(self):
        if self.x < 0 or self.x > self.block_grid.width or \
           self.y < 0 or self.y > self.block_grid.height:
            return False
        return True

class BlockGrid:
    def __init__(self, width, height, grid_opacity=GRID_OPACITY):
        self.width = width
        self.height = height
        self.blocks = [[0 for _ in range(width)] for _ in range(height)]
        self.surface = pygame.Surface(SCREEN_RESOLUTION)
        self.overlay = pygame.Surface(SCREEN_RESOLUTION, pygame.SRCALPHA)
        self.grid_opacity = grid_opacity
        self.setup_overlay()

    def setup_overlay(self, grid_size=BLOCK_SIZE, color=FG_COLOR, opacity=GRID_OPACITY):
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

    def set_block(self, x, y, color):
        self.blocks[y][x] = color

    def draw_blocks(self):
        y = 0
        for line in self.blocks:
            x = 0
            for color in line:
                self.draw_block(x, y, color)
                x += 1
            y += 1

    def draw_block(self, x, y, color):
        pygame.draw.rect(self.surface,
                         COLORS[color] + (255, ),
                         pygame.Rect(x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_overlay(self):
        self.surface.blit(self.overlay, ORIGIN)

    def draw(self):
        self.draw_blocks()
        self.draw_overlay()

    def draw_block_outline(self, x, y, color):
        pygame.draw.rect(self.surface,
                         COLORS[color] + (255, ),
                         pygame.Rect(x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
