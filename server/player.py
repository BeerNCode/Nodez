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
PLAYER_RADIUS = 50
NODE_COOLDOWN = 100

class Player:

    def __init__(self):
        logger.debug("Creating player.")
        self.pos = vector.Vector(0, 0)
        self.key_left = False
        self.node_ready = True
        self.node_cooldown = 0

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

        if self.node_ready:
            if self.key_space:
                self.node_cooldown = NODE_COOLDOWN
                self.node_ready = False
                return Node(self.pos)
        else:
            self.node_cooldown -= 1
            if self.node_cooldown <= 0:
                self.node_ready = True
        return None

    def show(self, screen):
        pygame.draw.ellipse(screen, colours.WHITE, [self.pos.x-PLAYER_RADIUS/2, self.pos.y-PLAYER_RADIUS/2, PLAYER_RADIUS, PLAYER_RADIUS], 2)
        font = pygame.font.SysFont('Calibri', 12, True, False)
        bar_step = 0.5
        screen.blit(font.render(str(self.node_cooldown), True, colours.WHITE), [self.pos.x, self.pos.y+PLAYER_RADIUS])