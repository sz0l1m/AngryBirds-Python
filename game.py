import config
import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


pygame.init()
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    screen.fill((255, 255, 255))
    pygame.display.flip()
