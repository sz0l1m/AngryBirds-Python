from classes import (
    CoordinatesError,
    Bird,
    Pig,
    Bar,
    Trajectory,
    Floor,
    Text,
    convert_coords,
    check_coords,
    check_radius,
    calc_distance_and_angle,
    is_on_circle
)
from config import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    floor_height
)
import pytest
import pygame
import pymunk

space = pymunk.Space()

width = SCREEN_WIDTH - 1
height = SCREEN_HEIGHT - 1


def test_bird_create_normal():
    bird = Bird(space, (width, height), 30, 2, 3)
    assert bird.body.position == (width, height)
    assert bird.radius == 30
    assert bird.shape.radius == 30
    assert bird.shape.density == 2
    assert bird.shape.elasticity == 3


def test_bird_create_default_values():
    bird = Bird(space, (width, height), 30)
    assert bird.body.position == (width, height)
    assert bird.radius == 30
    assert bird.shape.radius == 30
    assert bird.shape.density == 1
    assert bird.shape.elasticity == 1


def test_bird_create_negative_coordinates():
    with pytest.raises(CoordinatesError):
        Bird(space, (-100, height), 30, 4)


def test_bird_create_invalid_coordinates():
    with pytest.raises(CoordinatesError):
        Bird(space, (width, SCREEN_HEIGHT + 10), 30, 4)


def test_bird_create_negative_radius():
    with pytest.raises(ValueError):
        Bird(space, (width, height), -10, 4)


def test_bird_create_zero_radius():
    with pytest.raises(ValueError):
        Bird(space, (width, height), 0, 4)


def test_bird_create_negative_density():
    with pytest.raises(ValueError):
        Bird(space, (width, height), 10, -4)


def test_bird_create_negative_elasticity():
    with pytest.raises(ValueError):
        Bird(space, (width, height), 10, 4, -1)


def test_bird_set_radius():
    bird = Bird(space, (width, height), 30)
    assert bird.radius == 30
    bird.set_radius(50)
    assert bird.radius == 50


def test_bird_set_radius_negative_radius():
    bird = Bird(space, (width, height), 30)
    assert bird.radius == 30
    with pytest.raises(ValueError):
        bird.set_radius(-10)


def test_bird_set_radius_zero_radius():
    bird = Bird(space, (width, height), 30)
    assert bird.radius == 30
    with pytest.raises(ValueError):
        bird.set_radius(0)


def test_floor_create():
    floor = Floor(space)
    assert floor.shape.a == (-500, 0)
    assert floor.shape.b == (SCREEN_WIDTH + 500, 0)
    assert floor.shape.radius == floor_height
    assert floor.shape.elasticity == 0.6


def test_convert_coords():
    coords = (width, height)
    assert convert_coords(coords) == (width, SCREEN_HEIGHT - height)


def test_check_coords_valid():
    coords = (width, height)
    check_coords(coords)


def test_check_coords_negative():
    coords = (-300, height)
    with pytest.raises(CoordinatesError):
        check_coords(coords)


def test_check_coords_invalid():
    coords = (SCREEN_WIDTH + 1, height)
    with pytest.raises(CoordinatesError):
        check_coords(coords)


def test_text_create_normal():
    pygame.init()
    text = Text('WASD123', (width, height), 20, (0, 0, 255), (0, 0, 0), 'timesnewroman')
    assert text.str == 'WASD123'
    assert text.position == (width, height)
    assert text.size == 20
    assert text.color == (0, 0, 255)
    assert text.background == (0, 0, 0)
    assert text.font_type == 'timesnewroman'


def test_text_create_default_values():
    pygame.init()
    text = Text('WASD123', (width, height))
    assert text.str == 'WASD123'
    assert text.position == (width, height)
    assert text.size == 10
    assert text.color == (0, 0, 0)
    assert text.background == (255, 255, 255)


def test_text_create_empty_str():
    pygame.init()
    text = Text('', (width, height))
    assert text.str == ''
    assert text.position == (width, height)
    assert text.size == 10
    assert text.color == (0, 0, 0)
    assert text.background == (255, 255, 255)


def test_text_create_negative_position():
    pygame.init()
    with pytest.raises(CoordinatesError):
        Text('WASD123', (-100, height))


def test_text_create_invalid_position():
    pygame.init()
    with pytest.raises(CoordinatesError):
        Text('WASD123', (SCREEN_WIDTH + 100, height))


def test_text_create_invalid_size():
    pygame.init()
    with pytest.raises(ValueError):
        Text('WASD123', (width, height), -1)


def test_text_create_invalid_color():
    pygame.init()
    with pytest.raises(ValueError):
        Text('WASD123', (width, height), 1, (0, 0, 256))


def test_text_create_invalid_background():
    pygame.init()
    with pytest.raises(ValueError):
        Text('WASD123', (width, height), 1, (0, 0, 255), (-1, 0, 0))


def test_text_set_str():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    text = Text('WASD123', (width, height))
    assert text.str == 'WASD123'
    text.set_str(screen, '123')
    assert text.str == '123'


