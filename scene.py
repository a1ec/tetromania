import pygame

class Scene:

    fullscreen = False

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        print(f'{self.fullscreen}')

    def handle_events(self, events):
        pass

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
        print('Quitting')
        raise SystemExit

class Game(Scene):

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
