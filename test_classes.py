from classes import (
    CoordinatesError,
    Bird,
    Floor,
    Text,
    convert_coords
)
from config import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    floor_height
)
import pytest
import pygame


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


def test_convert_coordinates():
    coords = (300, 100)
    assert convert_coords(coords) == (300, SCREEN_HEIGHT - coords[1])


def test_text_create_normal():
    pygame.init()
    text = Text('WASD123', (100, 200), 20, (0, 0, 255), (0, 0, 0), 'timesnewroman')
    assert text.str == 'WASD123'
    assert text.position == (100, 200)
    assert text.size == 20
    assert text.color == (0, 0, 255)
    assert text.background == (0, 0, 0)


def test_text_create_default_values():
    pygame.init()
    text = Text('WASD123', (100, 200))
    assert text.str == 'WASD123'
    assert text.position == (100, 200)
    assert text.size == 10
    assert text.color == (0, 0, 0)
    assert text.background == (255, 255, 255)
