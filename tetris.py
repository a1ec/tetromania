import pygame
from game import Game
import config
from config import ORIGIN
from gfx import GRID_WIDTH, GRID_HEIGHT, COLORS

from block import Block, BlockGrid

class Tetris(Game):
    def __init__(self):
        super().__init__()
        self.block_grid = BlockGrid(GRID_WIDTH, GRID_HEIGHT)
        self.block = Block(self.block_grid)

    def run(self):
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
                if event.key == pygame.K_LCTRL:
                    self.block.set_down()
                if event.key == pygame.K_LSHIFT:
                    self.block.cycle_color()


    def update_gfx(self):
        self.block_grid.draw()
        self.block.draw()
        self.screen.blit(self.block_grid.surface, ORIGIN)
        pygame.display.update()
        self.clock.tick(config.SCREEN_REFRESH_RATE)
