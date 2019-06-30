import os
import logging
import json
import threading
import pygame
import nodes
import vector
import colours
import random
import spritesheet
import maptiles
import math

from entity import Entity
from tools import *
from vector import Vector
from nodes import Node


logger = logging.getLogger(__name__)

PLAYER_SPEED = 3
PLAYER_SPEED_PENALTY = 0.8
NODE_HELD_DIAMETER = 15
PLAYER_RADIUS = 15
NODE_PICKUP_REQUIRED = 100
PLAYER_DIAMETER = 2 * PLAYER_RADIUS
NODE_COOLDOWN = 10
PICKUP_DISTANCE = PLAYER_RADIUS * PLAYER_RADIUS + nodes.NODE_RADIUS * nodes.NODE_RADIUS

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
        self.node_pickup = 0
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

        sheet = spritesheet.spritesheet(os.path.join('server', 'resources','player.png'))
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
        if self.controls.joystick is not None:
            joystick = self.controls.joystick
            hats = joystick.get_hat(0)
            self.key_up = hats[1]==1
            self.key_down = hats[1]==-1
            self.key_left = hats[0]==-1
            self.key_right = hats[0]==1
            if (joystick.get_numbuttons()>2):
                self.key_space = joystick.get_button( 1 )==1
            else:
                self.key_space = keys[self.controls.getKeys()["space"]]
        elif self.controls.network is not None:
            self.key_up = self.controls.network["state"]["up"]
            self.key_down = self.controls.network["state"]["down"]
            self.key_left = self.controls.network["state"]["left"]
            self.key_right = self.controls.network["state"]["right"]
            self.key_space = self.controls.network["state"]["a"]
        else:
            self.key_up = keys[self.controls.keys["up"]]
            self.key_down = keys[self.controls.keys["down"]]
            self.key_left = keys[self.controls.keys["left"]]
            self.key_right = keys[self.controls.keys["right"]]
            self.key_space = keys[self.controls.keys["space"]]

    def update(self, world, nodes):
        self.capture_inputs()
        
        speed = PLAYER_SPEED
        if self.node is not None:
            speed *= PLAYER_SPEED_PENALTY

        dx = 0
        dy = 0
        movingVertically = False
        movingHorizontally = False
        if self.key_up:
            dy = -speed
            self.direction = 0
            super().set_sprite("walking_up")
            movingVertically = True
        elif self.key_down:
            dy = speed
            self.direction = 1
            super().set_sprite("walking_down")
            movingVertically = True
        if self.key_left:
            dx = -speed                
            self.direction = 2
            super().set_sprite("walking_left")
            movingHorizontally = True
        elif self.key_right:
            dx = speed
            self.direction = 3
            super().set_sprite("walking_right")
            movingHorizontally = True

        if movingHorizontally and movingVertically:
            dx *= 0.717
            dy *= 0.717


        if self.move(self.pos.x + dx, self.pos.y, world) :
            self.pos.x += dx
        if self.move(self.pos.x, self.pos.y + dy, world) : 
            self.pos.y += dy

        if not movingHorizontally and not movingVertically:
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
        self.picking_up = False
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

                        if node.pos.quadrance_to(self.pos) < PICKUP_DISTANCE:
                            if node.team == self.team or node.team is None or self.node_pickup >= NODE_PICKUP_REQUIRED:
                                self.node = node
                                self.node.team = self.team
                                self.node.is_placed = False
                                self.node_ready = False
                                self.node_cooldown = NODE_COOLDOWN
                                break
                            else:
                                self.node_pickup += 1
                                self.picking_up = True
                                break                        
        else:
            self.node_cooldown -= 1
            if self.node_cooldown <= 0:
                self.node_ready = True

        if not self.picking_up:
            self.node_pickup = 0

    def move(self, x, y, world) :
        row = []
        row.append(math.floor((y - PLAYER_RADIUS/2)/ maptiles.TILESIZE))
        row.append(math.floor((y + PLAYER_RADIUS/2)/ maptiles.TILESIZE))

        column = []
        column.append(math.floor((x - PLAYER_RADIUS/2)/ maptiles.TILESIZE))
        column.append(math.floor((x + PLAYER_RADIUS/2)/ maptiles.TILESIZE))

        for x in range(2):
           if row[x] < 0 or row[x] >= len(world.access_map[0]):
                return False
           if column[x] < 0 or column[x] >= len(world.access_map):
               return False

        checkrow = 0

        while checkrow < 2:
            checkcolumn = 0
            while checkcolumn < 2 :
                if world.access_map[column[checkrow]][row[checkcolumn]] == 15:
                    return False
                checkcolumn += 1
            checkrow +=1

        return True

        
    def show(self, screen):
        super().show()
        pygame.draw.rect(screen, self.team.colour, [self.pos.x-PLAYER_RADIUS*0.6, self.pos.y+PLAYER_RADIUS, 2*PLAYER_RADIUS*0.6, 5], 0)
        if self.node is not None:
            pygame.draw.ellipse(screen, self.team.colour, [self.pos.x-NODE_HELD_DIAMETER*0.5, self.pos.y-PLAYER_RADIUS-NODE_HELD_DIAMETER-5, NODE_HELD_DIAMETER, NODE_HELD_DIAMETER], 0)
