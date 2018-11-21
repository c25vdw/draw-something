import socket
import json
import sys
import pygame as pg
from settings import *

# create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# retrieve local hostname
local_hostname = socket.gethostname()

# get fully qualified hostname
local_fqdn = socket.getfqdn()

# get the according IP address
ip_address = socket.gethostbyname(local_hostname)

# bind the socket to the port 23456, and connect
server_address = (ip_address, 23456)
sock.connect(server_address)
print("connecting to %s (%s) with %s" %
      (local_hostname, local_fqdn, ip_address))

# ----------------------------------------------------------------------------------------

pg.init()

# initialize sound - uncomment if you're using sound
# pg.mixer.init()
# create the game window and set the title
screen = pg.display.set_mode((WIDTH, HEIGHT))
screen.fill(BGCOLOR)
pg.display.set_caption("My Game")
# start the clock
clock = pg.time.Clock()

# set the 'running' variable to False to end the game
running = True
mouseDown = False
while running:
    clock.tick(FPS)
    # Game loop part 1: Events #####
    for event in pg.event.get():
        # this one checks for the window being closed
        if event.type == pg.QUIT:
            pg.quit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouseDown = True
                prevPos = pg.mouse.get_pos()
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                mouseDown = False
        # add any other events here (keys, mouse, etc.)

    # Game loop part 2: Updates #####
    # Game loop part 3: Draw #####

    if mouseDown:
        (x, y) = pg.mouse.get_pos()
        pg.draw.line(screen, BLACK, prevPos, (x, y), LINEWIDTH)
        pg.draw.circle(screen, BLACK, (x, y), BRUSHRADIUS, 0)
        data = [(x, y), prevPos]
        data_string = json.dumps({"pos": data})
        sock.sendall(data_string.encode())
        prevPos = (x, y)
    pg.display.flip()

    # wait for two seconds

# close connection
sock.close()
pg.quit()
