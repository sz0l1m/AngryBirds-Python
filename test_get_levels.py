from get_levels import (
    Level
)
from classes import (
    Bird,
    Pig,
    Bar,
    Floor
)
from io import StringIO
import json
import pymunk
import config


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


def test_level_create():
    level = Level(data[0])
    assert level.number == 1
    assert level.objects['pigs'][0]['x_position'] == 800
    assert level.objects['bars'][0]['x_position'] == 700


def test_level_create_objects_check_bird():
    level = Level(data[0])
    bird = level.create_objects(space)[0]
    assert bird.body.position == (100, 130)
    assert bird.radius == 30
    assert bird.shape.radius == 30
    assert bird.shape.density == 1
    assert bird.shape.elasticity == 1
    assert bird.shape.friction == 0


def test_level_create_objects_check_pig():
    level = Level(data[0])
    pig = level.create_objects(space)[1][1]
    assert pig.body.position == (850, 120)
    assert pig.radius == 30
    assert pig.shape.radius == 30
    assert pig.shape.density == 0.8
    assert pig.shape.elasticity == 0.7
    assert pig.shape.friction == 0.8


def test_level_create_objects_check_bar():
    level = Level(data[0])
    bar = level.create_objects(space)[2][0]
    assert bar.body.position == (700, 200)
    assert bar.size == (20, 200)
    assert bar.shape.color == (0, 0, 0)
    assert bar.shape.density == 0.7
    assert bar.shape.elasticity == 0.4
    assert bar.shape.friction == 0.6


def test_level_create_objects_check_floor():
    level = Level(data[0])
    floor = level.create_objects(space)[3]
    assert floor.shape.a == (0, 0)
    assert floor.shape.b == (config.SCREEN_WIDTH, 0)
    assert floor.shape.radius == config.floor_height
    assert floor.shape.elasticity == 0.6
