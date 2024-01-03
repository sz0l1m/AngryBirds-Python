import json
import pygame
import pymunk
import os
import collisions
from classes import (
    Bird,
    Pig,
    Bar,
    Floor,
    Trajectory,
    Text,
    convert_coords,
    is_on_circle
)
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
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


def handle_level(space: pymunk.Space, level):
    pigs = 0
    for body, shape in zip(space.bodies, space.shapes):
        if body.position[0] > SCREEN_WIDTH + 50 or body.position[0] < -50:
            if shape.collision_type == 3:
                space.remove(body, shape)
            else:
                body.position = (SCREEN_WIDTH + 50, floor_height)
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
        # level, bird, trajectory = self.load_level(self.space, 0)
        # self._level = level
        # self._bird = bird
        # self._trajectory = trajectory
        self._angle_text = Text('0', (20, 20), 30)
        self._velocity_text = Text('0', (20, 100), 30)
        pymunk.pygame_util.positive_y_is_up = True
        self._draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        collisions.create_handlers(self.space)
        self._running = True
        self._bird_shot = False
        self._bird_clicked = False

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

    def load_level(self, level_number):
        self._level = get_level(self.space, level_number)
        self._bird = self._level.bird
        self._trajectory = Trajectory(self._bird)

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_SPACE and not self.bird_shot:
                    self.bird.body.velocity = (self.bird.x_velocity, self.bird.y_velocity)
                    self.bird_shot = True
                elif event.key == K_r:
                    self.load_level(self.level.number - 1)
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if is_on_circle(bird_position, bird_radius, convert_coords(mouse_pos)):
                    self.bird_clicked = True
            elif event.type == MOUSEBUTTONUP and self.bird_clicked and not self.bird_shot and event.button == 1:
                self.bird.body.velocity = (self.bird.x_velocity, self.bird.y_velocity)
                self.bird_shot = True
                self.bird_clicked = False
            elif event.type == MOUSEBUTTONUP:
                self.bird_clicked = False
            elif event.type == QUIT:
                self.running = False


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
                bar['type'] if 'type' in bar.keys() else 'dynamic'
            )
            for bar in self._objects['bars']
        ]

    def load_bird(self, space):
        """
        Loads new bird on the screen.
        """
        self._attempts -= 1
        space.remove(self.bird.body, self.bird.shape)
        self.bird = Bird(space, bird_position, bird_radius, 0.7, 0.7, 0.8)
