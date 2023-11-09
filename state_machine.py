import pygame
import config
from config import SCREEN_RESOLUTION, ORIGIN
from bitmapfont import BitmapFont
from scene import Menu, Game, Pause

class StateMachine:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((320, 240), pygame.NOFRAME)# pygame.FULLSCREEN)
        self.font = BitmapFont(config.FONT_FILENAME, config.FONT_WIDTH, config.FONT_HEIGHT)
        self.fullscreen = False

        self.states = {"Menu": Menu(self), "Game": Game(self), "Pause": Pause(self)}
        self.current_state = self.states["Menu"]
        self.transitions = {
            ("Menu", pygame.K_LSHIFT): "Game",
            ("Pause", pygame.K_p): "Game",
            ("Game", pygame.K_p): "Pause",
            ("Game", pygame.K_ESCAPE): "Menu",
        }

    def transition(self, new_state):
        print(f'{self.current_state} -> {self.states[new_state]}')
        self.current_state = self.states[new_state]

    def handle_events(self):
        if pygame.key.get_pressed()[pygame.K_F11]:
            self.toggle_fullscreen()
        events = pygame.event.get()
        self.current_state.handle_events(events)

    def update_gfx(self):
        self.current_state.update_gfx()

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        temp_surface = self.screen.copy()
        if self.fullscreen:
            self.screen = pygame.display.set_mode(SCREEN_RESOLUTION, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(SCREEN_RESOLUTION, pygame.NOFRAME)
        self.screen.blit(temp_surface, ORIGIN)  # Blit the old screen surface onto the new one
        pygame.display.update()

    def handle_transitions(self):
        'Scene changes occur via certain keypresses'
        keys = pygame.key.get_pressed()
        for key, state in self.transitions.items():
            if keys[key[1]]:
                self.transition(state)
                break

    def handle_transitions(self):
        keys = pygame.key.get_pressed()
        if isinstance(self.current_state, Menu) and keys[pygame.K_LSHIFT]:
            self.transition("Game")
        elif isinstance(self.current_state, Pause) and keys[pygame.K_p]:
            self.transition("Game")
        elif isinstance(self.current_state, Game):
            if keys[pygame.K_p]:
                self.transition("Pause")
            elif keys[pygame.K_ESCAPE]:
                self.transition("Menu")

    def run(self):
        while True:
            self.handle_events()
            self.handle_transitions()
            self.update_gfx()

def main():
    state_machine = StateMachine()
    state_machine.run()

if __name__ == "__main__":
    main()
