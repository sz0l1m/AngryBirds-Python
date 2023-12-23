import pygame
import pymunk
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    floor_height
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
    """
    def __init__(self, position: tuple, radius: int, density=1, elasticity=1):
        """
        Creates instance of Bird.

        Raises ValueError if radius, density or elasticiy is negative.

        Raises CoordinatesError if coordinates are negative or are bigger than screen size.
        """
        x, y = position
        if x < 0 or y < 0 or x > SCREEN_WIDTH or y > SCREEN_HEIGHT:
            raise CoordinatesError(position)
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
