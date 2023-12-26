from classes import (
    Bird,
    Floor,
    Text
)
from config import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    FPS,
    gravity,
    bird_position,
    bird_radius
)
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
    space.gravity = gravity

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    bird = Bird(bird_position, bird_radius)
    space.add(bird.body, bird.shape)

    floor = Floor()
    space.add(floor.body, floor.shape)

    angle_text = Text('0', (20, 20), 30)
    velocity_text = Text('0', (20, 100), 30)

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

        space.step(1 / FPS)

        screen.fill((255, 255, 255))
        bird.draw(screen)
        floor.draw(screen)

        angle_text.set_str(str(bird.angle))
        velocity_text.set_str(str(bird.velocity))
        angle_text.draw(screen)
        velocity_text.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)


if __name__ == '__main__':
    main()
