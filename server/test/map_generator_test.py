import pytest
from server.map_generator import MapGenerator

def test_generate_block_map():
    mapGen = MapGenerator((512,256), 32)

    tileTypeArray = mapGen.generate_block_map(0)

    print(tileTypeArray)

    assert tileTypeArray.count == 16
    assert tileTypeArray[0].count == 8
    assert all(lambda col: all(lambda val: val == 0, col), tileTypeArray)