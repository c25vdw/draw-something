import random
import pygame
import time
from server_handler import ServerHandler

import sys
sys.path.append('..')
from server.event_hub import EventHub
from settings import *
from utils import *

# pygame initialization
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BGCOLOR)
pygame.display.set_caption("Draw Something!")
pygame.init()
font = pygame.font.Font(None, 32)

# svh init - communication with server
server_addr = ('localhost', 12345)
local_addr = ('localhost', random.randint(10000, 20000))
local_event_hub = EventHub()
svh = ServerHandler(local_addr, server_addr, local_event_hub)
svh.start()

# state variables
mouseDown = False
prevPos = (None, None)

# wait for server setup
while svh.canDraw is None: time.sleep(0.1)

# game start
clock = pygame.time.Clock()
once = True
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif not svh.canDraw and event.type == pygame.KEYDOWN:
            parse_input_event(event, local_event_hub)
        else:
            mouseDown, prevPos = parse_drag_event(event, mouseDown, prevPos)

    # just to make this shorter.
    prevPos = update_cursors_from_mouseDown(mouseDown, prevPos, local_event_hub)
    # print(svh.correct, svh.score, svh.input_text)
    
    # now cur_pos is syncd with server.
    pos = svh.cur_pos # [(x, y), (prev_x, prev_y)]

    print(svh.canDraw)
    # draw lines according to two points.
    draw_the_drags_from_pos(pos, screen)
    draw_input_from_eh(local_event_hub, screen, font)
    pygame.display.flip()

pygame.quit()
