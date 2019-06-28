import pygame
import vector

NODE_SIZE = 50
NODE_RADIUS = 250

RED = (255, 0, 0)
DARK_RED = (100, 0, 0)

class Node:

    def __init__(self, pos):
        self.pos = vector.Vector(pos.x, pos.y)

    def update(self):
        pass

    def show(self, screen):
        pygame.draw.ellipse(screen, DARK_RED, [self.pos.x-NODE_SIZE/2, self.pos.y-NODE_SIZE/2, NODE_SIZE, NODE_SIZE], 2)
        pygame.draw.ellipse(screen, RED, [self.pos.x-NODE_RADIUS/2, self.pos.y-NODE_RADIUS/2, NODE_RADIUS, NODE_RADIUS], 2)