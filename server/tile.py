import pygame

GRASS_TILE = None

class Tile(pygame.sprite.Sprite):
    
    GRASS_TILE = None
    def __init__(self, pos):
        if self.GRASS_TILE is None:
            self.GRASS_TILE = pygame.image.load('resources\grass-200.png').convert_alpha()
        super().__init__()
        self.image = self.GRASS_TILE
 