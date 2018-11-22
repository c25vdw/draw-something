import random
import pygame
from server_handler import ServerHandler
import sys
sys.path.append('..')
from server.event_hub import EventHub


WIDTH = 300
HEIGHT = 400
BGCOLOR = (200,200,200)
BLACK = (0,0,0)
LINEWIDTH = 40
BRUSHRADIUS = 25

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BGCOLOR)
pygame.display.set_caption("Draw Something!")

def main():
    server_addr = ('localhost', 12345)
    pygame.init()
    local_addr = ('localhost', random.randint(10000,20000))
    local_event_hub = EventHub()
    svh = ServerHandler(local_addr, server_addr, local_event_hub)
    svh.start()

    FPS = 20
    clock = pygame.time.Clock()
    while True:
        if svh.canDraw is None: continue
        clock.tick(FPS)
        # Game loop part 1: Events #####
        mouseDown = False
        for event in pygame.event.get():
            # this one checks for the window being closed
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and svh.canDraw:
                if event.button == 1:
                    mouseDown = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouseDown = False
            # add any other events here (keys, mouse, etc.)

        # Game loop part 2: Updates #####
        # Game loop part 3: Draw #####
        x, y = 0, 0
        if mouseDown:
            (x, y) = pygame.mouse.get_pos()
            local_event_hub.cur_pos = [x, y]
        else:
            # print(svh.cur_pos)
            x, y = svh.cur_pos
        if x is None and y is None: continue
        
        pygame.draw.circle(screen, BLACK, (x, y), BRUSHRADIUS, 0)
        pygame.display.flip()

    
main()