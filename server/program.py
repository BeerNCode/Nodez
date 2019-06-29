#import socket
import pygame
import json
import threading
import logging
import colours
import nodes
from team import Team
from player import Player
from maptiles import MapTiles
from nodes import Node
from vector import Vector
import random

from tools import *

logging.basicConfig(level=logging.DEBUG)

CLIENT_TIMEOUT = 1000
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
GAME_SPEED = 60

NUMBER_OF_NODES = 20

logger = logging.getLogger(__name__)

class Program:

    def __init__(self):
        pygame.display.set_caption("Nodez")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        self.teams = []
        self.players = []
        self.nodes = []
        self.world = MapTiles()
        self.clock = pygame.time.Clock()
        teamA = Team("Sharks", (0, 0, 255))
        teamB = Team("Tigers", (0, 255, 0))
        self.teams.append(teamA)
        self.teams.append(teamB)
        teamANode = Node(True,False,Vector(SCREEN_WIDTH*0.1, SCREEN_HEIGHT*0.5))
        teamBNode = Node(True,False,Vector(SCREEN_WIDTH*0.9, SCREEN_HEIGHT*0.5))
        teamANode.team = teamA
        teamBNode.team = teamB
        teamA.node = teamANode
        teamB.node = teamBNode
        self.nodes.append(teamANode)
        self.nodes.append(teamBNode)
        self.nodes.append(Node(True,True,Vector(SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.5)))

        for i in range(NUMBER_OF_NODES):
            x = random.random() * SCREEN_WIDTH
            y = random.random() * SCREEN_HEIGHT
            self.nodes.append(Node(False,False,Vector(x, y)))

        self.start_ticks=pygame.time.get_ticks()
        self.players.append(Player("Dave",self.teams[0], {"up": pygame.K_UP,"down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "space": pygame.K_SPACE}))
        self.players.append(Player("Tom",self.teams[1], {"up": pygame.K_w,"down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d, "space": pygame.K_g}))
        self.running = True

    def update(self):
        logger.info("Got update!")

    def run(self):
        while self.running:
            self.update_events()
            
            for player in self.players:
                player.update(self.world, self.nodes)
            for node in self.nodes:
                node.update()

            self.render()
      
            pygame.display.flip()

            self.update_timer()

            self.clock.tick(GAME_SPEED)

    def update_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.info("Ending the game.")
                self.running = False

            if event.type == pygame.VIDEORESIZE:
                SCREEN_WIDTH = event.w
                SCREEN_HEIGHT = event.h
                logger.info(f"Resizing the window to {SCREEN_WIDTH}x{SCREEN_HEIGHT}.")
                self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

    def render(self):
        self.screen.fill(colours.LIGHT_GREY)
        player_sprites = pygame.sprite.Group()

        self.world.show(self.screen)
        for player in self.players:
            player.show(self.screen)
            player_sprites.add(player)
        for node in self.nodes:
            node.show(self.screen)
        player_sprites.draw(self.screen)

    def update_timer(self):
        seconds=(pygame.time.get_ticks()-self.start_ticks)/1000 
        if seconds>100: 
            self.running = False