import socket
import pygame
import json
import threading
import clients
import logging

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
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        self.clients = []
        self.new_clients_thread = threading.Thread(target=self.listen_for_new_clients)
        self.new_clients_thread.start()
        self.running = True
        pygame.display.set_caption("Super Nash Bros 2")

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
        pass

    def listen_for_new_clients(self):
        self.socket.bind((IP_ADDRESS, PORT))
        self.socket.listen(5)
        self.socket.settimeout(CLIENT_TIMEOUT)
        while self.running:
            try:
                logger.info(f"Listening for connection....")
                connection, ip_address = self.socket.accept()
                logger.info(f"Received connection from [{ip_address}]")
                client = clients.Client(connection, ip_address)
                client.connection.settimeout(CLIENT_TIMEOUT)
                client.start_listening()
                self.clients.append(client)

            except Exception as e:
                logger.error("Unable to connect to client.")
                logger.debug(e.args)



