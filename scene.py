import sys
import pygame
import config
from config import SCREEN_HEIGHT, SCREEN_WIDTH, NAME, COPYRIGHT
import gfx
from gfx import CELL_SIZE_PIXELS, GRID_COLS, GRID_ROWS, draw_crosshatch
from grid import Grid
from piece import Piece
from event import Event

class Scene:
    def __init__(self, state_machine):
        self.screen = state_machine.screen
        self.clock = state_machine.clock
        self.font = state_machine.font

    def handle_events(self, events):
        pass

    def update_gfx(self):
        pygame.display.update()
        self.clock.tick(config.SCREEN_REFRESH_RATE)

class Menu(Scene):
    def __init__(self, state_machine):
        super().__init__(state_machine)
        self.text = f'{NAME}\n{COPYRIGHT}\n\nEsc - Quit\nLSHIFT - New Game\nF11 - Toggle Fullscreen'
        self.key_actions = {
            pygame.K_ESCAPE: 'quit',
        }

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                action = self.key_actions.get(event.key)
                if action is not None:
                    if action == 'quit':
                        self.quit()

    def update_gfx(self):
        gfx.draw_crosshatch(self.screen, gfx.BLUE, crosshatch_size=1)
        self.font.draw_text(self.text, self.screen, gfx.CENTRE_SCREEN_X, config.SCREEN_HEIGHT - config.FONT_HEIGHT - (8 * config.FONT_HEIGHT))
        super().update_gfx()

    def quit(self):
        pygame.quit()
        sys.exit()


class Game(Scene):
    def __init__(self, state_machine):
        super().__init__(state_machine)
        self.grid = Grid(GRID_COLS, GRID_ROWS)
        self.piece = Piece(self.grid)
        pygame.time.set_timer(Event.GRAVITY, gfx.INITIAL_GRAVITY_INTERVAL_MS)

        self.key_actions = {
            pygame.K_DOWN: (0, 1, 0),
            pygame.K_UP: (0, -1, 0),
            pygame.K_RIGHT: (1, 0, 0),
            pygame.K_LEFT: (-1, 0, 0),
            pygame.K_LSHIFT: (0, 0, 1),
            pygame.K_c: 'clear',
        }

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                action = self.key_actions.get(event.key)
                if action is not None:
                    if action == 'clear':
                        self.grid.clear_cells()
                    else:
                        dx, dy, drotate = action
                        self.piece.update_position(dx=dx, dy=dy, drotate=drotate)
            elif event.type == Event.GRAVITY:
                self.piece.update_position(dy=1)

    def update_gfx(self):
        self.grid.update_gfx()
        self.status_text = f'PIECE: {self.piece.count}  LINES: {self.grid.lines_made}'
        self.font.draw_text(self.status_text, self.screen, gfx.CENTRE_SCREEN_X, SCREEN_HEIGHT - config.FONT_HEIGHT - (4 * config.FONT_HEIGHT))
        #self.font.draw_text('', self.screen, gfx.CENTRE_SCREEN_X, SCREEN_HEIGHT - config.FONT_HEIGHT)        
        self.screen.blit(self.grid.surface, gfx.GRID_CENTRE_SCREEN_DEST_RECT, area=gfx.GRID_VISIBLE_SRC_RECT)
        self.piece.draw_to_surface(self.screen, x_offset=gfx.GRID_CENTRE_SCREEN_DEST_RECT[0])
        pygame.draw.rect(self.screen, gfx.BLACK, (int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT*1/2), CELL_SIZE_PIXELS*4, CELL_SIZE_PIXELS*2))
        self.piece.draw_next(self.screen, gfx.CENTRE_SCREEN_X, int(SCREEN_HEIGHT*0.5))
        super().update_gfx()


class Pause(Scene):
    def __init__(self, state_machine):
        super().__init__(state_machine)

    def update_gfx(self):
        gfx.draw_crosshatch(self.screen, gfx.BLACK, crosshatch_size=1)
        super().update_gfx()
