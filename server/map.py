
OPEN_TILE = 0
HIGH_NOISE = 1
SOURCE_TILE = 2
SINK_TILE = 3
BLACK = (0,0,0)
BROWN = (153,76,0)
GREEN = (30,255,30)
BLUE = (30,40,255)
RED = (255,40,55)
COLOURS = {
        OPEN_TILE : BLACK,
        HIGH_NOISE : RED,
        SOURCE_TILE : GREEN,
        SINK_TILE : BLUE
    }
TILESIZE = 40

class Map:
    tilesize = TILESIZE
    tilemap = [
        [OPEN_TILE,OPEN_TILE,OPEN_TILE],
        [OPEN_TILE,OPEN_TILE,OPEN_TILE],
        [OPEN_TILE,OPEN_TILE,OPEN_TILE],
        [OPEN_TILE,OPEN_TILE,OPEN_TILE]
        ]
    height = 4
    width = 3
    