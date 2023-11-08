import sys
import pygame


class Scene:
    def __init__(self):
        self.fullscreen = False
    def handle_events(self, events):
        pass

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        print(f'{self.fullscreen}')

class Menu(Scene):
    def handle_events(self, events):
        self.key_actions = {
            pygame.K_F11: 'toggle_fullscreen',
            pygame.K_ESCAPE: 'quit',
        }
        for event in events:
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                action = self.key_actions.get(event.key)
                if action is not None:
                    if action == 'quit':
                        self.quit()
                    elif action == 'toggle_fullscreen':
                        self.toggle_fullscreen()

    def quit(self):
        print('Quiting')
        sys.exit()

class Game(Scene):
    def __init__(self):
        super().__init__()

    def handle_events(self, events):
        self.key_actions = {
            pygame.K_DOWN: (0, 1, 0),
            pygame.K_UP: (0, -1, 0),
            pygame.K_RIGHT: (1, 0, 0),
            pygame.K_LEFT: (-1, 0, 0),
            pygame.K_LSHIFT: (0, 0, 1),
            pygame.K_c: 'clear',
            pygame.K_F11: 'toggle_fullscreen',
        }
        for event in events:
            if event.type == pygame.KEYDOWN:
                action = self.key_actions.get(event.key)
                if action is not None:
                    if action == 'clear':
                        print(action)
                    else:
                        dx, dy, drotate = action
                        print(action)

class Pause(Scene):
    def handle_events(self, events):
        pass

class StateMachine:
    def __init__(self):
        self.states = {"Menu": Menu(), "Game": Game(), "Pause": Pause()}
        self.current_state = self.states["Menu"]

    def transition(self, new_state):
        self.current_state = self.states[new_state]
        print(f'{self.current_state} -> {self.states[new_state]}')

    def handle_events(self, events):
        self.current_state.handle_events(events)

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((320, 240), pygame.NOFRAME)# pygame.FULLSCREEN)
    state_machine = StateMachine()

    while True:
        events = pygame.event.get()
        state_machine.handle_events(events)

        # Transition between states based on some condition
        if isinstance(state_machine.current_state, Menu) and pygame.key.get_pressed()[pygame.K_LSHIFT]:
            state_machine.transition("Game")
        elif isinstance(state_machine.current_state, Game) and pygame.key.get_pressed()[pygame.K_p]:
            state_machine.transition("Pause")
        elif isinstance(state_machine.current_state, Pause) and pygame.key.get_pressed()[pygame.K_p]:
            state_machine.transition("Game")
        elif isinstance(state_machine.current_state, Game) and pygame.key.get_pressed()[pygame.K_ESCAPE]:
            state_machine.transition("Menu")
if __name__ == "__main__":
    main()
