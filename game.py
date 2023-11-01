import pygame
import config
import colors

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(config.SCREEN_PIXEL_DIMENSIONS)#, pygame.FULLSCREEN)
        self.running = False

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

    def update_gfx(self):
        self.screen.fill(colors.DARK_BLUE)
        pygame.display.update()
        self.clock.tick(config.SCREEN_UPDATE_HERTZ)