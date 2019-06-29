#import socket
import pygame
import json
import threading
import logging
import colours
import nodes

import maptiles
from team import Team
from player import Player
from maptiles import MapTiles
from nodes import Node
from vector import Vector
import random
import game_modes
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
        self.clock = pygame.time.Clock()
        self.start_ticks=pygame.time.get_ticks()
        self.setup = False
        self.selected = "Start"
        self.playersWaiting = {
            "total":4,
            "remote":0,
            "joysticks":pygame.joystick.get_count()
        }
        pygame.joystick.init()
        i = 0
        while not self.setup:
            pygame.event.pump()
            self.update_events()
            
            if not self.setup:
                pygame.joystick.quit()
                pygame.joystick.init()
                self.playersWaiting["joysticks"]=pygame.joystick.get_count()
                self.screen.fill((i%255,i*2%255,i*3%255))
                i = i + 1
                smallText = pygame.font.Font('freesansbold.ttf',50)
                largeText = pygame.font.Font('freesansbold.ttf',115)
                largerText = pygame.font.Font('freesansbold.ttf',200)
                TextSurf, TextRect = self.text_objects("Node", largeText)
                TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2))
                self.screen.blit(TextSurf, TextRect)
                TextSurf, TextRect = self.text_objects("z", largeText)
                TextRect.center = ((SCREEN_WIDTH/2)+200,(SCREEN_HEIGHT/2)+50)
                self.screen.blit(TextSurf, TextRect)
                TextSurf, TextRect = self.text_objects(f'Total Required: {self.playersWaiting["total"]}', smallText)
                TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2)+200)
                self.screen.blit(TextSurf, TextRect)
                TextSurf, TextRect = self.text_objects(f'Joysticks Connected: {self.playersWaiting["joysticks"]}', smallText)
                TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2)+250)
                self.screen.blit(TextSurf, TextRect)
                TextSurf, TextRect = self.text_objects(f'Remote Connected: {self.playersWaiting["remote"]}', smallText)
                TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2)+300)
                self.screen.blit(TextSurf, TextRect)
                keys = pygame.key.get_pressed()
                if (keys[pygame.K_SPACE]):
                   self.setup = True
            self.update_timer()
            pygame.display.flip()
            self.clock.tick(GAME_SPEED)
        game_mode = game_modes.generate_basic(SCREEN_WIDTH, SCREEN_HEIGHT)
        for node in game_mode["nodes"]:
            self.nodes.append(node)
        for player in game_mode["players"]:
            self.players.append(player)
        for team in game_mode["teams"]:
            self.teams.append(team)
        self.world = game_mode["world"]
        self.running = True
        

    def text_objects(self,text, font):
        textSurface = font.render(text, True, (0,0,0))
        return textSurface, textSurface.get_rect()

    def run(self):

        while self.running:
            pygame.event.pump()
            self.update_events()
            
            for player in self.players:
                player.update(self.world, self.nodes)
            for node in self.nodes:
                node.update()
            self.render()
            
            self.update_timer()
            pygame.display.flip()
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
        node_sprites = pygame.sprite.Group()

        self.world.show(self.screen)
        for node in self.nodes:
            if node.is_placed:
                node.show(self.screen)
                node_sprites.add(node)
        for player in self.players:
            player.show(self.screen)
            player_sprites.add(player)
        player_sprites.draw(self.screen)
        node_sprites.draw(self.screen)

    def update_timer(self):
        seconds=(pygame.time.get_ticks()-self.start_ticks)/1000 
        if seconds>10000: 
            self.running = False