import pygame
from game import Game
import config
from config import ORIGIN
import gfx
from gfx import BLOCK_SIZE, COLORS, WHITE, DARK_BLUE
from block import Block

class Tetris(Game):
    def __init__(self):
        super().__init__()
        self.blocks_array = [[0 for _ in range(gfx.GRID_X_SIZE)] for _ in range(gfx.GRID_Y_SIZE)]
        self.blocks_surface = pygame.Surface(config.SCREEN_PIXEL_DIMENSIONS)
        self.grid_overlay_surface = pygame.Surface(config.SCREEN_PIXEL_DIMENSIONS, pygame.SRCALPHA)
        self.block = Block()

    def draw_grid_overlay(self, grid_size=BLOCK_SIZE, color=WHITE, opacity=gfx.GRID_OPACITY):
        opacity = (opacity, )
        # Draw the grid lines on the grid surface
        for y in range(0, config.SCREEN_HEIGHT + grid_size, grid_size):
            if y != 0:
                y -= 1
            pygame.draw.line(self.grid_overlay_surface, color + opacity, (0, y), (config.SCREEN_WIDTH, y), 1)
        for x in range(0, config.SCREEN_WIDTH + grid_size, grid_size):
            if x != 0:
                x -= 1
            pygame.draw.line(self.grid_overlay_surface, color + opacity, (x, 0), (x, config.SCREEN_HEIGHT), 1)

    def draw_blocks(self):
        y = 0
        for line in self.blocks_array:
            x = 0
            for color in line:
                self.draw_block(x, y, color)
                x += 1
            y += 1

    def set_block(self, x, y, color):
        self.blocks_array[y][x] = color

    def draw_block(self, x, y, color):
        pygame.draw.rect(self.blocks_surface,
                         COLORS[color] + (255, ),
                         pygame.Rect(x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_block_outline(self, x, y, color):
        pygame.draw.rect(self.blocks_surface,
                         COLORS[color] + (255, ),
                         pygame.Rect(x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_user_block(self):
        self.draw_block_outline(self.block.x, self.block.y, self.block.color)

    def set_user_block(self):
        self.set_block(self.block.x, self.block.y, self.block.color)

    def run(self):
        self.draw_grid_overlay()
        self.draw_blocks()
        self.running = True
        while self.running:
            self.get_user_events()
            self.update_gfx()

    def get_user_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                if event.key == pygame.K_DOWN:
                    self.block.move(dy=1)
                if event.key == pygame.K_UP:
                    self.block.move(dy=-1)
                if event.key == pygame.K_RIGHT:
                    self.block.move(dx=1)
                if event.key == pygame.K_LEFT:
                    self.block.move(dx=-1)
                if event.key == pygame.K_RSHIFT:
                    self.set_user_block()

    def update_gfx(self):
        self.screen.fill(DARK_BLUE)
        self.draw_blocks()
        self.draw_user_block()
        self.draw_grid_overlay()
        self.screen.blit(self.blocks_surface, ORIGIN)
        self.screen.blit(self.grid_overlay_surface, ORIGIN)
        pygame.display.update()
        self.clock.tick(config.SCREEN_UPDATE_HERTZ)