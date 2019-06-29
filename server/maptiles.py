import pygame
import os
import spritesheet
from tile import Tile
#TRDL
XXXX = 0
XXXO = 1
XXOX = 2
XXOO = 4
XOXX = 5
XOXO = 6
XOOX = 7
XOOO = 7
OXXX = 8
OXXO = 9
OXOX = 10
OXOO = 11
OOXX = 12
OOXO = 13
OOOX = 14
OOOO = 15


SOURCE_TILE = 2
SINK_TILE = 3
BLACK = (30,30,30)
BROWN = (153,76,0)
GREEN = (30,255,30)
BLUE = (30,40,255)
RED = (255,40,55)
TILESIZE = 32

class MapTiles:
    def __init__(self):
        self.rows = 20
        self.columns = 30
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
        bottomEdge = ss.image_at((32*6, 32*7, 32*6+32, 32*7+32))
        self.accessMap = [
            
            ]

        #self.tilemap = [
        #    [topLeft,topCentre,topCentre,topCentre,topCentre,topCentre,topCentre,topCentre,topCentre,topRight],
        #    [sideLeft,centre,centre,centre,centre,centre,centre,centre,centre,sideRight],
        #    [sideLeft,centre,centre,centre,centre,centre,centre,centre,centre,sideRight],
        #    [sideLeft,centre,centre,centre,centre,centre,centre,centre,centre,sideRight],
        #    [sideLeft,centre,centre,centre,centre,centre,centre,centre,centre,sideRight],
        #    [sideLeft,centre,centre,centre,centre,centre,centre,centre,centre,sideRight],
        #    [sideLeft,centre,centre,centre,centre,centre,centre,centre,centre,sideRight],
        #    [sideLeft,centre,centre,centre,centre,centre,centre,centre,centre,sideRight],
        #    [bottomLeft,bottomCentre,bottomCentre,bottomCentre,bottomCentre,bottomCentre,bottomCentre,bottomCentre,bottomCentre,bottomRight],
        #    [bottomEdge,bottomEdge,bottomEdge,bottomEdge,bottomEdge,bottomEdge,bottomEdge,bottomEdge,bottomEdge,bottomEdge]
        #]
        self.tilemap = [[0] * self.columns for _ in range(self.rows)]
        for row in range(self.rows): 
            for col in range(self.columns):
                if (row == 0):
                    if (col == 0):
                        self.tilemap[row][col] = topLeft
                    elif (col == self.columns-1):
                        self.tilemap[row][col] = topRight
                    else:
                        self.tilemap[row][col] = topCentre
                    continue
                if (row == self.rows-2):
                    if (col == 0):
                        self.tilemap[row][col] = bottomLeft
                    elif (col == self.columns-1):
                        self.tilemap[row][col] = bottomRight
                    else:
                        self.tilemap[row][col] = bottomCentre
                    continue
                if (row == self.rows-1):
                    self.tilemap[row][col] = bottomEdge
                    continue
                if (col == 0):
                    self.tilemap[row][col] = sideLeft
                elif (col == self.columns-1):
                    self.tilemap[row][col] = sideRight
                else:
                    self.tilemap[row][col] = centre
                continue


        for row in range(self.rows): 
            for col in range(self.columns):
                self.map_surface.blit(self.tilemap[row][col], (col*TILESIZE,row*TILESIZE,TILESIZE,TILESIZE))

    def show(self, screen):
        screen.blit(self.map_surface, (0, 0, self.width, self.height))

    def lookupTile(self,row,col):
        if (self.accessMap[row][col]==XXXX):
            return self.blank
        if (self.accessMap[row][col]==XXXO):
            return self.blank
        if (self.accessMap[row][col]==XXOX):
            return self.blank
        if (self.accessMap[row][col]==XXOO):
            return self.topRight
        if (self.accessMap[row][col]==XOXX):
            return self.blank
        if (self.accessMap[row][col]==XOXO):
            return self.blank
        if (self.accessMap[row][col]==XOOX):
            return self.topLeft
        if (self.accessMap[row][col]==XOOO):
            return self.topCentre
        if (self.accessMap[row][col]==OXXX):
            return self.blank
        if (self.accessMap[row][col]==OXXO):
            return self.blank
        if (self.accessMap[row][col]==OXOX):
            return self.blank
        if (self.accessMap[row][col]==OXOO):
            return self.sideRight
        if (self.accessMap[row][col]==OOXX):
            return self.bottomLeft
        if (self.accessMap[row][col]==OOXO):
            return self.bottomCentre
        if (self.accessMap[row][col]==OOOX):
            return self.blank
        if (self.accessMap[row][col]==OOOO):
            return self.centre
