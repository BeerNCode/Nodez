import pygame
import os
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
        self.rows = 10
        self.columns = 10
        self.height = self.rows * TILESIZE
        self.width = self.columns * TILESIZE

        grass_img = pygame.image.load('server\\resources\\grass-200.png')
        grass_inv_img = pygame.image.load('server\\resources\\grass-inv-200.png')
        ss = spritesheet.spritesheet('server\\resources\\dungeon_tiles.png')
        topLeft = ss.image_at((32, 32, 64, 64))
        sideLeft = ss.image_at((32, 64, 64, 96))
        bottomLeft = ss.image_at((32, 96, 64, 128))
        topCentre = ss.image_at((64, 32, 96, 64))
        centre = ss.image_at((64, 64, 96, 96))
        bottomCentre = ss.image_at((64, 96, 96, 128))
        topRight = ss.image_at((96, 32, 128, 64))
        sideRight = ss.image_at((96, 64, 128, 96))
        bottomRight = ss.image_at((96, 96, 128, 128))
        self.tilemap = [
            [topLeft,topCentre,topCentre,topCentre,topCentre,topCentre,topCentre,topCentre,topCentre,topRight],
            [sideLeft,centre,centre,centre,centre,centre,centre,centre,centre,sideRight],
            [sideLeft,centre,centre,centre,centre,centre,centre,centre,centre,sideRight],
            [sideLeft,centre,centre,centre,centre,centre,centre,centre,centre,sideRight],
            [sideLeft,centre,centre,centre,centre,centre,centre,centre,centre,sideRight],
            [sideLeft,centre,centre,centre,centre,centre,centre,centre,centre,sideRight],
            [sideLeft,centre,centre,centre,centre,centre,centre,centre,centre,sideRight],
            [sideLeft,centre,centre,centre,centre,centre,centre,centre,centre,sideRight],
            [sideLeft,centre,centre,centre,centre,centre,centre,centre,centre,sideRight],
            [bottomLeft,bottomCentre,bottomCentre,bottomCentre,bottomCentre,bottomCentre,bottomCentre,bottomCentre,bottomCentre,bottomRight]
        ]

    def show(self,screen):
        for row in range(self.rows): 
            for col in range(self.columns):
                screen.blit(self.tilemap[row][col], (col*TILESIZE,row*TILESIZE,TILESIZE,TILESIZE))
                #Tile((col*self.tilesize,row*self.tilesize,self.tilesize,self.tilesize))
                #pygame.draw.rect(screen,COLOURS[self.tilemap[row][col]],(col*self.tilesize,row*self.tilesize,self.tilesize,self.tilesize))
                