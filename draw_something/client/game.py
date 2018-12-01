import pygame
import time
import socket
import random

from server.event_hub import EventHub
from client.server_handler import ServerHandlerG as ServerHandler
from client.settings import *

class Game:
    """
    there should be the pygame while loop wrapping this.
    """
    FPS = 60
    def __init__(self):
        """
        svh: server_handler, initialized outside by client.
        eh: event_handler, initialized outside by client.

        screen, font, svh, eh
        """
        pygame.init()
        self._init_window() # self.screen
        self._init_components()
        self._init_font() # self.font
        self.eh = EventHub()
        self._init_svh() # self.svh

        # event states
        self.mouse_down = False
        self.prevPos = (None, None)
    
    def _init_window(self):
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.screen.fill(SCREENBG)
        pygame.display.set_caption("Draw something!")
        # may be draw something here.
        pygame.display.flip()
    
    def _init_components(self):
        self.canvas = pygame.Surface((CANVASWIDTH, CANVASHEIGHT))
        self.canvas.fill(CANVASBG)
        
        self.toolbar = pygame.Surface((TOOLBARWIDTH,TOOLBARHEIGHT))
        self.toolbar.fill(ORANGE)
        self.screen.blit(self.toolbar, (MARGIN,MARGIN))

        self.INPUT_BOX = pygame.Surface((INPUTBOXWIDTH,INPUTBOXHEIGHT))
        self.INPUT_BOX.fill(RED)

    def _init_font(self):
        self.font = pygame.font.Font(None, 48)

    def _init_svh(self):
        def get_ip_address():
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_addr = s.getsockname()[0]
            return ip_addr
        local_addr = (get_ip_address(), random.randint(10000, 20000))
        # server_addr = (input("what is the server's ip address?>"), 12345)
        server_addr = ("10.0.0.207", 12345)

        self.svh = ServerHandler(self.eh, local_addr, server_addr)

    def before_loop(self):
        self.svh.start()
        while self.svh.canDraw is None: time.sleep(0.1)

    def handle_pygame_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
        elif not self.svh.canDraw and event.type == pygame.KEYDOWN:
            self._handle_keydown(event)
        elif event.type == pygame.MOUSEBUTTONDOWN or \
             event.type == pygame.MOUSEBUTTONUP:
            self._handle_mouse_up_down(event)
    

    def _handle_keydown(self, event):
        if event.key == pygame.K_RETURN:
            self.eh.flush_input_to_client_answer(self.svh.player_id)
            time.sleep(0.1)
            self.eh.client_answer[str(self.svh.player_id)] = ""
        elif event.key == pygame.K_BACKSPACE:
            print("input: backspace.")
            self.eh.input_txt = self.eh.input_txt[:-1]
        else:
            self.eh.input_txt += event.unicode
        print("input> {}".format(self.eh.input_txt))

    def _handle_mouse_up_down(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.eh.color = BLACK
            elif event.button == 3:
                self.eh.color = CANVASBG
            self.mouse_down = True
            (xp, yp) = pygame.mouse.get_pos()
            self.prevPos = (xp + XPOSOFFSET * -1, yp - MARGIN)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_down = False
            print("mouse up")
    
    def update(self):
        if self.mouse_down:
            (x, y) = pygame.mouse.get_pos()
            # update local cursor position
            self.eh.cur_pos = [(x + XPOSOFFSET * -1, y - MARGIN), self.prevPos]
            self.prevPos = (x + XPOSOFFSET * -1, y - MARGIN)
        else:
            self.eh.cur_pos = [(None, None), (None, None)]

    def draw(self):
        self._draw_sketch() # using svh.cur_pos values.
        self.input_box = self._draw_text() # using svh.input_txt

        self.screen.blit(self.canvas, (XPOSOFFSET,MARGIN))
        self.screen.blit(self.input_box, (XPOSOFFSET, CANVASHEIGHT + MARGIN))

        pygame.display.flip()
    
    def _draw_sketch(self):
        if self.svh.cur_pos != [[None, None], [None, None]]:
            p = self.svh.cur_pos
            pygame.draw.line(self.canvas, self.svh.color, p[0], p[1], LINEWIDTH)
            pygame.draw.circle(self.canvas, self.svh.color, p[1], BRUSHRADIUS, 0)
    def _draw_text(self):
        txt_surface = self.font.render(self.eh.input_txt, True, NAVYBLUE)
        self.input_box = self.INPUT_BOX.copy()
        self.input_box.blit(txt_surface, (0, 0))
        return self.input_box