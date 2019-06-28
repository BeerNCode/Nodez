#import socket
import pygame
import json
import threading
import logging
import colours
from player import Player

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
        self.players.append(Player())
        self.running = True

    def update(self):
        logger.info("Got update!")

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logger.info("Ending the game.")
                    self.running = False

                if event.type == pygame.VIDEORESIZE:
                    Program.SCREEN_HEIGHT = event.h
                    Program.SCREEN_WIDTH = event.w
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE) 
            
            self.render()

            pygame.display.flip()

    def render(self):
        self.screen.fill(colours.BLACK)

        pygame.draw.ellipse(self.screen, colours.WHITE, [SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 100, 100], 2)

        sprites = pygame.sprite.Group()
        for idx, player in enumerate(self.players):
            player.show(self.screen)
            sprites.add(player)
        sprites.draw(self.screen)