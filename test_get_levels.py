from get_levels import (
    Game,
    Level
)
from io import StringIO
import json
import pymunk
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    bird_position,
    floor_height,
    gravity
)


space = pymunk.Space()

file = """
{
    "levels": [
        {
            "level": 1,
            "objects": {
                "birds": {
                    "amount": 2
                },
                "pigs": [
                    {
                        "x_position": 800,
                        "y_position": 320,
                        "radius": 20
                    },
                    {
                        "x_position": 850,
                        "y_position": 120,
                        "radius": 30
                    }
                ],
                "bars": [
                    {
                        "x_position": 700,
                        "y_position": 200,
                        "x_size": 20,
                        "y_size": 200
                    },
                    {
                        "x_position": 900,
                        "y_position": 200,
                        "x_size": 20,
                        "y_size": 200
                    },
                    {
                        "x_position": 800,
                        "y_position": 310,
                        "x_size": 220,
                        "y_size": 20
                    }
                ]
            }
        }
    ]
}
"""
file_handle = StringIO(file)
data = json.load(file_handle)['levels']


def get_level(space: pymunk.Space, level):
    for body, shape in zip(space.bodies, space.shapes):
        space.remove(body, shape)
    level = Level(data[level], len(data))
    level.create_objects(space)
    return level


def test_game_create():
    game = Game()
    assert game.space.gravity == gravity
    assert game.screen.get_width() == SCREEN_WIDTH
    assert game.screen.get_height() == SCREEN_HEIGHT
    assert type(game.level) is Level
    assert game.level.number == 1
    assert game.bird.body.position == bird_position
    assert game.trajectory.start_point[0] == bird_position[0]
    assert game.trajectory.start_point[1] == bird_position[1]
    assert game.trajectory.bird == game.bird
    assert game.running is True
    assert game.bird_shot is False
    assert game.bird_clicked is False


def test_level_create():
    level = Level(data[0], len(data))
    assert level.number == 1
    assert level.objects['pigs'][0]['x_position'] == 800
    assert level.objects['bars'][0]['x_position'] == 700
    assert level.amount_of_levels == 1
    assert level.attempts == 2
    assert level.bird is None
    assert level.pigs is None
    assert level.bars is None
    assert level.floor is None


def test_level_create_objects_check_bird():
    level = Level(data[0], len(data))
    level.create_objects(space)
    assert level.bird.body.position == bird_position
    assert level.bird.radius == 30
    assert level.bird.shape.radius == 30
    assert level.bird.shape.density == 0.7
    assert level.bird.shape.elasticity == 0.7
    assert level.bird.shape.friction == 0.8


def test_level_create_objects_check_pig():
    level = Level(data[0], len(data))
    level.create_objects(space)
    assert level.pigs[1].body.position == (SCREEN_WIDTH - 850, 320)
    assert level.pigs[1].radius == 30
    assert level.pigs[1].shape.radius == 30
    assert level.pigs[1].shape.density == 0.8
    assert level.pigs[1].shape.elasticity == 0.7
    assert level.pigs[1].shape.friction == 0.8


def test_level_create_objects_check_bar():
    level = Level(data[0], len(data))
    level.create_objects(space)
    assert level.bars[0].body.position == (SCREEN_WIDTH - 700, 400)
    assert level.bars[0].size == (20, 200)
    assert level.bars[0].shape.color == (0, 0, 0)
    assert level.bars[0].shape.density == 0.7
    assert level.bars[0].shape.elasticity == 0.4
    assert level.bars[0].shape.friction == 0.6


def test_level_create_objects_check_floor():
    level = Level(data[0], len(data))
    level.create_objects(space)
    assert level.floor.shape.a == (-500, 0)
    assert level.floor.shape.b == (SCREEN_WIDTH + 500, 0)
    assert level.floor.shape.radius == floor_height
    assert level.floor.shape.elasticity == 0.6


def test_get_level():
    level = get_level(space, 0)
    assert level.number == 1
    assert level.objects['pigs'][0]['x_position'] == 800
    assert level.objects['bars'][0]['x_position'] == 700
    assert level.amount_of_levels == 1
    assert level.attempts == 2


def test_get_level_check_bird():
    level = get_level(space, 0)
    assert level.bird.body.position == bird_position
    assert level.bird.radius == 30
    assert level.bird.shape.radius == 30
    assert level.bird.shape.density == 0.7
    assert level.bird.shape.elasticity == 0.7
    assert level.bird.shape.friction == 0.8


def test_get_level_check_pig():
    level = get_level(space, 0)
    assert level.pigs[1].body.position == (SCREEN_WIDTH - 850, 320)
    assert level.pigs[1].radius == 30
    assert level.pigs[1].shape.radius == 30
    assert level.pigs[1].shape.density == 0.8
    assert level.pigs[1].shape.elasticity == 0.7
    assert level.pigs[1].shape.friction == 0.8


def test_get_level_check_bar():
    level = get_level(space, 0)
    assert level.bars[0].body.position == (SCREEN_WIDTH - 700, 400)
    assert level.bars[0].size == (20, 200)
    assert level.bars[0].shape.color == (0, 0, 0)
    assert level.bars[0].shape.density == 0.7
    assert level.bars[0].shape.elasticity == 0.4
    assert level.bars[0].shape.friction == 0.6


def test_get_level_check_floor():
    level = get_level(space, 0)
    assert level.floor.shape.a == (-500, 0)
    assert level.floor.shape.b == (SCREEN_WIDTH + 500, 0)
    assert level.floor.shape.radius == floor_height
    assert level.floor.shape.elasticity == 0.6
