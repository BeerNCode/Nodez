import pygame
import sys
import game_modes
import network_player
from controls import Controls
from program import Game

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

CONTROLS = [
    {"up": pygame.K_UP,"down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "space": pygame.K_SPACE},
    {"up": pygame.K_w,"down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d, "space": pygame.K_e},
    {"up": pygame.K_t,"down": pygame.K_g, "left": pygame.K_f, "right": pygame.K_h, "space": pygame.K_y},
    {"up": pygame.K_i,"down": pygame.K_k, "left": pygame.K_j, "right": pygame.K_l, "space": pygame.K_o}
]

def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Nodez")
    screen =  pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

    network_player.run_thread()

    setup = False
    selected = "Start"
    playersWaiting = {
        "total":4,
        "remote":0,
        "joysticks":pygame.joystick.get_count()
    }
    pygame.joystick.init()
    i = 0
    while not setup:
        pygame.event.pump()
        
        if not setup:
            pygame.joystick.quit()
            pygame.joystick.init()
            playersWaiting["joysticks"]=pygame.joystick.get_count()
            screen.fill((i%255,i*2%255,i*3%255))
            i = i + 1
            smallText = pygame.font.Font('freesansbold.ttf',50)
            largeText = pygame.font.Font('freesansbold.ttf',115)
            largerText = pygame.font.Font('freesansbold.ttf',200)
            TextSurf, TextRect = text_objects("Node", largeText)
            TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2))
            screen.blit(TextSurf, TextRect)
            TextSurf, TextRect = text_objects("z", largeText)
            TextRect.center = ((SCREEN_WIDTH/2)+200,(SCREEN_HEIGHT/2)+50)
            screen.blit(TextSurf, TextRect)
            TextSurf, TextRect = text_objects(f'Total Required: {playersWaiting["total"]}', smallText)
            TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2)+200)
            screen.blit(TextSurf, TextRect)
            TextSurf, TextRect = text_objects(f'Joysticks Connected: {playersWaiting["joysticks"]}', smallText)
            TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2)+250)
            screen.blit(TextSurf, TextRect)
            TextSurf, TextRect = text_objects(f'Remote Connected: {playersWaiting["remote"]}', smallText)
            TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2)+300)
            screen.blit(TextSurf, TextRect)
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_SPACE]):
               setup = True
        pygame.display.flip()

    # actually make the game
    controls = []
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    for joystick in joysticks:
        joystick.init()
        controls.append(Controls(None, joystick, None))

    for network in network_player.players:
        controls.append(Controls(None, None, network))

    for i in range(0, 4-len(controls)):
        controls.append(Controls(CONTROLS[i], None, None))

    game_mode = game_modes.generate_basic(SCREEN_WIDTH, SCREEN_HEIGHT, controls)

    p = Game(screen, game_mode)
    p.run()

    pygame.quit()
    sys.exit(0)

