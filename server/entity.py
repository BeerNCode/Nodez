import pygame
import logging

logger = logging.getLogger(__name__)

class Entity(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.sprites = {}
        self.sprite_index = 0

    def add_sprite(self, sprite_id, sheet, rectangle):
        logger.debug(f"setting {sprite_id}")
        logger.debug(rectangle)
        sprite = sheet.image_at(rectangle)
        sprite.set_colorkey((255, 255, 255))
        self.sprites[sprite_id] = [sprite]

    def add_sprites(self, sprite_id, sheet, rectangle, amount, offset):
        sprites = []
        logger.debug(f"setting {sprite_id}")
        for i in range(amount):
            r = (rectangle[0]+offset[0]*i, rectangle[1]+offset[1]*i,rectangle[2],rectangle[3])
            logger.debug(r)
            sprite = sheet.image_at(r)
            sprite.set_colorkey((255, 255, 255))
            sprites.append(sprite)
        self.sprites[sprite_id] = sprites

    def set_sprite(self, sprite_id):
        logger.debug(f"setting sprite to {sprite_id}")
        self.images = self.sprites[sprite_id]

    def show(self):
        logger.debug(f"{self.sprite_index} in {len(self.images)}")
        self.sprite_index += 1
        if self.sprite_index >= len(self.images):
            self.sprite_index = 0
        self.image = self.images[self.sprite_index]

        self.rect = self.image.get_rect()
        self.rect.x = (self.pos.x-self.rect.width/2)
        self.rect.y = (self.pos.y-self.rect.height/2)