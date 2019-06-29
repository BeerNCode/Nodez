import pygame
import os
import spritesheet
from tile import Tile
#TRDL
XXXX = 15
XXXO = 14
XXOX = 13
XXOO = 12
XOXX = 11
XOXO = 10
XOOX = 9
XOOO = 8
OXXX = 7
OXXO = 6
OXOX = 5
OXOO = 4
OOXX = 3
OOXO = 2
OOOX = 1
OOOO = 0


SOURCE_TILE = 2
SINK_TILE = 3
BLACK = (30,30,30)
BROWN = (153,76,0)
GREEN = (30,255,30)
BLUE = (30,40,255)
RED = (255,40,55)
TILESIZE = 32

class MapTiles:
    def __init__(self, accessMap):
        self.rows = 20
        self.columns = 30
        self.height = self.rows * TILESIZE
        self.width = self.columns * TILESIZE
        self.map_surface = pygame.Surface((self.width, self.height))

        grass_img = pygame.image.load('server\\resources\\grass-200.png')
        grass_inv_img = pygame.image.load('server\\resources\\grass-inv-200.png')
        ss = spritesheet.spritesheet('server\\resources\\dungeon_tiles.png')
        blank = ss.image_at((0, 0, 32, 32),(255,255,255))
        topLeft = ss.image_at((64, 64, 32, 32),(255,255,255))
        sideLeft = ss.image_at((64, 96, 32, 32),(255,255,255))
        bottomLeft = ss.image_at((64, 32*6, 32, 32),(255,255,255))
        topCentre = ss.image_at((96, 64, 32, 32),(255,255,255))
        centre = ss.image_at((96, 32*4, 32, 32),(255,255,255))
        bottomCentre = ss.image_at((96, 32*6, 32, 32),(255,255,255))
        topRight = ss.image_at((32*6, 64, 32, 32),(255,255,255))
        sideRight = ss.image_at((32*6, 32*4, 32, 32),(255,255,255))
        bottomRight = ss.image_at((32*6, 32*6, 32, 32),(255,255,255))
        bottomEdge = ss.image_at((32*6, 32*7, 32, 32),(255,255,255))
        leftRightBridge = ss.image_at((264, 64, 32, 32),(255,255,255))
        leftBlock = ss.image_at((64, 256, 32, 32),(255,255,255))
        topBottomBridge = ss.image_at((280, 340, 32, 32),(255,255,255))
        self.accessMap = accessMap

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
        self.tilemap[5][5] = leftBlock

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
            return self.leftRightBridge
        if (self.accessMap[row][col]==XOOX):
            return self.topLeft
        if (self.accessMap[row][col]==XOOO):
            return self.topCentre
        if (self.accessMap[row][col]==OXXX):
            return self.blank
        if (self.accessMap[row][col]==OXXO):
            return self.blank
        if (self.accessMap[row][col]==OXOX):
            return self.topBottomBridge
        if (self.accessMap[row][col]==OXOO):
            return self.sideRight
        if (self.accessMap[row][col]==OOXX):
            return self.bottomLeft
        if (self.accessMap[row][col]==OOXO):
            return self.bottomCentre
        if (self.accessMap[row][col]==OOOX):
            return self.sideLeft
        if (self.accessMap[row][col]==OOOO):
            return self.centre
