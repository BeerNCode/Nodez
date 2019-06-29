import pytest
from server.map_generator import MapGenerator

def test_generate_block_map():
    mapGen = MapGenerator((512,256), 32)

    tileTypeArray = mapGen.generate_block_map(0)

    assert len(tileTypeArray) == 16
    assert len(tileTypeArray[0]) == 8
    assert all(map(lambda col: all(map(lambda val: val == 0, col)), tileTypeArray))

def test_generate_block_map_with_holes():
    mapGen = MapGenerator((512,256), 32)

    tileTypeArray = mapGen.generate_block_map(3)

    assert len(tileTypeArray) == 16
    assert len(tileTypeArray[0]) == 8
    assert any(map(lambda col: any(map(lambda val: val == -1, col)), tileTypeArray))

