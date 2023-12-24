import pygame
import pymunk
from math import sin, cos, radians
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    floor_height
)
from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)


def convert_coords(coords):
    """
    Converts coordinates in such a way that it moves horizontal axis
    from the bottom of display to the top or vice versa.
    Vertical axis stays the same and it is located on the left of the diplay.
    The function is needed because pygame has its horizontal axis at the top of diplay,
    while pymunk on the bottom.
    """
    x, y = coords
    return (x, SCREEN_HEIGHT - y)


def check_coords(coords):
    """
    If given coordinates are invalid raises CoordinatesError.
    Coordinates are invlaid when one of them is negative
    or is bigger than screen size.
    """
    x, y = coords
    if x < 0 or y < 0 or x > SCREEN_WIDTH or y > SCREEN_HEIGHT:
        raise CoordinatesError(coords)


class CoordinatesError(Exception):
    def __init__(self, coords):
        super().__init__('Invalid coordinates')
        self.coordinates = coords


class Bird:
    """
    Class Bird. Contains attributes:
    :param body: pymunk body of the bird
    :type body: pymunk.body.Body

    :param shape: pymunk shape of the bird
    :type body: pymunk.shapes.Circle

    :param radius: radius of the bird
    :type radius: int

    :param velocity: initial velocity of the bird set by set_speed method
    :type radius: int

    :param angle: initial angle of the bird trajectory set by set_speed method
    :type radius: int

    :param x_velocity: initial x_velocity of the bird set by set_speed method
    :type x_velocity: int

    :param x_velocity: initial y_velocity of the bird set by set_speed method
    :type x_velocity: int
    """
    def __init__(self, position: tuple, radius: int, density=1, elasticity=1):
        """
        Creates instance of Bird.

        Raises ValueError if radius, density or elasticiy is negative.

        Raises CoordinatesError if coordinates are negative or are bigger than screen size.
        """
        check_coords(position)
        if radius < 0:
            raise ValueError('Radius cannot be negative')
        if density < 0:
            raise ValueError('Density cannot be negative')
        if elasticity < 0:
            raise ValueError('Elasticity cannot be negative')
        self.body = pymunk.Body()
        self.body.position = position
        self._shape = pymunk.Circle(self.body, radius)
        self._shape.density = density
        self._shape.elasticity = elasticity
        self._radius = radius
        self.velocity = 0
        self.angle = 0
        self.x_velocity = 0
        self.y_velocity = 0
        self.body.velocity = (self.x_velocity, self.y_velocity)

    @property
    def shape(self):
        """
        Returns shape of the bird
        """
        return self._shape

    @property
    def radius(self):
        """
        Returns radius of the bird
        """
        return self._radius

    def set_radius(self, new_radius):
        """
        Changes radius of the bird to new_radius
        """
        if new_radius < 0:
            raise ValueError('Radius cannot be negative')
        self._radius = new_radius

    def draw(self, screen):
        """
        Draws bird on pygame display
        """
        pygame.draw.circle(screen, (0, 0, 0), convert_coords(self.body.position), self._radius)

    def set_speed(self, pressed_keys):
        """
        Sets speed of the bird depending on what key has been pressed.
        """
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            if self.angle < 90:
                self.angle += 1
        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            if self.angle > 0:
                self.angle -= 1
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.velocity += 10
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            if self.velocity > 10:
                self.velocity -= 10
            else:
                self.velocity = 0
        self.x_velocity = int(self.velocity * cos(radians(self.angle)))
        self.y_velocity = int(self.velocity * sin(radians(self.angle)))

    # def set_speed(self, pressed_keys):
    #     """
    #     Sets speed of the bird depending on what key has been pressed.
    #     """
    #     if pressed_keys[K_UP] or pressed_keys[K_w]:
    #         self.y_velocity += 10
    #     if pressed_keys[K_DOWN] or pressed_keys[K_s]:
    #         if self.y_velocity > 10:
    #             self.y_velocity -= 10
    #         else:
    #             self.y_velocity = 0
    #     if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
    #         self.x_velocity += 10
    #     if pressed_keys[K_LEFT] or pressed_keys[K_a]:
    #         if self.x_velocity > 10:
    #             self.x_velocity -= 10
    #         else:
    #             self.x_velocity = 0


