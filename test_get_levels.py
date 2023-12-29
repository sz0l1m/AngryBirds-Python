from get_levels import (
    Level
)
from io import StringIO
import json


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