def test_text_set_str_empty():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.init()
    text = Text('WASD123', (width, height))
    assert text.str == 'WASD123'
    text.set_str(screen, '')
    assert text.str == ''


def test_text_set_position():
    pygame.init()
    text = Text('WASD123', (width, height))
    assert text.position == (width, height)
    text.set_position((0, 1))
    assert text.position == (0, 1)


def test_text_set_position_negative_position():
    pygame.init()
    text = Text('WASD123', (width, height))
    assert text.position == (width, height)
    with pytest.raises(CoordinatesError):
        text.set_position((-1, height))


def test_text_set_position_invalid_position():
    pygame.init()
    text = Text('WASD123', (width, height))
    assert text.position == (width, height)
    with pytest.raises(CoordinatesError):
        text.set_position((width, SCREEN_HEIGHT + 1))


def test_text_set_size():
    pygame.init()
    text = Text('WASD123', (width, height), 20)
    assert text.size == 20
    text.set_size(30)
    assert text.size == 30


def test_text_set_size_negative_size():
    pygame.init()
    text = Text('WASD123', (width, height), 20)
    assert text.size == 20
    with pytest.raises(ValueError):
        text.set_size(-1)


def test_text_set_size_zero_size():
    pygame.init()
    text = Text('WASD123', (width, height), 20)
    assert text.size == 20
    with pytest.raises(ValueError):
        text.set_size(0)


def test_text_set_color():
    pygame.init()
    text = Text('WASD123', (width, height))
    assert text.color == (0, 0, 0)
    text.set_color((100, 100, 255))
    assert text.color == (100, 100, 255)


def test_text_set_color_negative_color():
    pygame.init()
    text = Text('WASD123', (width, height))
    assert text.color == (0, 0, 0)
    with pytest.raises(ValueError):
        text.set_color((-1, 0, 0))


def test_text_set_color_invalid_color():
    pygame.init()
    text = Text('WASD123', (width, height))
    assert text.color == (0, 0, 0)
    with pytest.raises(ValueError):
        text.set_color((300, 0, 0))


def test_text_set_background():
    pygame.init()
    text = Text('WASD123', (width, height))
    assert text.background == (255, 255, 255)
    text.set_background((100, 100, 255))
    assert text.background == (100, 100, 255)


def test_text_set_size_negative_background():
    pygame.init()
    text = Text('WASD123', (width, height))
    assert text.background == (255, 255, 255)
    with pytest.raises(ValueError):
        text.set_background((-1, 0, 0))


def test_text_set_size_invalid_background():
    pygame.init()
    text = Text('WASD123', (width, height))
    assert text.background == (255, 255, 255)
    with pytest.raises(ValueError):
        text.set_background((300, 0, 0))


def test_text_set_font_type():
    pygame.init()
    text = Text('WASD123', (width, height))
    assert text.font_type == 'timesnewroman'
    text.set_font_type('123')
    assert text.font_type == '123'


def test_trajectory_create():
    bird = Bird(space, (width, height), 20)
    tra = Trajectory(bird)
    assert tra.x_vel == 0
    assert tra.y_vel == 0
    assert tra.start_point == [width, height]
    assert tra.vertex == [width, height]
    assert tra.a_of_pattern == 0


def test_trajectory_calc():
    bird = Bird(space, (width, height), 20)
    tra = Trajectory(bird)
    bird.x_velocity = 200
    bird.y_velocity = 300
    tra.calc()
    assert tra.x_vel == 200
    assert tra.y_vel == 300
    assert tra.start_point == [width, height]
    assert tra.vertex == [width + 120, height + 90]
    assert tra.a_of_pattern == pytest.approx(-0.00625)


def test_bar_create_normal():
    bar = Bar(space, (width, height), (10, 20), 'static', (0, 0, 0))
    assert bar.body.position == (width, height)
    assert bar.size == (10, 20)
    assert bar.shape.density == 0.7
    assert bar.shape.elasticity == 0.4
    assert bar.shape.friction == 0.6
    assert bar.body.body_type == 2


def test_bar_create_default_values():
    bar = Bar(space, (width, height), (10, 20))
    assert bar.body.position == (width, height)
    assert bar.size == (10, 20)
    assert bar.shape.color == (0, 0, 0)
    assert bar.shape.density == 0.7
    assert bar.shape.elasticity == 0.4
    assert bar.shape.friction == 0.6
    assert bar.body.body_type == 0


def test_bar_create_invalid_bor_type():
    with pytest.raises(ValueError):
        Bar(space, (width, height), (10, 20), 'asdas')


def test_bar_create_negative_position():
    with pytest.raises(CoordinatesError):
        Bar(space, (-width, height), (10, 20))


def test_bar_create_invalid_position():
    with pytest.raises(CoordinatesError):
        Bar(space, (width, height + 2), (10, 20))


def test_bar_create_negative_size_1():
    with pytest.raises(ValueError):
        Bar(space, (width, height), (-10, 20))


