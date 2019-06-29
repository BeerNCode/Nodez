
import pygame

class Controls():

    def __init__(self,keys,joystick,network):
        self.joystick = joystick
        self.keys = keys
        self.network = network