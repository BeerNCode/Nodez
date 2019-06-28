import logging
import json
import threading
import pygame
import vector
import colours
from tools import *
from vector import Vector

logger = logging.getLogger(__name__)

PLAYER_SPEED = 5

class Player(pygame.sprite.Sprite):

    def __init__(self):
        logger.debug("Creating player.")
        self.pos = vector.Vector(0, 0)

    def get_inputs(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.key_up = True
        if keys[pygame.K_DOWN]:
            self.key_down = True
        if keys[pygame.K_LEFT]:
            self.key_left = True
        if keys[pygame.K_RIGHT]:
            self.key_right = True
        if keys[pygame.K_SPACE]:
            self.key_space = True

    def update(self):
        if self.key_left:
            self.pos.x -= PLAYER_SPEED
        elif self.key_right:
            self.pos.x += PLAYER_SPEED
        elif self.key_up:
            self.pos.y += PLAYER_SPEED
        elif self.key_down:
            self.pos.y -= PLAYER_SPEED

    def show(self, screen):
        pygame.draw.ellipse(screen, colours.WHITE, [self.x, self.y, 50, 50], 2)