from classes import (
    CoordinatesError,
    Bird,
    Floor
)
from config import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    floor_height
)
import pytest


def test_bird_create_normal():
    bird = Bird((100, 500), 30, 2, 3)
    assert bird.body.position == (100, 500)
    assert bird.radius == 30
    assert bird.shape.density == 2
    assert bird.shape.elasticity == 3


def test_bird_create_default_values():
    bird = Bird((100, 500), 30)
    assert bird.body.position == (100, 500)
    assert bird.radius == 30
    assert bird.shape.density == 1
    assert bird.shape.elasticity == 1


def test_bird_create_negative_coordinates():
    with pytest.raises(CoordinatesError):
        Bird((-100, 500), 30, 4)


def test_bird_create_invalid_coordinates():
    with pytest.raises(CoordinatesError):
        Bird((100, SCREEN_HEIGHT + 10), 30, 4)


def test_bird_create_negative_radius():
    with pytest.raises(ValueError):
        Bird((100, 500), -10, 4)


def test_bird_create_negative_density():
    with pytest.raises(ValueError):
        Bird((100, 500), 10, -4)


def test_bird_create_negative_elasticity():
    with pytest.raises(ValueError):
        Bird((100, 500), 10, 4, -1)


def test_bird_set_radius():
    bird = Bird((100, 500), 30)
    assert bird.radius == 30
    bird.set_radius(50)
    assert bird.radius == 50


def test_bird_set_radius_negative_radius():
    bird = Bird((100, 500), 30)
    assert bird.radius == 30
    with pytest.raises(ValueError):
        bird.set_radius(-10)


def test_floor_create():
    floor = Floor()
    assert floor.shape.a == (0, 0)
    assert floor.shape.b == (SCREEN_WIDTH, 0)
    assert floor.shape.radius == floor_height
    assert floor.shape.elasticity == 0.5
