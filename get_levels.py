import json
from classes import (
    Bird,
    Pig,
    Bar,
    Floor
)
from config import (
    bird_position,
    bird_radius
)


def get_data():
    """
    Returns data from the file.
    """
    with open('levels.json') as fp:
        return json.load(fp)


def load_level(space, level):
    """
    Creates instance of Level and calls create objects method.
    """
    level = Level(get_data()['levels'][level])
    return level.create_objects(space)


class Level:
    """
    Class Level. Contains attributes:
    :param number: number of the level
    :type number: int

    :param objects: all objects of the level
    :type objects: dict

    :param attempts: attempts of the level
    :type attempts: int

    :param bird: currently used bird
    :type bird: Bird

    :param pigs: all pigs of the level
    :type pigs: list

    :param bars: all bars of the level
    :type bars: list

    :param floor: floor of the level
    :type floor: Floor
    """
    def __init__(self, level_data: dict):
        """
        Creates instance of the level.
        """
        self._number = level_data["level"]
        self._objects = level_data["objects"]
        self._attempts = self._objects["birds"]["amount"]
        self.bird = None
        self.pigs = None
        self.bars = None
        self.floor = None

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
        """
        Creates instances of all objects and returns them.
        """
        floor = Floor(space)
        bird = Bird(
            space,
            bird_position,
            bird_radius,
            0.7,
            0.7,
            0.8
        )
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
                (bar['x_position'], bar['y_position']),
                (bar['x_size'], bar['y_size'])
            )
            for bar in self._objects['bars']
        ]
        return self._attempts, bird, pigs, bars, floor

    def load_bird(self, space, bird: Bird):
        """
        Loads new bird on the screen.
        """
        self._attempts
        space.remove(bird.body, bird.shape)
        return Bird(space, bird_position, bird_radius, 0.7, 0.7, 0.8)
