import pygame
import os
import spritesheet
from tile import Tile
from map_generator import MapGenerator

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
        self.map_surface = pygame.Surface((self.width, self.height))

        grass_img = pygame.image.load('server\\resources\\grass-200.png')
        grass_inv_img = pygame.image.load('server\\resources\\grass-inv-200.png')
        ss = spritesheet.spritesheet('server\\resources\\dungeon_tiles.png')
        blank = ss.image_at((0, 0, 32, 32))
        topLeft = ss.image_at((64, 64, 96, 96))
        sideLeft = ss.image_at((64, 96, 96, 128))
        bottomLeft = ss.image_at((64, 32*6, 96, 32*6+32))
        topCentre = ss.image_at((96, 64, 128, 96))
        centre = ss.image_at((96, 32*4, 128, 32*4+32))
        bottomCentre = ss.image_at((96, 32*6, 128, 32*6+32))
        topRight = ss.image_at((32*6, 64, 32*6+32, 96))
        sideRight = ss.image_at((32*6, 32*4, 32*6+32, 32*4+32))
        bottomRight = ss.image_at((32*6, 32*6, 32*6+32, 32*6+32))

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
        for row in range(self.rows): 
            for col in range(self.columns):
                self.map_surface.blit(self.tilemap[row][col], (col*TILESIZE,row*TILESIZE,TILESIZE,TILESIZE))

    def show(self, screen):
        screen.blit(self.map_surface, (0, 0, self.width, self.height))