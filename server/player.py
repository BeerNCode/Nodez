import logging
import json
import threading
import pygame
import nodes
import vector
import colours
import random
import spritesheet
from entity import Entity
from tools import *
from vector import Vector
from nodes import Node


logger = logging.getLogger(__name__)

PLAYER_SPEED = 1
PLAYER_RADIUS = 24
PLAYER_DIAMETER = 2 * PLAYER_RADIUS
NODE_COOLDOWN = 100

class Player(Entity):

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
        self.direction = 0

        tile_size = 32
        offsets = [
            (tile_size * 0, tile_size * 0),
            (tile_size * 3, tile_size * 0),
            (tile_size * 6, tile_size * 0),
            (tile_size * 9, tile_size * 0),
            (tile_size * 0, tile_size * 4),
            (tile_size * 3, tile_size * 4),
            (tile_size * 6, tile_size * 4),
            (tile_size * 9, tile_size * 4),
        ]
        
        offset = offsets[random.randint(0, len(offsets)-1)]
        logger.debug(f"offset is {offset}")

        sheet = spritesheet.spritesheet('server\\resources\\player.png')
        super().add_sprite("up", sheet, (offset[0] + 0 * tile_size, offset[1] + 3 * tile_size, tile_size, tile_size))
        super().add_sprite("down", sheet, (offset[0] + 0 * tile_size, offset[1] + 0 * tile_size, tile_size, tile_size))
        super().add_sprite("left", sheet, (offset[0] + 0 * tile_size, offset[1] + 1 * tile_size, tile_size, tile_size))
        super().add_sprite("right", sheet, (offset[0] + 0 * tile_size, offset[1] + 2 * tile_size, tile_size, tile_size))
        super().add_sprites("walking_up", sheet, (offset[0] + 0 * tile_size, offset[1] + 3 * tile_size, tile_size, tile_size), 3, (tile_size, 0))
        super().add_sprites("walking_down", sheet, (offset[0] + 0 * tile_size, offset[1] + 0 * tile_size, tile_size, tile_size), 3, (tile_size, 0))
        super().add_sprites("walking_left", sheet, (offset[0] + 0 * tile_size, offset[1] + 1 * tile_size, tile_size, tile_size), 3, (tile_size, 0))
        super().add_sprites("walking_right", sheet, (offset[0] + 0 * tile_size, offset[1] + 2 * tile_size, tile_size, tile_size), 3, (tile_size, 0))
        super().set_sprite("down")

    def capture_inputs(self):
        keys = pygame.key.get_pressed()
        self.key_up = keys[self.controls["up"]]
        self.key_down = keys[self.controls["down"]]
        self.key_left = keys[self.controls["left"]]
        self.key_right = keys[self.controls["right"]]
        self.key_space = keys[self.controls["space"]]

    def update(self, world, nodes):
        self.capture_inputs()
        
        speed = PLAYER_SPEED
        if self.node is not None:
            speed *= 0.8

        moving = False
        if self.key_up:
            self.pos.y -= PLAYER_SPEED
            self.direction = 0
            super().set_sprite("walking_up")
            moving = True
        elif self.key_down:
            self.pos.y += PLAYER_SPEED
            self.direction = 1
            super().set_sprite("walking_down")
            moving = True
        if self.key_left:
            self.pos.x -= PLAYER_SPEED
            self.direction = 2
            super().set_sprite("walking_left")
            moving = True
        elif self.key_right:
            self.pos.x += PLAYER_SPEED
            self.direction = 3
            super().set_sprite("walking_right")
            moving = True

        if not moving:
            if self.direction == 0:
                super().set_sprite("up")
            elif self.direction == 1:
                super().set_sprite("down")
            elif self.direction == 2:
                super().set_sprite("left")
            elif self.direction == 3:
                super().set_sprite("right")

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
        super().show()