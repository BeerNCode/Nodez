from server.map_generator import MapGenerator

def test_generation():
    mapGen = MapGenerator((512,256), 32)

    tileTypeArray = mapGen.generate(3)

    assert tileTypeArray.count == 16
    assert tileTypeArray[0].count == 8
