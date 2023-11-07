import sys

import pygame

from game import Game
import config
from config import ORIGIN, SCREEN_WIDTH, SCREEN_HEIGHT

from piece import Piece
from grid import Grid
import gfx
from gfx import GRID_COLS, GRID_ROWS
from event import Event
from bitmapfont import BitmapFont

class Tetris(Game):
    def __init__(self):
        super().__init__()
        self.grid = Grid(GRID_COLS, GRID_ROWS)
        self.piece = Piece(self.grid)
        self.font = BitmapFont(config.FONT_FILENAME, config.FONT_WIDTH, config.FONT_HEIGHT)
        self.paused = False

    def run(self):
        self.running = True
        pygame.time.set_timer(Event.GRAVITY, 500)
        while self.running:
            self.get_user_events()
            self.update_gfx()

    def toggle_pause(self):
        self.paused = not self.paused

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
                if event.key == pygame.K_DOWN:
                    self.piece.update_position(dy=1)
                if event.key == pygame.K_UP:
                    self.piece.update_position(dy=-1)
                if event.key == pygame.K_RIGHT:
                    self.piece.update_position(dx=1)
                if event.key == pygame.K_LEFT:
                    self.piece.update_position(dx=-1)
                if event.key == pygame.K_LSHIFT:
                    self.piece.update_position(drotate=1)
                if event.key == pygame.K_c:
                    self.grid.clear_cells()
                if event.key == pygame.K_p:
                    self.grid.clear_cells()
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                    break
            if event.type == Event.GRAVITY:
                self.piece.update_position(dy=1)
            #if event.type == Event.GAME_OVER:
            #    print(event.message)

    def update_gfx(self):
        self.grid.update_gfx()
        # this should be partial blit - everything execpt top two rows
        # Rect(left, top, width, height)
        self.status_text = f'-----------\nPIECES: {self.piece.count}\n-----------\nLINES: {self.grid.lines_made}\n\n\n\n\n\n\nTetromania\n(c) Maxivision 1986\n'
        self.font.draw_text(self.status_text, self.screen, gfx.CENTRE_SCREEN_X, config.FONT_HEIGHT)
        self.screen.blit(self.grid.surface,
                         gfx.GRID_CENTRE_SCREEN_DEST_RECT,
                         area=gfx.GRID_VISIBLE_SRC_RECT)
        self.piece.draw_to_surface(self.screen,
                                   x_offset=gfx.GRID_CENTRE_SCREEN_DEST_RECT[0])
        self.piece.draw_next(self.screen, int(SCREEN_WIDTH*0.6), int(SCREEN_HEIGHT/2))
        pygame.display.update()
        self.clock.tick(config.SCREEN_REFRESH_RATE)
