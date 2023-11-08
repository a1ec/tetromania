import pygame

class Event:
    ENACT_GRAVITY = pygame.USEREVENT + 1
    HIT_WALL = pygame.USEREVENT + 2
    BLOCK_FIXED = pygame.USEREVENT + 3
    GAME_OVER = pygame.USEREVENT + 4
    HIT_BLOCK = pygame.USEREVENT + 5
    GRAVITY = pygame.USEREVENT + 6
    hit_wall = pygame.event.Event(HIT_WALL, message='Donk!')
    block_fixed = pygame.event.Event(BLOCK_FIXED)
    game_over = pygame.event.Event(GAME_OVER)
    gravity = pygame.event.Event(GRAVITY)
