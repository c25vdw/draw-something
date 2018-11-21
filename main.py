import sys
import pygame as pg
from settings import *

# define some colors (R, G, B)

# initialize pygame
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
# start the game loop
while running:
    # keep the loop running at the right speed
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
        prevPos = (x, y)
    pg.display.flip()

# close the window
pg.quit()
