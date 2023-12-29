from classes import (
    Trajectory,
    Text,
    space_draw
)
from get_levels import Level, get_data
from config import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    FPS,
    gravity,
)
import pygame
import pymunk
import pymunk.pygame_util
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
    pygame.display.set_caption('Angry Birds')
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    data = get_data()['levels']
    level_1 = Level(data[0])
    bird = level_1.create_objects(space)[0]

    trajectory = Trajectory(bird)

    angle_text = Text('0', (20, 20), 30)
    velocity_text = Text('0', (20, 100), 30)

    pymunk.pygame_util.positive_y_is_up = True
    draw_options = pymunk.pygame_util.DrawOptions(screen)

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

        trajectory.calc()

        screen.fill((255, 255, 255))

        space_draw(space, draw_options)

        trajectory.draw(screen)

        angle_text.set_str(str(bird.angle))
        velocity_text.set_str(str(bird.velocity))
        angle_text.draw(screen)
        velocity_text.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)


if __name__ == '__main__':
    main()
