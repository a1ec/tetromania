import pygame
import config
from config import ORIGIN, BLOCK_SIZE
import colors
from block import Block

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(config.SCREEN_PIXEL_DIMENSIONS, pygame.FULLSCREEN)
        self.grid_surface = pygame.Surface(config.SCREEN_PIXEL_DIMENSIONS, pygame.SRCALPHA)
        self.block = Block()
        self.running = False

    def draw_grid(self, grid_size=BLOCK_SIZE, color=colors.WHITE, opacity=config.GRID_OPACITY):
        opacity = (opacity, )
        # Draw the grid lines on the grid surface
        for y in range(0, config.SCREEN_HEIGHT, grid_size):
            pygame.draw.line(self.grid_surface, color + opacity, (0, y), (config.SCREEN_WIDTH, y), 1)
        for x in range(0, config.SCREEN_WIDTH, grid_size):
            pygame.draw.line(self.grid_surface, color + opacity, (x, 0), (x, config.SCREEN_HEIGHT), 1)

    def draw_block(self):
        pygame.draw.rect(self.grid_surface,
                         self.block.color + (255, ),
                         pygame.Rect(self.block.x*BLOCK_SIZE, self.block.y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def run(self):
        self.draw_grid()
        self.running = True
        while self.running:
            self.get_user_events()
            self.update()

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


    def update(self):
        self.screen.fill(colors.DARK_BLUE)
        self.draw_block()
        self.screen.blit(self.grid_surface, ORIGIN)
        pygame.display.update()
        self.clock.tick(config.SCREEN_UPDATE_HERTZ)