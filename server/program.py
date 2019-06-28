#import socket
import pygame
import json
import threading
import logging
import colours
import nodes
from team import Team
from player import Player
from map import Map
from nodes import Node
from vector import Vector
import random

from tools import *

logging.basicConfig(level=logging.DEBUG)

CLIENT_TIMEOUT = 1000
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
GAME_SPEED = 30

OPEN_TILE = 0
HIGH_NOISE = 1
SOURCE_TILE = 2
SINK_TILE = 3
PINK = (255,72,196)
YELLOW = (243,234,95)
PURPLE = (192,77,249)
BLUE = (43,209,252)
RED = (255,63,63)
COLOURS = {
        OPEN_TILE : PINK,
        HIGH_NOISE : YELLOW,
        SOURCE_TILE : PURPLE,
        SINK_TILE : BLUE
    }
TILESIZE = 40

NUMBER_OF_NODES = 20

logger = logging.getLogger(__name__)

class Program:

    screenSize = (SCREEN_WIDTH, SCREEN_HEIGHT)

    def __init__(self):
        pygame.display.set_caption("Nodez")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        self.teams = []
        self.players = []
        self.nodes = []

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

        self.players.append(Player("Dave",self.teams[0],{"up": pygame.K_UP,"down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "space": pygame.K_SPACE}))
        self.players.append(Player("Tom",self.teams[1], {"up": pygame.K_w,"down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d, "space": pygame.K_g}))
        self.running = True

    def update(self):
        logger.info("Got update!")

    def run(self):
        while self.running:
            self.update_events()
            
            for player in self.players:
                player.update(self.nodes)
            for node in self.nodes:
                node.update()



            self.render()

            pygame.display.flip()

    def update_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.info("Ending the game.")
                self.running = False

            if event.type == pygame.VIDEORESIZE:
                Program.SCREEN_HEIGHT = event.h
                Program.SCREEN_WIDTH = event.w
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    def render(self):
        self.screen.fill(colours.BLACK)

        map = Map()
        map.show(self.screen)
        for player in self.players:
            player.show(self.screen)
        for node in self.nodes:
            node.show(self.screen)