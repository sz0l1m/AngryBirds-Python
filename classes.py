import pygame
import pymunk
import config


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
        x, y = position
        if x < 0 or y < 0 or x > config.SCREEN_WIDTH or y > config.SCREEN_HEIGHT:
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
        x, y = self.body.position
        pygame.draw.circle(screen, (0, 0, 0), (x, config.SCREEN_HEIGHT - y), self._radius)