def test_bar_create_size_zero():
    with pytest.raises(ValueError):
        Bar(space, (width, height), (10, 0))


def test_bar_create_negative_color():
    with pytest.raises(ValueError):
        Bar(space, (width, height), (10, 20), (-1, 0, 0))


def test_bar_create_invalid_color():
    with pytest.raises(ValueError):
        Bar(space, (width, height), (10, 20), (1, 0, 256))


def test_bar_set_position():
    bar = Bar(space, (width, height), (10, 20))
    assert bar.body.position == (width, height)
    bar.set_position((0, 0))
    assert bar.body.position == (0, 0)


def test_bar_set_position_negative():
    bar = Bar(space, (width, height), (10, 20))
    assert bar.body.position == (width, height)
    with pytest.raises(CoordinatesError):
        bar.set_position((-width, 0))


def test_bar_set_position_invalid():
    bar = Bar(space, (width, height), (10, 20))
    assert bar.body.position == (width, height)
    with pytest.raises(CoordinatesError):
        bar.set_position((width, height + 2))


def test_bar_set_size():
    bar = Bar(space, (width, height), (10, 20))
    assert bar.size == (10, 20)
    bar.set_size((1, 2))
    assert bar.size == (1, 2)


def test_bar_set_size_negative():
    bar = Bar(space, (width, height), (10, 20))
    assert bar.size == (10, 20)
    with pytest.raises(ValueError):
        bar.set_size((-1, 2))


def test_bar_set_size_zero():
    bar = Bar(space, (width, height), (10, 20))
    assert bar.size == (10, 20)
    with pytest.raises(ValueError):
        bar.set_size((1, 0))


def test_bar_set_color():
    bar = Bar(space, (width, height), (10, 20))
    assert bar.shape.color == (0, 0, 0)
    bar.set_color((255, 255, 255))
    assert bar.shape.color == (255, 255, 255)


def test_bar_set_color_negative():
    bar = Bar(space, (width, height), (10, 20))
    assert bar.shape.color == (0, 0, 0)
    with pytest.raises(ValueError):
        bar.set_color((-1, 0, 0))


def test_bar_set_color_zero():
    bar = Bar(space, (width, height), (10, 20))
    assert bar.shape.color == ((0, 0, 0))
    with pytest.raises(ValueError):
        bar.set_color((256, 0, 0))


def test_pig_create_normal():
    pig = Pig(space, (width, height), 10)
    assert pig.body.position == (width, height)
    assert pig.radius == 10
    assert pig.shape.radius == 10
    assert pig.shape.density == 0.8
    assert pig.shape.elasticity == 0.7
    assert pig.shape.friction == 0.8


def test_pig_create_negative_position():
    with pytest.raises(CoordinatesError):
        Pig(space, (-width, height), 10)


def test_pig_create_invalid_position():
    with pytest.raises(CoordinatesError):
        Pig(space, (width, height + 2), 10)


def test_pig_create_negative_radius():
    with pytest.raises(ValueError):
        Pig(space, (width, height), -10)


def test_pig_create_zero_radius():
    with pytest.raises(ValueError):
        Pig(space, (width, height), 0)


def test_pig_set_position_normal():
    pig = Pig(space, (width, height), 10)
    assert pig.body.position == (width, height)
    pig.set_position((0, 0))
    assert pig.body.position == (0, 0)


def test_pig_set_position_negative_position():
    pig = Pig(space, (width, height), 10)
    assert pig.body.position == (width, height)
    with pytest.raises(CoordinatesError):
        pig.set_position((-1, 0))


def test_pig_set_position_invalid_position():
    pig = Pig(space, (width, height), 10)
    assert pig.body.position == (width, height)
    with pytest.raises(CoordinatesError):
        pig.set_position((width, height + 2))


def test_pig_set_radius_normal():
    pig = Pig(space, (width, height), 10)
    assert pig.radius == 10
    assert pig.shape.radius == 10
    pig.set_radius(1)
    assert pig.radius == 1
    assert pig.shape.radius == 1


def test_pig_set_radius_negative_radius():
    pig = Pig(space, (width, height), 10)
    assert pig.radius == 10
    assert pig.shape.radius == 10
    with pytest.raises(ValueError):
        pig.set_radius(-1)


def test_pig_set_radius_zero_radius():
    pig = Pig(space, (width, height), 10)
    assert pig.radius == 10
    assert pig.shape.radius == 10
    with pytest.raises(ValueError):
        pig.set_radius(0)


def test_calc_distance_and_angle():
    distance, angle = calc_distance_and_angle((100, 200), (50, 120))
    assert distance == pytest.approx(94.3398)
    assert angle == pytest.approx(57.9946)


def test_check_radius_valid():
    check_radius(20)


def test_check_radius_invalid():
    with pytest.raises(ValueError):
        check_radius(-20)


def test_is_on_circle_true():
    assert is_on_circle((100, 100), 30, (110, 105))


def test_is_on_circle_false():
    assert not is_on_circle((100, 100), 30, (130, 105))
