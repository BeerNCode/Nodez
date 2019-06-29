
import pygame

class Controls():

    def __init__(self,controls,joystick):
        self.joystick = joystick
        self.controls = controls
        
    def hasGamepad(self):
        return not (self.joystick is None)

    def getKeys(self):
        return self.controls

    def getGamepad(self):
        return self.joystick