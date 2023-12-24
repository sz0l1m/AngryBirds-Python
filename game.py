from classes import (
    Bird,
    Floor
)
import config
import pymunk
import pygame
from pygame.locals import (
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)


def main():
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

    space_used = False

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_SPACE and not space_used:
                    bird.body.velocity = (bird.x_velocity, bird.y_velocity)
                    space_used = True
            elif event.type == QUIT:
                running = False

        pressed_keys = pygame.key.get_pressed()
        bird.set_speed(pressed_keys)

        space.step(1 / config.FPS)

        screen.fill((255, 255, 255))
        bird.draw(screen)
        floor.draw(screen)
        pygame.display.flip()

        clock.tick(config.FPS)


if __name__ == '__main__':
    main()
