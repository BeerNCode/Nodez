import pygame
import vector
import colours
import spritesheet
import random
from pygame import gfxdraw
from entity import Entity

NODE_RADIUS = 25
NODE_RANGE = 100

RED = (255, 0, 0)
DARK_RED = (100, 0, 0)
DARK_GREY = (25, 25, 25)

pygame.font.init()
FONT = pygame.font.SysFont('Calibri', 12, True, False)

class Node(Entity):

    def __init__(self, is_fixed, is_source, pos):
        super().__init__()
        self.pos = vector.Vector(pos.x, pos.y)
        self.is_placed = True
        self.team = None
        self.is_source = is_source
        self.is_fixed = is_fixed
        self.links = set()
        self.energy = 0

        tile_size = 32
        sheet = spritesheet.spritesheet('server\\resources\\dungeon_tiles.png')
        super().add_sprite("flicker_left", sheet, (383, 262, 16, 40))
        super().add_sprite("flicker_right", sheet, (414, 262, 16, 40))
        super().set_sprite("flicker_left")

    def update(self):
        if self.is_source:
            self.energy += 1

        if self.is_fixed and self.team is not None and self.energy > 0:
            self.team.energy += 1
        else:
            for node in self.links:
                if (node.energy < self.energy or (node.team is not None and node.is_fixed)) and self.energy > 1:
                    rate = 50 / node.pos.distance_to(self.pos)
                    node.energy += rate
                    self.energy -= rate


    def update_links(self, nodes):
        for node in self.links:
            node.links.remove(self)
        self.links.clear()

        for node in nodes:
            if node is self:
                continue

            if not node.is_placed:
                continue

            if not node.is_source:
                if node.team is None or node.team is not self.team:
                    continue

            if self.pos.quadrance_to(node.pos) < NODE_RANGE * NODE_RANGE:
                self.link(node)

    def link(self, node):
        self.links.add(node)
        node.links.add(self)

    def unlink(self, node):
        self.links.remove(node)

    def show(self, screen):
        super().show()

        if random.random() > 0.5:
            super().set_sprite("flicker_left")
        else:
            super().set_sprite("flicker_right")

        if self.is_placed:
            if self.team is not None:
                colour = self.team.colour
            elif self.is_source:
                colour = (200, 255, 150)
            else:
                colour = DARK_GREY
            line_width = 2
            if self.is_fixed:
                line_width = 0

            #pygame.draw.ellipse(screen, colour, [self.pos.x-NODE_RADIUS*0.5, self.pos.y-NODE_RADIUS*0.5, NODE_RADIUS, NODE_RADIUS], line_width)
            
            pygame.gfxdraw.aacircle(screen, int(self.pos.x), int(self.pos.y), int(NODE_RANGE*0.5), colour)
            screen.blit(FONT.render(f"{self.energy:.0f}", True, colours.WHITE), [self.pos.x, self.pos.y+NODE_RADIUS])

            for node in self.links:
                if node.is_placed:
                    pygame.draw.line(screen, colour, (self.pos.x, self.pos.y), (node.pos.x, node.pos.y), 2)