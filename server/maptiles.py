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
    def __init__(self, block_map, columns, rows):
        self.rows = rows
        self.columns = columns
        self.height = self.rows * TILESIZE
        self.width = self.columns * TILESIZE
        self.map_surface = pygame.Surface((self.width, self.height))
        self.block_map = block_map
        self.generate_access_map()

        grass_img = pygame.image.load('server\\resources\\grass-200.png')
        grass_inv_img = pygame.image.load('server\\resources\\grass-inv-200.png')
        ss = spritesheet.spritesheet('server\\resources\\dungeon_tiles.png')
        self.blank = ss.image_at((0, 0, 32, 32),(255,255,255))
        self.topLeft = ss.image_at((64, 64, 32, 32),(255,255,255))
        self.sideLeft = ss.image_at((64, 96, 32, 32),(255,255,255))
        self.bottomLeft = ss.image_at((64, 32*6, 32, 32),(255,255,255))
        self.topCentre = ss.image_at((96, 64, 32, 32),(255,255,255))
        self.centre = ss.image_at((96, 32*4, 32, 32),(255,255,255))
        self.bottomCentre = ss.image_at((96, 32*6, 32, 32),(255,255,255))
        self.topRight = ss.image_at((32*6, 64, 32, 32),(255,255,255))
        self.sideRight = ss.image_at((32*6, 32*4, 32, 32),(255,255,255))
        self.bottomRight = ss.image_at((32*6, 32*6, 32, 32),(255,255,255))
        self.bottomEdge = ss.image_at((32*6, 32*7, 32, 32),(255,255,255))
        self.leftRightBridge = ss.image_at((264, 64, 32, 32),(255,255,255))
        self.leftBlock = ss.image_at((64, 256, 32, 32),(255,255,255))
        self.rightBlock = ss.image_at((96, 256, 32, 32),(255,255,255))
        self.topBottomBridge = ss.image_at((280, 340, 32, 32),(255,255,255))
        self.barrelIcon = ss.image_at((392, 219, 32, 32),(255,255,255))
        self.barrel = pygame.Surface((32,32)).convert()
        self.barrel.blit(self.centre, (0, 0, self.width, self.height))
        self.barrel.blit(self.barrelIcon, (0, 0, self.width, self.height))

        
        self.tilemap = [[0] * self.columns for _ in range(self.rows)]
        for row in range(self.rows): 
            for col in range(self.columns):
                self.tilemap[row][col] = self.lookupTile(row,col)

        for row in range(self.rows): 
            for col in range(self.columns):
                self.map_surface.blit(self.tilemap[row][col], (col*TILESIZE,row*TILESIZE,TILESIZE,TILESIZE))

    def show(self, screen):
        screen.blit(self.map_surface, (0, 0, self.width, self.height))

    def generate_access_map(self):
        self.access_map = [[0] * self.rows for i in range(self.columns)]
        max_x = self.columns - 1
        max_y = self.rows - 1

        for ix in range(self.columns):
            for iy in range(self.rows):
                if (self.block_map[ix][iy] < 0):
                    self.access_map[ix][iy] = 15
                    continue
                
                if (iy == 0 or self.block_map[ix][iy-1] < 0):
                    self.access_map[ix][iy] += 8
                if (ix == max_x or self.block_map[ix+1][iy] < 0):
                    self.access_map[ix][iy] += 4
                if (iy == max_y or self.block_map[ix][iy+1] < 0):
                    self.access_map[ix][iy] += 2
                if (ix == 0 or self.block_map[ix-1][iy] < 0):
                    self.access_map[ix][iy] += 1

    def lookupTile(self,row,col):
        if (self.access_map[col][row]==XXXX):
            if (row>0 and row < self.rows-1 and col >0 and col < self.columns-1):
                if (self.access_map[col-1][row-1]==OOOO and self.access_map[col-1][row]==OOOO and self.access_map[col-1][row+1]==OOOO and
                    self.access_map[col][row-1]==OOOO and self.access_map[col][row+1]==OOOO and
                    self.access_map[col+1][row-1]==OOOO and self.access_map[col+1][row]==OOOO and self.access_map[col+1][row+1]==OOOO):
                    return self.barrel
            if (row>0 and self.access_map[col][row-1]!=XXXX):
                return self.bottomEdge
            return self.blank
        if (self.access_map[col][row]==XXXO):
            return self.rightBlock
        if (self.access_map[col][row]==XXOX):
            return self.blank
        if (self.access_map[col][row]==XXOO):
            return self.topRight
        if (self.access_map[col][row]==XOXX):
            return self.blank
        if (self.access_map[col][row]==XOXO):
            return self.leftRightBridge
        if (self.access_map[col][row]==XOOX):
            return self.topLeft
        if (self.access_map[col][row]==XOOO):
            return self.topCentre
        if (self.access_map[col][row]==OXXX):
            return self.blank
        if (self.accessMap[col][row]==OXXO):
            return self.bottomRight
        if (self.accessMap[col][row]==OXOX):
            return self.topBottomBridge
        if (self.access_map[col][row]==OXOO):
            return self.sideRight
        if (self.access_map[col][row]==OOXX):
            return self.bottomLeft
        if (self.access_map[col][row]==OOXO):
            return self.bottomCentre
        if (self.access_map[col][row]==OOOX):
            return self.sideLeft
        if (self.access_map[col][row]==OOOO):
            return self.centre
