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

    def __init__(self, name, team, controls):
        logger.debug("Creating player.")
        self.name = name
        self.team = team
        self.controls = controls
        self.pos = vector.Vector(0, 0)
        self.key_left = False
        self.node_ready = True
        self.node_cooldown = 0

    def capture_inputs(self):
        keys = pygame.key.get_pressed()
        self.key_up = keys[self.controls["up"]]
        self.key_down = keys[self.controls["down"]]
        self.key_left = keys[self.controls["left"]]
        self.key_right = keys[self.controls["right"]]
        self.key_space = keys[self.controls["space"]]

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
        pygame.draw.ellipse(screen, self.team.colour, [self.pos.x-PLAYER_RADIUS/2, self.pos.y-PLAYER_RADIUS/2, PLAYER_RADIUS, PLAYER_RADIUS], 2)
        font = pygame.font.SysFont('Calibri', 12, True, False)
        bar_step = 0.5
        screen.blit(font.render(str(self.node_cooldown), True, colours.WHITE), [self.pos.x, self.pos.y+PLAYER_RADIUS])