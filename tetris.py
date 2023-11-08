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
        self.pause_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
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
            pygame.K_ESCAPE: 'quit'
        }
        self.init_pause_overlay(fill_color=gfx.WHITE)
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

    def init_pause_overlay(self, fill_color=(0,0,0), alpha=255):
        # Create a new surface with the same size as the main screen
        self.pause_overlay.fill(gfx.BLACK)
        #self.pause_overlay.set_alpha(alpha)  # Alpha can be from 0 (fully transparent) to 255 (fully opaque)
        # Draw the crosshatch pattern
        crosshatch_size = 1  # Size of each square in the crosshatch pattern
        for i in range(0, SCREEN_WIDTH, crosshatch_size):
            for j in range(0, SCREEN_HEIGHT, crosshatch_size):
                if (i // crosshatch_size + j // crosshatch_size) % 2 == 0:
                    pygame.draw.rect(self.pause_overlay, fill_color + (0,), (i, j, crosshatch_size, crosshatch_size))  # Set every other square to be fully transparent


    def draw_pause_screen(self):
        # Draw the overlay onto the main screen
        self.screen.blit(self.pause_overlay, ORIGIN, special_flags=pygame.BLEND_RGBA_SUB)
        pygame.display.update()

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
        self.status_text = f'PIECE: {self.piece.count}  LINES: {self.grid.lines_made}\n\nTETROMANIA\n(c) MAXIVISION 1985'
        self.font.draw_text(self.status_text, self.screen, gfx.CENTRE_SCREEN_X, SCREEN_HEIGHT - config.FONT_HEIGHT - (4 * config.FONT_HEIGHT))
        self.font.draw_text('', self.screen, gfx.CENTRE_SCREEN_X, SCREEN_HEIGHT - config.FONT_HEIGHT)
        
        self.screen.blit(self.grid.surface,
                         gfx.GRID_CENTRE_SCREEN_DEST_RECT,
                         area=gfx.GRID_VISIBLE_SRC_RECT)
        self.piece.draw_to_surface(self.screen,
                                   x_offset=gfx.GRID_CENTRE_SCREEN_DEST_RECT[0])
        self.piece.draw_next(self.screen, gfx.CENTRE_SCREEN_X, int(SCREEN_HEIGHT*0.5))
        pygame.display.update()
        self.clock.tick(config.SCREEN_REFRESH_RATE)
