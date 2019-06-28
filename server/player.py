import logging
import json
import threading
import pygame
import vector
import colours
from tools import *
from vector import Vector
from node import Node

logger = logging.getLogger(__name__)

PLAYER_SPEED = 1

class Player:

    def __init__(self):
        logger.debug("Creating player.")
        self.pos = vector.Vector(0, 0)
        self.key_left = False

    def capture_inputs(self):
        keys = pygame.key.get_pressed()
        self.key_up = keys[pygame.K_UP]
        self.key_down = keys[pygame.K_DOWN]
        self.key_left = keys[pygame.K_LEFT]
        self.key_right = keys[pygame.K_RIGHT]
        self.key_space = keys[pygame.K_SPACE]

    def update(self):
        self.capture_inputs()

        if self.key_left:
            self.pos.x -= PLAYER_SPEED
        elif self.key_right:
            self.pos.x += PLAYER_SPEED
        if self.key_up:
            self.pos.y -= PLAYER_SPEED
        elif self.key_down:
            self.pos.y += PLAYER_SPEED

        if self.key_space:
            return Node(self.pos)
        return None

    def show(self, screen):
        pygame.draw.ellipse(screen, colours.WHITE, [self.pos.x, self.pos.y, 50, 50], 2)