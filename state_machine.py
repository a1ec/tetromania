import pygame
import config
from config import SCREEN_RESOLUTION, ORIGIN
from bitmap_font import BitmapFont
from scene import Menu, Game, Pause, GameOver
from event import Event

class StateMachine:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((320, 240), pygame.NOFRAME)# pygame.FULLSCREEN)
        self.font = BitmapFont(config.FONT_FILENAME, config.FONT_WIDTH, config.FONT_HEIGHT)
        self.fullscreen = False

        self.states = {"Menu": Menu(self), "Game": Game(self), "Pause": Pause(self), "GameOver": GameOver(self)}
        self.current_state = self.states["Menu"]
        self.transitions = {
            ("Menu", pygame.K_LSHIFT): "Game",
            ("Pause", pygame.K_p): "Game",
            ("Game", pygame.K_p): "Pause",
            ("Game", pygame.K_ESCAPE): "Menu",
            ("Game", "GAME_OVER"): "GameOver",
            ("GameOver", pygame.K_ESCAPE): "Menu",
        }

    def transition(self, new_state):
        print(f'{self.current_state} -> {self.states[new_state]}')
        self.current_state = self.states[new_state]

    def handle_events(self, events):
        if pygame.key.get_pressed()[pygame.K_F11]:
            self.toggle_fullscreen()
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

    def handle_transitions(self, events):
        'Scene changes occur via certain keypresses and events'
        keys = pygame.key.get_pressed()
        for (state, key), new_state in self.transitions.items():
            if isinstance(key, int):  # Key is a pygame key code
                if keys[key] and self.current_state == self.states[state]:
                    self.transition(new_state)
                    break
            elif isinstance(key, str):  # Key is a pygame event type
                for event in events:
                    if event.type == getattr(Event, key) and self.current_state == self.states[state]:
                        self.transition(new_state)
                        break


    def run(self):
        while True:
            events = pygame.event.get()
            self.handle_events(events)
            self.handle_transitions(events)
            self.update_gfx()

def main():
    state_machine = StateMachine()
    state_machine.run()

if __name__ == "__main__":
    main()
