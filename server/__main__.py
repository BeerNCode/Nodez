import pygame
import sys
import game_modes
import network_player
from controls import Control
from program import Game

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

CONTROLS = [
    {"up": pygame.K_UP,"down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "space": pygame.K_SPACE},
    {"up": pygame.K_w,"down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d, "space": pygame.K_e},
    {"up": pygame.K_t,"down": pygame.K_g, "left": pygame.K_f, "right": pygame.K_h, "space": pygame.K_y},
    {"up": pygame.K_i,"down": pygame.K_k, "left": pygame.K_j, "right": pygame.K_l, "space": pygame.K_o}
]

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Nodez")
    pygame.joystick.init()
    screen =  pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

    network_player.run_thread()

    while True:
        pass        

    # actually make the game

    controls = []
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    for joystick in joysticks:
        joystick.init()
        controls.append(Control(None, joystick, None))

    for network in network_player.players:
        controls.append(Control(None, None, network))

    for i in range(0, 4-len(controls)):
        controls.append(Control(CONTROLS[i], None, None))

    game_mode = game_modes.generate_basic(SCREEN_WIDTH, SCREEN_HEIGHT, controls)

    p = Game(game_mode)
    p.run()

    pygame.quit()
    sys.exit(0)