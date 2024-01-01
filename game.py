from classes import (
    Trajectory,
    Text,
    space_draw,
    convert_coords
)
from get_levels import Level, get_level
from config import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    FPS,
    gravity
)
import pygame
import pymunk
import pymunk.pygame_util
from pygame.locals import (
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    QUIT,
    K_r,
)
import collisions


def handle_level(space: pymunk.Space, level: Level):
    pigs = 0
    for body, shape in zip(space.bodies, space.shapes):
        if body.position[0] > SCREEN_WIDTH + 50 or body.position[0] < -50:
            if shape.collision_type == 3:
                space.remove(body, shape)
            else:
                body.position = (SCREEN_WIDTH + 50, 100)
                body.velocity = (0, 0)
        if round(body.velocity[0]) != 0 or round(body.velocity[1]) != 0:
            return None
        if shape.collision_type == 3:
            pigs += 1
    if pigs == 0 and level.number < level.amount_of_levels:
        return 'Next level'
    elif pigs != 0 and level.attempts > 1:
        return 'Next attempt'
    elif pigs != 0 and level.attempts == 1:
        return 'Restart'


def load_level(space, level_number):
    level = get_level(space, level_number)
    bird = level.bird
    trajectory = Trajectory(bird)
    return level, bird, trajectory


def is_on_circle(circle_position, radius, position):
    a, b = circle_position
    x, y = convert_coords(position)
    if round((x - a)**2 + (y - b)**2) <= round(radius ** 2):
        return True
    return False


def main():
    space = pymunk.Space()
    space.gravity = gravity

    pygame.init()
    pygame.display.set_caption('Angry Birds')
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    level, bird, trajectory = load_level(space, 0)

    angle_text = Text('0', (20, 20), 30)
    velocity_text = Text('0', (20, 100), 30)

    pymunk.pygame_util.positive_y_is_up = True
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    collisions.create_handlers(space)

    running = True

    space_used = False

    bird_clicked = False

    last_mouse_pos = None

    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_SPACE and not space_used:
                    bird.body.velocity = (bird.x_velocity, bird.y_velocity)
                    space_used = True
                elif event.key == K_r:
                    level, bird, trajectory = load_level(space, level.number - 1)
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if is_on_circle(bird.body.position, bird.radius, mouse_pos):
                    bird_clicked = True
            elif event.type == MOUSEBUTTONUP and bird_clicked and not space_used and event.button == 1:
                bird.body.velocity = (bird.x_velocity, bird.y_velocity)
                space_used = True
                bird_clicked = False
            elif event.type == MOUSEBUTTONUP:
                bird_clicked = False
            elif event.type == QUIT:
                running = False

        space.step(1 / FPS)

        screen.fill((255, 255, 255))

        trajectory.calc()

        trajectory.draw(screen)

        space_draw(space, draw_options)

        pressed_keys = pygame.key.get_pressed()
        if bird_clicked:
            # pygame.draw.line(screen, (0, 0, 0), convert_coords(mouse_pos), convert_coords(bird_position))
            last_mouse_pos = bird.set_speed(pressed_keys, convert_coords(mouse_pos), screen, last_mouse_pos)
        else:
            bird.set_speed(pressed_keys, None, None, None)

        angle_text.set_str(str(bird.angle))
        velocity_text.set_str(str(bird.velocity))
        angle_text.draw(screen)
        velocity_text.draw(screen)

        collisions.rolling_resistance(space)

        if space_used:
            match handle_level(space, level):
                case 'Next level':
                    level, bird, trajectory = load_level(space, level.number)
                    space_used = False
                case 'Next attempt':
                    level.load_bird(space)
                    bird = level.bird
                    trajectory = Trajectory(bird)
                    space_used = False
                case 'Restart':
                    level, bird, trajectory = load_level(space, 0)
                    space_used = False

        pygame.display.flip()

        clock.tick(FPS)


if __name__ == '__main__':
    main()
