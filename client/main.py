"""where the client pygame GUI starts,

step 1: init pygame, ask for server ip address

step 2: init this client's **server handler**, which
    1. takes the initialized game object as own param.
    2. updates the game, by lazily receiving JSON from server's client handler(later), in a while loop, which blocks by socket.
    3. is a thread (and a child of socket), and runs itself at init, far before we enter while loop. (and is already looping)

step 3: enter pygame while loop
    the game object inited in step 1, updated in step 2(infinitely in another thread), is here updated and drawn out.

we need:
    1. before while loop:
        game object: local_drawgame = DrawGame()
        this client's server handler: my_server_handler = ServerHandler(1. local_drawgame, 2. local ip address, some other stuff)

    2. inside while loop:
        there will be no reference to my_server_handler, while it changes our game object stealthly.
        the only thing we do is drawing out the game object.
"""
import random
import pygame
from server_handler import ServerHandler

import sys
sys.path.append('..')

from server.event_hub import EventHub

server_addr = ('localhost', 12345)

def main():
    pygame.init()
    local_addr = ('localhost', random.randint(10000,20000))
    local_event_hub = EventHub()
    svh = ServerHandler(local_addr, server_addr, local_event_hub)
    svh.start()

    FPS = 20
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        # Game loop part 1: Events #####
        mouseDown = False
        for event in pygame.event.get():
            # this one checks for the window being closed
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseDown = True
                    prevPos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouseDown = False
            # add any other events here (keys, mouse, etc.)

        # Game loop part 2: Updates #####
        # Game loop part 3: Draw #####

        if mouseDown:
            (x, y) = pygame.mouse.get_pos()
            local_event_hub.cur_pos = [x, y]
            pygame.draw.line(screen, BLACK, prevPos, (x, y), LINEWIDTH)
            pygame.draw.circle(screen, BLACK, (x, y), BRUSHRADIUS, 0)
            prevPos = (x, y)
        pygame.display.flip()

    
main()