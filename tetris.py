import sys
import random
from copy import copy
import pygame
from game import Game
import config
from config import ORIGIN
from gfx import GRID_WIDTH, GRID_HEIGHT, COLORS
from shape import Shapes
from block import Block, Grid

class Event:
    ENACT_GRAVITY = pygame.USEREVENT + 1
    HIT_WALL = pygame.USEREVENT + 2
    BLOCK_SET = pygame.USEREVENT + 3

    hit_wall = pygame.event.Event(HIT_WALL, message='Donk!')
    block_set = pygame.event.Event(BLOCK_SET)

class Player:
    def __init__(self, grid: Grid):
        self.grid = grid


class Tetris(Game):
    def __init__(self):
        super().__init__()
        self.grid = Grid(GRID_WIDTH, GRID_HEIGHT)
        self.player = Player(self.grid)
        self.cursor = Block(self.grid)
        self.shapes = []
        self.shape = None
        self.get_next_shape()

    def get_next_shape(self):
        if not self.shapes:
            self.shapes = copy(Shapes)
            random.shuffle(self.shapes)
        self.shape = self.shapes.pop()

    def run(self):
        self.running = True
        while self.running:
            self.get_user_events()
            self.update_gfx()

    def stop(self):
        self.running = False

    def start(self):
        self.running = True

    def quit(self):
        pygame.quit()
        sys.exit()

    def get_user_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                    break
                if event.key == pygame.K_DOWN:
                    self.cursor.move(dy=1)
                if event.key == pygame.K_UP:
                    self.cursor.move(dy=-1)
                if event.key == pygame.K_RIGHT:
                    self.cursor.move(dx=1)
                if event.key == pygame.K_LEFT:
                    self.cursor.move(dx=-1)
                if event.key == pygame.K_LCTRL:
                    self.cursor.set_down()
                if event.key == pygame.K_LSHIFT:
                    self.shape.rotate()
                if event.key == pygame.K_RSHIFT:
                    self.get_next_shape()
                if event.key == pygame.K_c:
                    self.grid.clear_cells()
                if event.key == pygame.K_SPACE:
                    self.shape.set_on_grid(self.grid.cells, self.cursor.x, self.cursor.y)
            if event.type == Event.HIT_WALL:
                print(event.message)

    def update_gfx(self):
        self.screen.blit(self.grid.surface, ORIGIN)
        self.grid.draw()
        self.shape.draw(self.cursor.x, self.cursor.y, self.screen)
        self.cursor.draw()
        pygame.display.update()
        self.clock.tick(config.SCREEN_REFRESH_RATE)
