import logging
import json
import threading
import pygame
import node
import vector
import colours
from tools import *
from vector import Vector
from node import Node

logger = logging.getLogger(__name__)

PLAYER_SPEED = 1
PLAYER_RADIUS = 50

NODE_COOLDOWN = 50

class Player:

    def __init__(self, name, team, controls):
        logger.debug("Creating player.")
        self.name = name
        self.team = team
        self.controls = controls
        self.pos = vector.Vector(0, 0)
        self.key_left = False
        self.node = None
        self.node_cooldown = 0
        self.node_ready = True

    def capture_inputs(self):
        keys = pygame.key.get_pressed()
        self.key_up = keys[self.controls["up"]]
        self.key_down = keys[self.controls["down"]]
        self.key_left = keys[self.controls["left"]]
        self.key_right = keys[self.controls["right"]]
        self.key_space = keys[self.controls["space"]]

    def update(self, nodes):
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
                if self.node is not None:
                    self.node.pos.x = self.pos.x
                    self.node.pos.y = self.pos.y
                    self.node.is_placed = True
                    self.node = None
                    self.node_ready = False
                    self.node_cooldown = NODE_COOLDOWN
                else:
                    for node in nodes:
                        if node.pos.quadrance_to(self.pos) < PLAYER_RADIUS * PLAYER_RADIUS:
                            self.node = node
                            self.node.is_placed = False
                            self.node_ready = False
                            self.node_cooldown = NODE_COOLDOWN
                            break
        else:
            self.node_cooldown -= 1
            if self.node_cooldown <= 0:
                self.node_ready = True

    def show(self, screen):
        pygame.draw.ellipse(screen, self.team.colour, [self.pos.x-PLAYER_RADIUS/2, self.pos.y-PLAYER_RADIUS/2, PLAYER_RADIUS, PLAYER_RADIUS], 2)
        if self.node:
            pygame.draw.ellipse(screen, node.DARK_RED, [self.pos.x-node.NODE_SIZE/2, self.pos.y-node.NODE_SIZE/2, node.NODE_SIZE, node.NODE_SIZE], 2)