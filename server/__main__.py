import pygame
import sys
from program import Program

if __name__ == "__main__":
    pygame.init()

    p = Program()
    p.run()

    pygame.quit()
    sys.exit(0)