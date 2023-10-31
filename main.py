import pygame
import config
import colors

pygame.init()
screen = pygame.display.set_mode(config.SCREEN_PIXEL_DIMENSIONS)
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break

    screen.fill(colors.DARK_BLUE)
    pygame.display.update()
    clock.tick(config.SCREEN_UPDATE_HERTZ)
