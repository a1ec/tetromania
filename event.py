import pygame

class Event:
    GRAVITY = pygame.USEREVENT + 1
    GAME_OVER = pygame.USEREVENT + 2
    gravity = pygame.event.Event(GRAVITY)
    game_over = pygame.event.Event(GAME_OVER)
