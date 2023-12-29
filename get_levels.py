import json


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
