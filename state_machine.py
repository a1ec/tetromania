import sys
import pygame
from scene import Menu, Game, Pause
import config

class StateMachine:
    def __init__(self):
        self.states = {"Menu": Menu(), "Game": Game(), "Pause": Pause()}
        self.current_state = self.states["Menu"]

    def transition(self, new_state):
        print(f'{self.current_state} -> {self.states[new_state]}')
        self.current_state = self.states[new_state]

    def init_game_lib(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((320, 240), pygame.NOFRAME)# pygame.FULLSCREEN)

    def handle_events(self, events):
        self.current_state.handle_events(events)

    def update_gfx(self):
        self.clock.tick(config.SCREEN_REFRESH_RATE)

    def run(self):
        self.init_game_lib()

        while True:
            events = pygame.event.get()
            self.handle_events(events)

            # Transition between states based on some condition
            if isinstance(self.current_state, Menu) and pygame.key.get_pressed()[pygame.K_LSHIFT]:
                self.transition("Game")
            elif isinstance(self.current_state, Game) and pygame.key.get_pressed()[pygame.K_p]:
                self.transition("Pause")
            elif isinstance(self.current_state, Pause) and pygame.key.get_pressed()[pygame.K_p]:
                self.transition("Game")
            elif isinstance(self.current_state, Game) and pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.transition("Menu")
            self.update_gfx()

def main():
    state_machine = StateMachine()
    state_machine.run()        

if __name__ == "__main__":
    main()
