import sys

import pygame

from game import Game
import config
from config import ORIGIN, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_RESOLUTION

from piece import Piece
from grid import Grid
import gfx
from gfx import GRID_COLS, GRID_ROWS, CELL_SIZE_PIXELS
from event import Event
from bitmapfont import BitmapFont

class Tetris(Game):
    def __init__(self):
        super().__init__()
        self.grid = Grid(GRID_COLS, GRID_ROWS)
        self.piece = Piece(self.grid)
        self.font = BitmapFont(config.FONT_FILENAME, config.FONT_WIDTH, config.FONT_HEIGHT)
        self.is_pause_drawn = False
        self.paused = False
        self.key_actions = {
            pygame.K_DOWN: (0, 1, 0),
            pygame.K_UP: (0, -1, 0),
            pygame.K_RIGHT: (1, 0, 0),
            pygame.K_LEFT: (-1, 0, 0),
            pygame.K_LSHIFT: (0, 0, 1),
            pygame.K_c: 'clear',
            pygame.K_p: 'pause',
            pygame.K_F11: 'toggle_fullscreen',
            pygame.K_ESCAPE: 'quit',
        }
        self.fullscreen = False

    def run(self):
        self.running = True
        pygame.time.set_timer(Event.GRAVITY, 500)
        while self.running:
            self.get_user_events()
            if not self.paused:
                self.update_gfx()
            else:
                self.draw_pause_screen()

    def toggle_pause(self):
        self.paused = not self.paused

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.paused = True
        temp_surface = self.screen.copy()
        if self.fullscreen:
            self.screen = pygame.display.set_mode(SCREEN_RESOLUTION, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(SCREEN_RESOLUTION, pygame.NOFRAME)
        self.screen.blit(temp_surface, ORIGIN)  # Blit the old screen surface onto the new one
        pygame.display.flip()

    def draw_pause_screen(self):
        gfx.draw_crosshatch(self.screen, gfx.BLACK, crosshatch_size=1)
        pygame.display.flip()

    def quit(self):
        pygame.quit()
        sys.exit()

    def get_user_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                action = self.key_actions.get(event.key)
                if action is not None:
                    if action == 'quit':
                        self.quit()
                    elif action == 'pause':
                        self.toggle_pause()
                    elif action == 'toggle_fullscreen':
                        self.toggle_fullscreen()
                    elif action == 'clear':
                        self.grid.clear_cells()
                    else:
                        dx, dy, drotate = action
                        self.piece.update_position(dx=dx, dy=dy, drotate=drotate)
            elif event.type == Event.GRAVITY and not self.paused:
                self.piece.update_position(dy=1)

    def update_gfx(self):
        self.grid.update_gfx()
        # this should be partial blit - everything execpt top two rows
        # Rect(left, top, width, height)
        self.status_text = f'PIECE: {self.piece.count}  LINES: {self.grid.lines_made}'
        self.font.draw_text(self.status_text, self.screen, gfx.CENTRE_SCREEN_X, SCREEN_HEIGHT - config.FONT_HEIGHT - (4 * config.FONT_HEIGHT))
        self.font.draw_text('', self.screen, gfx.CENTRE_SCREEN_X, SCREEN_HEIGHT - config.FONT_HEIGHT)
        
        self.screen.blit(self.grid.surface,
                         gfx.GRID_CENTRE_SCREEN_DEST_RECT,
                         area=gfx.GRID_VISIBLE_SRC_RECT)
        self.piece.draw_to_surface(self.screen,
                                   x_offset=gfx.GRID_CENTRE_SCREEN_DEST_RECT[0])
        pygame.draw.rect(self.screen, gfx.BLACK, (int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT*1/2), CELL_SIZE_PIXELS*4, CELL_SIZE_PIXELS*2))
        self.piece.draw_next(self.screen, gfx.CENTRE_SCREEN_X, int(SCREEN_HEIGHT*0.5))
        pygame.display.update()
        self.clock.tick(config.SCREEN_REFRESH_RATE)
