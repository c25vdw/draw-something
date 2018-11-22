import random
import pygame
from server_handler import ServerHandler
import sys
sys.path.append('..')
from server.event_hub import EventHub


WIDTH = 300
HEIGHT = 400
BGCOLOR = (200, 200, 200)
BLACK = (0, 0, 0)
BRUSHWIDTH = 25
BRUSHOFFSET = 1
LINEWIDTH = BRUSHWIDTH - BRUSHOFFSET
BRUSHRADIUS = int(BRUSHWIDTH/2-BRUSHOFFSET*4)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BGCOLOR)
pygame.display.set_caption("Draw Something!")


server_addr = ('localhost', 12345)
pygame.init()
local_addr = ('localhost', random.randint(10000, 20000))
local_event_hub = EventHub()
svh = ServerHandler(local_addr, server_addr, local_event_hub)
svh.start()

FPS = 60
clock = pygame.time.Clock()
mouseDown = False
while True:
    if svh.canDraw is None:
        continue
    clock.tick(FPS)
    # Game loop part 1: Events #####
    for event in pygame.event.get():
        # this one checks for the window being closed
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown = True
            prevPos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouseDown = False
                print("mouse up")
        # add any other events here (keys, mouse, etc.)

    # Game loop part 2: Updates #####
    # Game loop part 3: Draw #####

    if mouseDown:
        (x, y) = pygame.mouse.get_pos()
        data = [(x, y), prevPos]
        local_event_hub.cur_pos = data
        prevPos = (x, y)
        print(data)
    else:
        # print(svh.cur_pos)
        data = [(None, None), (None, None)]
        local_event_hub.cur_pos = data

    pos = svh.cur_pos

    if pos != [[None, None], [None, None]]:

        pygame.draw.line(screen, BLACK, pos[0], pos[1], LINEWIDTH)
        pygame.draw.circle(screen, BLACK, pos[1], BRUSHRADIUS, 0)

    pygame.display.flip()
pygame.quit()
