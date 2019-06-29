import logging
import json
import threading
import pygame
import nodes
import vector
import colours
from tools import *
from vector import Vector
from nodes import Node

import spritesheet

logger = logging.getLogger(__name__)

PLAYER_SPEED = 2
PLAYER_RADIUS = 24
PLAYER_DIAMETER = 2 * PLAYER_RADIUS
NODE_COOLDOWN = 100

class Player(pygame.sprite.Sprite):

    def __init__(self, name, team, controls):
        super().__init__()
        logger.debug("Creating player.")
        self.name = name
        self.team = team
        self.controls = controls
        self.pos = vector.Vector(self.team.node.pos.x, self.team.node.pos.y)
        self.node = None
        self.node_cooldown = 0
        self.node_ready = True

        self.sprites = {}
        sheet = spritesheet.spritesheet('server\\resources\\dungeon_tiles.png')
        self.add_sprite("down", sheet, (0, 0, PLAYER_DIAMETER, PLAYER_DIAMETER))

        self.set_sprite("down")

    def capture_inputs(self):
        keys = pygame.key.get_pressed()
        self.key_up = keys[self.controls["up"]]
        self.key_down = keys[self.controls["down"]]
        self.key_left = keys[self.controls["left"]]
        self.key_right = keys[self.controls["right"]]
        self.key_space = keys[self.controls["space"]]

    def add_sprite(self, spriteid, sheet, rectangle):
        sprite = sheet.image_at(rectangle)
        self.sprites[spriteid] = sprite

    def set_sprite(self, spriteid):
        self.image = self.sprites[spriteid]

    def update(self, world, nodes):
        self.capture_inputs()
        
        speed = PLAYER_SPEED
        if self.node is not None:
            speed *= 0.8

        if self.key_left:
            self.pos.x -= PLAYER_SPEED
        elif self.key_right:
            self.pos.x += PLAYER_SPEED
        if self.key_up:
            self.pos.y -= PLAYER_SPEED
        elif self.key_down:
            self.pos.y += PLAYER_SPEED

        if self.pos.x < PLAYER_RADIUS*0.5:
            self.pos.x = PLAYER_RADIUS*0.5
        if self.pos.y < PLAYER_RADIUS*0.5:
            self.pos.y = PLAYER_RADIUS*0.5
        if self.pos.x > world.width - PLAYER_RADIUS*0.5:
            self.pos.x = world.width - PLAYER_RADIUS*0.5
        if self.pos.y > world.height - PLAYER_RADIUS*0.5:
            self.pos.y = world.height - PLAYER_RADIUS*0.5

        if self.node_ready:
            if self.key_space:
                if self.node is not None:
                    self.node.pos.x = self.pos.x
                    self.node.pos.y = self.pos.y
                    self.node.is_placed = True
                    self.node.update_links(nodes)
                    self.node.energy = 0
                    self.node = None
                    self.node_ready = False
                    self.node_cooldown = NODE_COOLDOWN

                else:
                    for node in nodes:
                        if node.is_fixed:
                            continue

                        if node.pos.quadrance_to(self.pos) < PLAYER_RADIUS * PLAYER_RADIUS:
                            self.node = node
                            self.node.team = self.team
                            self.node.is_placed = False
                            self.node_ready = False
                            self.node_cooldown = NODE_COOLDOWN
                            break
        else:
            self.node_cooldown -= 1
            if self.node_cooldown <= 0:
                self.node_ready = True

    def show(self, screen):
        self.rect = self.image.get_rect()
        self.rect.x = (self.pos.x-self.rect.width/2)
        self.rect.y = (self.pos.y-self.rect.height/2)
        
        #pygame.draw.ellipse(screen, self.team.colour, [self.pos.x-PLAYER_RADIUS/2, self.pos.y-PLAYER_RADIUS/2, PLAYER_RADIUS, PLAYER_RADIUS], 2)
        #if self.node:
        #    pygame.draw.ellipse(screen, self.team.colour, [self.pos.x-nodes.NODE_RADIUS/2, self.pos.y-nodes.NODE_RADIUS/2, nodes.NODE_RADIUS, nodes.NODE_RADIUS], 2)