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
        self._init_font() # self.font
        self.eh = EventHub()
        self._init_svh() # self.svh

        # event states
        self.mouse_down = False
        self.prevPos = (None, None)
    
    def _init_window(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(BGCOLOR)
        pygame.display.set_caption("Draw something!")
        # may be draw something here.
        pygame.display.flip()
    
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
        server_addr = ("10.0.0.172", 12345)

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
            time.sleep(1)
            self.eh.client_answer[str(self.svh.player_id)] = ""
        elif event.key == pygame.K_BACKSPACE:
            print("input: backspace.")
            self.eh.input_txt = self.eh.input_txt[:-1]
        else:
            self.eh.input_txt += event.unicode
        print("input> {}".format(self.eh.input_txt))

    def _handle_mouse_up_down(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_down = True
            self.prevPos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_down = False
                print("mouse up")
    
    def update(self):
        if self.mouse_down:
            (x, y) = pygame.mouse.get_pos()
            # update local cursor position
            self.eh.cur_pos = [(x, y), self.prevPos]
            self.prevPos = (x, y)
        else:
            self.eh.cur_pos = [(None, None), (None, None)]
        ###### seems to be redundant. vv
        # if not pos:
        #     pos = [[0,0], [0,0]]
        # pos: [(x, y), (prev_x, prev_y)]
    
    def draw(self):
        self._draw_sketch() # using svh.cur_pos values.
        self._draw_text() # using svh.input_txt
        pygame.display.flip()
    
    def _draw_sketch(self):
        if self.svh.cur_pos != [[None, None], [None, None]]:
            p = self.svh.cur_pos
            pygame.draw.line(self.screen, BLACK, p[0], p[1], LINEWIDTH)
            pygame.draw.circle(self.screen, BLACK, p[1], BRUSHRADIUS, 0)
    
    def _draw_text(self):
        self.screen.blit(self.font.render("", True, NAVYBLUE), (WIDTH/2, HEIGHT/2))
        txt_surface = self.font.render(self.eh.input_txt, True, NAVYBLUE)
        self.screen.blit(txt_surface, (WIDTH/2, HEIGHT/2))
