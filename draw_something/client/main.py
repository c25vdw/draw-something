"""
run client(pygame front end)
this should only be called by ../run_client.py
"""


def run():
    import pygame
    import sys
    from client.game import Game
    g = Game()
    clock = pygame.time.Clock()

    g.before_loop()
    while g.running:
        clock.tick(g.FPS)
        # event handling
        for event in pygame.event.get():
            g.handle_pygame_event(event)
        g.update()
        g.draw()

    pygame.quit()
    sys.exit(0)
