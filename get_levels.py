import json
import pygame
import pymunk
import os
import collisions
import time
from classes import (
    Bird,
    Pig,
    Bar,
    Floor,
    Skin,
    Trajectory,
    Text,
    convert_coords,
    is_on_circle,
    space_draw
)
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    bird_position,
    bird_radius,
    floor_height,
    gravity
)
from pygame.locals import (
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    QUIT,
    K_r
)


def get_data():
    """
    Returns data from the file.
    """
    with open('levels.json') as fp:
        return json.load(fp)


def get_level(space: pymunk.Space, level):
    """
    Creates instance of Level and calls create_objects method.
    """
    for body, shape in zip(space.bodies, space.shapes):
        space.remove(body, shape)
    data = get_data()
    level = Level(data['levels'][level], len(data['levels']))
    level.create_objects(space)
    return level


class Game:
    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = gravity
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
        pygame.init()
        pygame.display.set_caption('Angry Birds')
        self._clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.load_level(0)
        self._angle_text = Text('0', (20, 20), 30)
        self._velocity_text = Text('0', (20, 100), 30)
        pymunk.pygame_util.positive_y_is_up = True
        self._draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        collisions.create_handlers(self.space)
        self._running = True
        self._bird_shot = False
        self._bird_clicked = False
        self._timer = 0
        self._background = Skin(None, 'background.jpg', (2131, 1146))
        self._start = False

    @property
    def level(self):
        """
        Returns current level of the game.
        """
        return self._level

    @property
    def bird(self):
        """
        Returns currently used bird.
        """
        return self._bird

    @property
    def trajectory(self):
        """
        Returns current trajectory of the bird.
        """
        return self._trajectory

    @property
    def running(self):
        """
        Returns True if the game is running.
        """
        return self._running

    @property
    def bird_shot(self):
        """
        Returns True if bird was shot in current attempt.
        """
        return self._bird_shot

    @property
    def bird_clicked(self):
        """
        Returns True if bird was clicked with LMP and was not released.
        """
        return self._bird_clicked

    @property
    def start(self):
        """
        Returns True if game should be started.
        """
        return self._start

    def load_level(self, level_number):
        self._level = get_level(self.space, level_number)
        self._bird = self._level.bird
        self._trajectory = Trajectory(self._bird)

    def start_screen(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self._running = False
                elif event.key == K_SPACE:
                    self._start = True
            elif event.type == QUIT:
                self._running = False

        self.space.step(1 / FPS)
        self.screen.fill((255, 255, 255))
        self.screen.blit(self._background.default_image, (0, 0))
        pygame.display.flip()
        self._clock.tick(FPS)

    def handle_level(self):
        pigs = 0
        for body, shape in zip(self.space.bodies, self.space.shapes):
            if body.position[0] > SCREEN_WIDTH + 50 or body.position[0] < -50:
                if shape.collision_type == 3:
                    self.space.remove(body, shape)
                else:
                    body.position = (SCREEN_WIDTH + 50, floor_height)
                    body.velocity = (0, 0)
            if round(body.velocity[0]) != 0 or round(body.velocity[1]) != 0:
                self._timer = 0
                return None
            if shape.collision_type == 3:
                pigs += 1
        if self._timer == 0:
            self._timer = time.time()
        if pigs == 0 and self._level.number < self._level.amount_of_levels:
            self.load_level(self.level.number)
            self._bird_shot = False
        elif pigs != 0 and self._level.attempts >= 1:
            if self._bird_shot:
                self._level.load_bird(self.space)
                self._bird = self.level.bird
                self._trajectory = Trajectory(self.bird)
                self._bird_shot = False
        elif pigs != 0 and self._level.attempts == 0 and time.time() - self._timer > 1:
            self.load_level(self._level.number - 1)

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self._running = False
                elif event.key == K_SPACE and not self._bird_shot:
                    self.shoot_bird()
                elif event.key == K_r:
                    self.load_level(self.level.number - 1)
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if is_on_circle(bird_position, bird_radius, convert_coords(mouse_pos)):
                    self._bird_clicked = True
            elif event.type == MOUSEBUTTONUP and self.bird_clicked and not self.bird_shot and event.button == 1:
                self.shoot_bird()
                self._bird_clicked = False
            elif event.type == MOUSEBUTTONUP:
                self._bird_clicked = False
            elif event.type == QUIT:
                self._running = False

    def shoot_bird(self):
        self._bird.body.velocity = (self.bird.x_velocity, self.bird.y_velocity)
        self._bird_shot = True
        self._level.reduce_attempts()

    def update_skins(self):
        for body, shape in zip(self.space.bodies, self.space.shapes):
            if shape.collision_type == 1 or shape.collision_type == 3:
                body.skin.update(self.screen)

    def draw_grass(self):
        for x in range(SCREEN_WIDTH + 310 // 300):
            self.screen.blit(
                self._level.floor.body.grass.default_image,
                convert_coords((-10 + 300 * x, floor_height + 20))
                )

    def step(self):
        self.handle_events()
        mouse_pos = pygame.mouse.get_pos()
        self.space.step(1 / FPS)
        self.screen.fill((255, 255, 255))
        self.screen.blit(self._background.default_image, (0, -7))
        self._trajectory.calc()
        self._trajectory.draw(self.screen)
        space_draw(self.space, self._draw_options)
        self.update_skins()
        self.draw_grass()
        pressed_keys = pygame.key.get_pressed()
        if self._bird_clicked:
            self._bird.set_speed(pressed_keys, convert_coords(mouse_pos), self.screen)
        else:
            self._bird.set_speed(pressed_keys, None, None)
        self._angle_text.set_str(self.screen, str(self._level.attempts))
        # self._angle_text.set_str(self.screen, str(self._bird.angle))
        self._velocity_text.set_str(self.screen, str(self._bird.velocity))
        collisions.rolling_resistance(self.space)
        self.handle_level()
        pygame.display.flip()
        self._clock.tick(FPS)


class Level:
    """
    Class Level. Contains attributes:
    :param number: number of the level
    :type number: int

    :param objects: all objects of the level
    :type objects: dict

    :param attempts: attempts of the level
    :type attempts: int

    :param bird: currently used bird
    :type bird: Bird

    :param pigs: all pigs of the level
    :type pigs: list

    :param bars: all bars of the level
    :type bars: list

    :param floor: floor of the level
    :type floor: Floor
    """
    def __init__(self, level_data: dict, amount_of_levels):
        """
        Creates instance of the level.
        """
        self._number = level_data["level"]
        self._objects = level_data["objects"]
        self._amount_of_levels = amount_of_levels
        self._attempts = self._objects["birds"]["amount"]
        self.bird = None
        self.pigs = None
        self.bars = None
        self.floor = None

    @property
    def number(self):
        """
        Returns number of the level.
        """
        return self._number

    @property
    def objects(self):
        """
        Returns objects of the level.
        """
        return self._objects

    @property
    def amount_of_levels(self):
        """
        Returns total amount of levels in the game.
        """
        return self._amount_of_levels

    @property
    def attempts(self):
        """
        Returns total attempts of the level.
        """
        return self._attempts

    def reduce_attempts(self):
        self._attempts -= 1

    def create_objects(self, space):
        """
        Creates instances of all objects and returns them.
        """
        self.floor = Floor(space)
        self.bird = Bird(
            space,
            bird_position,
            bird_radius,
            0.7,
            0.7,
            0.8
        )
        self.pigs = [
            Pig(
                space,
                (SCREEN_WIDTH - pig['x_position'], pig['y_position'] + floor_height),
                pig['radius']
            )
            for pig in self._objects['pigs']
            ]
        self.bars = [
            Bar(
                space,
                (SCREEN_WIDTH - bar['x_position'], bar['y_position'] + floor_height),
                (bar['x_size'], bar['y_size']),
                bar['type'] if 'type' in bar.keys() else 'dynamic',
                (110, 50, 20, 255)
            )
            for bar in self._objects['bars']
        ]

    def load_bird(self, space):
        """
        Loads new bird on the screen.
        """
        space.remove(self.bird.body, self.bird.shape)
        self.bird = Bird(space, bird_position, bird_radius, 0.7, 0.7, 0.8)
