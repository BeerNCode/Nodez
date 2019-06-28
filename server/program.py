#import socket
import pygame
import json
import threading
import logging
import colours
from player import Player
from map import Map
from node import Node

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
BLACK = (10,10,10)
BROWN = (153,76,0)
GREEN = (30,255,30)
BLUE = (30,40,255)
RED = (255,40,55)
COLOURS = {
        OPEN_TILE : BLACK,
        HIGH_NOISE : RED,
        SOURCE_TILE : GREEN,
        SINK_TILE : BLUE
    }
TILESIZE = 40


IP_ADDRESS = "0.0.0.0"
PORT = 5000



logger = logging.getLogger(__name__)

class Program:

    screenSize = (SCREEN_WIDTH, SCREEN_HEIGHT)

    def __init__(self):
        pygame.display.set_caption("Nodez")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        self.players = []
        self.nodes = []
        self.players.append(Player())
        self.running = True

    def update(self):
        logger.info("Got update!")

    def run(self):
        while self.running:
            self.update_events()
            
            for player in self.players:
                node = player.update()
                if node is not None:
                    self.nodes.append(node)
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
        for row in range(map.height): 
            for col in range(map.width):
                pygame.draw.rect(self.screen,COLOURS[map.tilemap[row][col]],(col*map.tilesize,row*map.tilesize,map.tilesize,map.tilesize))
        for player in self.players:
            player.show(self.screen)
        for node in self.nodes:
            node.show(self.screen)
        
