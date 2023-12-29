import json
from classes import (
    Bird,
    Pig,
    Bar,
    Floor
)
import config


def get_data():
    with open('levels.json') as fp:
        return json.load(fp)


levels_data = get_data()["levels"]


class Level:
    """
    Class Level. Contains attributes:
    :param number: number of the level
    :type number: int

    :param objects: all objects of the level
    :type objects: dict
    """
    def __init__(self, level_data: dict):
        """
        Creates instance of the level.
        """
        self._number = level_data["level"]
        self._objects = level_data["objects"]

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

    def create_objects(self, space):
        Floor(space)
        bird = Bird(space, config.bird_position, config.bird_radius)
        pigs = [
            Pig(
                space,
                (pig['x_position'], pig['y_position']),
                pig['radius']
            )
            for pig in self._objects['pigs']
            ]
        bars = [
            Bar(
                space,
                (bar['x_position'], bar['x_position']),
                (bar['x_position'], bar['x_position'])
            )
            for bar in self._objects['bars']
        ]
        return bird, pigs, bars
