from classes import (
    Bird,
    Floor
)
import config
import pymunk
import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

space = pymunk.Space()
space.gravity = config.gravity

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

bird = Bird(config.bird_position, 30)
space.add(bird.body, bird.shape)

floor = Floor()
space.add(floor.body, floor.shape)

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    space.step(1 / config.FPS)

    screen.fill((255, 255, 255))
    bird.draw(screen)
    floor.draw(screen)
    pygame.display.flip()

    clock.tick(config.FPS)
