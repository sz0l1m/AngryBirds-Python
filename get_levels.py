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
    Wooden_bar,
    Stone_bar,
    Floor,
    Skin,
    Trajectory,
    Text,
    convert_coords,
    is_on_circle,
    space_draw
)
from configs.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    DISPLAY_WIDTH,
    DISPLAY_HEIGHT,
    FPS,
    screen_factor,
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
        self.screen = pygame.Surface((1913, 1050))
        self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.load_level(0)
        self._texts = {
            'attempts': Text('0', (130, 70), 40),
            'info': Text(
                'Press space to start',
                (SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT - 100), 30
                )
        }
        self._images = {
            'background': Skin(None, 'background.jpg', (1914, 1029)),
            'title': Skin(None, 'title.png', (512, 295)),
            'bird_amount': Skin(None, 'red_bird.png', (80, 80))
        }
        pymunk.pygame_util.positive_y_is_up = True
        self._draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        collisions.create_handlers(self.space)
        self._running = True
        self._bird_shot = False
        self._bird_clicked = False
        self._timer = 0
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

    def load_bird(self):
        """
        Loads new bird on the screen.
        """
        if self._level.attempts > 0:
            self.space.remove(self._bird.body, self._bird.shape)
            self._bird = Bird(self.space, bird_position, bird_radius, 0.7, 0.7, 0.8)
            self._trajectory = Trajectory(self.bird)
            self._bird_shot = False

    def shoot_bird(self):
        self._bird.body.velocity = (self.bird.x_velocity, self.bird.y_velocity)
        self._bird_shot = True
        self._bird_clicked = False
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

    def scale_screen(self):
        self.frame = pygame.transform.scale(self.screen, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.display.blit(self.frame, self.frame.get_rect())
        pygame.display.flip()

    def start_screen(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self._running = False
                elif event.key == K_SPACE:
                    self._start = True
                    self.load_level(3)
            elif event.type == QUIT:
                self._running = False

        self.space.step(1 / FPS)
        self.screen.fill((255, 255, 255))
        self.screen.blit(self._images['background'].default_image, (0, -30))
        self.screen.blit(self._images['title'].default_image, (SCREEN_WIDTH / 2 - 256, 200))
        self._texts['info'].draw(self.screen)
        self.scale_screen()
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
        if pigs == 0:
            if self._level.number < self._level.amount_of_levels:
                self.load_level(self.level.number)
                self._bird_shot = False
            else:
                self.__init__()
                self.start_screen()
                self._bird_shot = False
        elif pigs != 0 and self._bird_shot:
            self.load_bird()
        if pigs != 0 and self._level.attempts == 0 and time.time() - self._timer > 1:
            self.load_level(self._level.number - 1)

    def handle_events(self, mouse_pos):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self._running = False
                elif event.key == K_SPACE and not self._bird_shot and self._bird.velocity:
                    self.shoot_bird()
                elif event.key == K_SPACE and self._bird_shot:
                    self.load_bird()
                elif event.key == K_r:
                    self.load_level(self.level.number - 1)
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if is_on_circle(bird_position, bird_radius, convert_coords(mouse_pos)):
                    self._bird_clicked = True
            elif event.type == MOUSEBUTTONUP and self.bird_clicked and not self.bird_shot and event.button == 1:
                self.shoot_bird()
                self._bird_clicked = False
            elif event.type == MOUSEBUTTONUP and event.button == 3:
                self._bird.velocity = 0
                self._bird_clicked = False
            elif event.type == QUIT:
                self._running = False

    def step(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (mouse_pos[0] / screen_factor, mouse_pos[1] / screen_factor)
        self.handle_events(mouse_pos)
        self.space.step(1 / FPS)
        self.screen.fill((255, 255, 255))
        self.screen.blit(self._images['background'].default_image, (0, -30))
        self._trajectory.calc()
        self._trajectory.draw(self.screen)
        space_draw(self.space, self._draw_options)
        self.update_skins()
        self.draw_grass()
        self.screen.blit(self._images['bird_amount'].default_image, (50, 50))
        self._texts['attempts'].set_str(self.screen, str(f'x{self._level.attempts}'))
        pressed_keys = pygame.key.get_pressed()
        if self._bird_clicked:
            self._bird.set_speed(pressed_keys, convert_coords(mouse_pos), self.screen)
        else:
            self._bird.set_speed(pressed_keys, None, None)
        collisions.rolling_resistance(self.space)
        self.handle_level()
        self.scale_screen()
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

    def create_bar(self, space, bar):
        if 'type' not in bar.keys():
            return Wooden_bar(
                space,
                (SCREEN_WIDTH - bar['x_position'], bar['y_position'] + floor_height),
                (bar['x_size'], bar['y_size'])
            )
        elif bar['type'] == 'stone':
            return Stone_bar(
                space,
                (SCREEN_WIDTH - bar['x_position'], bar['y_position'] + floor_height),
                (bar['x_size'], bar['y_size'])
            )
        else:
            return Bar(
                space,
                (SCREEN_WIDTH - bar['x_position'], bar['y_position'] + floor_height),
                (bar['x_size'], bar['y_size']),
                bar['type'] if 'type' in bar.keys() else 'dynamic',
                (110, 50, 20, 255)
            )

    def create_objects(self, space):
        """
        Creates instances of all objects and returns them.
        """
        self.floor = Floor(space)
        self.bird = Bird(
            space,
            bird_position,
            bird_radius,
            0.6,
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
            self.create_bar(space, bar)
            for bar in self._objects['bars']
        ]
