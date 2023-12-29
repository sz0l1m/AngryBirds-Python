from get_levels import (
    Level,
    get_data
)


data = get_data()['levels']


def test_level_create():
    level = Level(data[0])
    assert level.number == 1
    assert level.objects['pigs'][0]['x_position'] == 800
    assert level.objects['bars'][0]['x_position'] == 700