class Floor:
    """
    Class Floor. Contains attributes:
    :param body: pymunk body of the floor
    :type body: pymunk.body.Body

    :param shape: pymunk shape of the floor
    :type body: pymunk.shapes.Segment
    """
    def __init__(self):
        """
        Creates instance of Floor.
        """
        self._body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self._shape = pymunk.Segment(
            body=self._body,
            a=(0, 0),
            b=(SCREEN_WIDTH, 0),
            radius=floor_height)
        self._shape.elasticity = 0.5

    @property
    def body(self):
        """
        Returns body of the floor
        """
        return self._body

    @property
    def shape(self):
        """
        Returns shape of the floor
        """
        return self._shape

    def draw(self, screen):
        """
        Draws floor on pygame display
        """
        pygame.draw.line(
            surface=screen,
            color=(0, 0, 0),
            start_pos=convert_coords((0, floor_height)),
            end_pos=convert_coords((SCREEN_WIDTH, floor_height)),
            width=6
        )


class Text:
    """
    Class Text. Contains attributes:
    :param str: content of the text
    :type str: str

    :param position: position of the text
    :type position: tuple

    :param size: font size of the text
    :type size: int

    :param color: color of the text's symbols
    :type color: tuple

    :param background: background color of the text
    :type background: tuple

    :param font_type: system's font of the text
    :type font: str

    :param font: pygame font object, contains font_type and size
    :type font: pygame.font.SysFont
    """
    def __init__(
            self,
            str: str,
            position: tuple,
            size=10,
            color=(0, 0, 0),
            background=(255, 255, 255),
            font='timesnewroman'
    ):
        check_coords(position)
        if size <= 0:
            raise ValueError('Size has to be positive')
        self._str = str
        self._position = position
        self._size = size
        self._color = color
        self._background = background
        self._font_type = font
        self._font = pygame.font.SysFont(self._font_type, self._size)
        self._surf = self._font.render(self._str, True, self._color, self._background)

    @property
    def str(self):
        """
        Returns str of the text
        """
        return self._str

    @property
    def position(self):
        """
        Returns position of the text
        """
        return self._position

    @property
    def size(self):
        """
        Returns size of the text
        """
        return self._size

    @property
    def color(self):
        """
        Returns color of the text
        """
        return self._color

    @property
    def background(self):
        """
        Returns background of the text
        """
        return self._background

    @property
    def font_type(self):
        """
        Returns font_type of the text
        """
        return self._font_type

    def set_str(self, new_str):
        """
        Changes str of the text to new_str
        """
        self._str = new_str
        self._surf = self._font.render(self._str, True, self._color, self._background)

    def set_position(self, new_position):
        """
        Changes position of the text to new_position
        """
        check_coords(new_position)
        self._position = new_position

    def set_size(self, new_size):
        """
        Changes size of the text to new_size
        """
        if new_size <= 0:
            raise ValueError('Size has to be positive')
        self._size = new_size
        self._font = pygame.font.SysFont(self._font_type, self._size)
        self._surf = self._font.render(self._str, True, self._color, self._background)

    def set_color(self, new_color):
        """
        Changes color of the text to new_color
        """
        self._color = new_color
        self._surf = self._font.render(self._str, True, self._color, self._background)

    def set_background(self, new_background):
        """
        Changes background of the text to new_background
        """
        self._background = new_background
        self._surf = self._font.render(self._str, True, self._color, self._background)

    def set_font_type(self, new_font_type):
        """
        Changes font_type of the text to new_font_type
        """
        self._font_type = new_font_type
        self._font = pygame.font.SysFont(self._font_type, self._size)
        self._surf = self._font.render(self._str, True, self._color, self._background)

    def draw(self, screen):
        """
        Draws text on pygame display
        """
        screen.blit(self._surf, self._position)
