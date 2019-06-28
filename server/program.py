#import socket
import pygame
import json
import threading
import logging
import colours
from player import Player
from node import Node

from tools import *

logging.basicConfig(level=logging.DEBUG)

CLIENT_TIMEOUT = 1000
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
GAME_SPEED = 30

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

        for player in self.players:
            player.show(self.screen)
        for node in self.nodes:
            node.show(self.screen)