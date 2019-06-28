import pygame
import sys
from program import Program

if __name__ == "__main__":
    pygame.init()

    p = Program()
    p.run()

    pygame.quit()
    p.socket.close()

    for client in p.clients:
        client.conn.close()
    print("Closing application")
    sys.exit(0)