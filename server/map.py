import pygame
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
TILESIZE = 200

class Map:
    tilesize = TILESIZE
    grass_img = pygame.image.load('resources\grass-200.png')
    grass_inv_img = pygame.image.load('resources\grass-inv-200.png')
    tilemap = [
        [grass_img,grass_img,grass_img],
        [grass_img,grass_inv_img,grass_img],
        [grass_inv_img,grass_img,grass_img],
        [grass_img,grass_img,grass_inv_img]
        ]
    height = 4
    width = 3
    
    def show(self,screen):
        
        for row in range(self.height): 
            for col in range(self.width):
                screen.blit(self.tilemap[row][col], (col*self.tilesize,row*self.tilesize,self.tilesize,self.tilesize))
                #Tile((col*self.tilesize,row*self.tilesize,self.tilesize,self.tilesize))
                #pygame.draw.rect(screen,COLOURS[self.tilemap[row][col]],(col*self.tilesize,row*self.tilesize,self.tilesize,self.tilesize))
                