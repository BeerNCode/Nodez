import pygame
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
        [HIGH_NOISE,SOURCE_TILE,OPEN_TILE],
        [OPEN_TILE,OPEN_TILE,HIGH_NOISE],
        [SOURCE_TILE,OPEN_TILE,OPEN_TILE]
        ]
    height = 4
    width = 3

    def show(self,screen):
        for row in range(self.height): 
            for col in range(self.width):
                pygame.draw.rect(screen,COLOURS[self.tilemap[row][col]],(col*self.tilesize,row*self.tilesize,self.tilesize,self.tilesize))
    