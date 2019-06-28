import pygame
import vector

NODE_RADIUS = 5
NODE_RANGE = 100

RED = (255, 0, 0)
DARK_RED = (100, 0, 0)
DARK_GREY = (25, 25, 25)

class Node:

    def __init__(self, is_fixed, is_source, pos):
        self.pos = vector.Vector(pos.x, pos.y)
        self.is_placed = True
        self.team = None
        self.is_source = is_source
        self.is_fixed = is_fixed
        self.links = set()

    def update(self):
        pass

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

            pygame.draw.ellipse(screen, colour, [self.pos.x-NODE_RADIUS*0.5, self.pos.y-NODE_RADIUS*0.5, NODE_RADIUS, NODE_RADIUS], line_width)
            pygame.draw.ellipse(screen, colour, [self.pos.x-NODE_RANGE*0.5, self.pos.y-NODE_RANGE*0.5, NODE_RANGE, NODE_RANGE], 2)

            for node in self.links:
                if node.is_placed:
                    pygame.draw.line(screen, colour, (self.pos.x, self.pos.y), (node.pos.x, node.pos.y), 2)