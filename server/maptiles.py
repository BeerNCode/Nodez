import pygame
import spritesheet
from tile import Tile
OPEN_TILE = 0
HIGH_NOISE = 1
SOURCE_TILE = 2
SINK_TILE = 3
BLACK = (30,30,30)
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
TILESIZE = 32

class MapTiles:
    def __init__(self):
        self.tilesize = TILESIZE
        grass_img = pygame.image.load('server\\resources\\grass-200.png')
        grass_inv_img = pygame.image.load('server\\resources\\grass-inv-200.png')
        ss = spritesheet.spritesheet('server\\resources\\dungeon_tiles.png')
        topLeft = ss.image_at((32, 32, 64, 64))
        sideLeft = ss.image_at((32, 64, 64, 96))
        bottomLeft = ss.image_at((32, 96, 64, 128))
        self.tilemap = [
            [topLeft,topLeft,topLeft],
            [sideLeft,sideLeft,sideLeft],
            [bottomLeft,bottomLeft,bottomLeft]
            ]
        self.height = 3
        self.width = 3
    
    def show(self,screen):
        
        for row in range(self.height): 
            for col in range(self.width):
                screen.blit(self.tilemap[row][col], (col*self.tilesize,row*self.tilesize,self.tilesize,self.tilesize))
                #Tile((col*self.tilesize,row*self.tilesize,self.tilesize,self.tilesize))
                #pygame.draw.rect(screen,COLOURS[self.tilemap[row][col]],(col*self.tilesize,row*self.tilesize,self.tilesize,self.tilesize))
                