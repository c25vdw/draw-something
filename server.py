import socket
import sys
import json
import pygame as pg
from ast import literal_eval
from settings import *

# define some colors (R, G, B)

# initialize pygame

# ---------------------------------CONNECTION STUFFS--------------------------------------
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

local_hostname = socket.gethostname()

local_fqdn = socket.getfqdn()

ip_address = socket.gethostbyname(local_hostname)

print("working on %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))

server_address = (ip_address, 23456)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

sock.listen(1)
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
connection, client_address = sock.accept()
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
    data = connection.recv(64)
    data = json.loads(data.decode())
    pos = data.get("pos")
    if data:
        pg.draw.line(screen, BLACK, pos[0], pos[1], LINEWIDTH)
        pg.draw.circle(screen, BLACK, pos[1], BRUSHRADIUS, 0)
    # print('waiting for a connection')
    # connection, client_address = sock.accept()

    # # show who connected to us
    # print('connection from', client_address)

    # receive the data in small chunks and print it
    # while True:

    #     print(pos)

    #     else:
    #         # no more data -- quit the loop
    #         print("no more data.")
    #         break
    pg.display.flip()


pg.quit()
