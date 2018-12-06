import pygame
import pygame.gfxdraw
import time
import socket
import random
from pathlib import Path

from server.event_hub import EventHub
from client.server_handler import ServerHandlerG as ServerHandler
from client.settings import *
from client.components.InfoScreen import InfoScreen
from client.components.InputBox import InputBox


class Game:
    """
    there should be the pygame while loop wrapping this.
    """
    FPS = 60
    DISPLAY_TIMEOUT = 4000

    def __init__(self):
        """
        svh: server_handler, initialized outside by client.
        eh: event_handler, initialized outside by client.

        screen, font, svh, eh
        """
        pygame.init()
        pygame.mixer.init()
        self._init_window()  # self.screen
        self._init_font()  # self.font
        self.eh = EventHub()
        self._init_svh()  # self.svh
        self._init_components()  # self.canvas, toolbar and INPUT_BOX
        self._init_matrix_for_brush()
        # self.input = Text(400, 60, self.font, (WIDTH/2, HEIGHT/2))
        # event states
        self.mouse_down = False
        self.prevPos = (None, None)
        self.running = True
        # for round change event
        self.drawer_changed = False
        self.prev_drawer_id = -1  # initialized in self.beforeloop()
        self.drawer_changed_timestamp = pygame.time.get_ticks()
        self.prev_answer = ""

    def _init_window(self):
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.screen.fill(SCREENBG)
        pygame.display.set_caption("Draw something!")
        # may be draw something here.
        pygame.display.flip()

    def _init_components(self):
        self.INFO_BAR = pygame.Surface((INFOBARWIDTH, INFOBARHEIGHT))
        self.INFO_BAR.fill(INFOBARBG)
        self.TIMER_BOX = self.INFO_BAR.subsurface(
            (INFOBARWIDTH - TIMERBOXWIDTH) / 2, (INFOBARHEIGHT - TIMERBOXHEIGHT) / 2, TIMERBOXWIDTH, TIMERBOXHEIGHT)
        self.TIMER_BOX.fill(WHITE)

        self.canvas = pygame.Surface((CANVASWIDTH, CANVASHEIGHT))
        self.canvas.fill(CANVASBG)
        # self.info_screen = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
        # self.info_screen.fill(YELLOW_1)

        self.info_screen = InfoScreen(
            SCREENWIDTH, SCREENHEIGHT, self.screen, self.svh, timeout=self.DISPLAY_TIMEOUT)

        self.input_box = InputBox(self.screen, self.font_path_roboto)

    def _init_font(self):
        # resolve font file path
        self.font_path_roboto = str(
            Path('./client/fonts/Roboto.ttf').resolve())
        self.font_path_luna = str(Path('./client/fonts/Luna.ttf').resolve())

        self.font = pygame.font.Font(None, 48)
        self.desc_font = pygame.font.Font(self.font_path_roboto, 16)

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

    def _init_matrix_for_brush(self):
        self.matrix = []
        x, y = -1, 1
        for i in range(0, 3):
            for j in range(0, 3):
                self.matrix.append([x + j, y])
            y -= 1

    def before_loop(self):
        self.svh.start()
        while self.svh.canDraw is None:
            time.sleep(0.1)
        self.prev_drawer_id = self.svh.drawer_id

    def handle_pygame_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
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
            self.prevPos = (xp, yp - YOFFSET)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_down = False
            print("mouse up")

    def update(self):
        if self.mouse_down:
            (x, y) = pygame.mouse.get_pos()
            # update local cursor position
            self.eh.cur_pos = [(x, y - YOFFSET), self.prevPos]
            self.prevPos = (x, y - YOFFSET)
        else:
            self.eh.cur_pos = [(None, None), (None, None)]

        self._update_drawer_changed()  # draw depends on self.drawer_changed
        self.input_box.update(self.eh.input_txt)

        if not self.drawer_changed and self.prev_answer != self.svh.answer:
            self.prev_answer = self.svh.answer  # cache the answer for previous round

    def _update_drawer_changed(self):
        self.eh.restart_timer = False
        if self.svh.drawer_id != self.prev_drawer_id:
            self.drawer_changed = True
            self.drawer_changed_timestamp = pygame.time.get_ticks()
        if self.drawer_changed:
            self.eh.correct = True
            time_past = pygame.time.get_ticks() - self.drawer_changed_timestamp
            if time_past > self.info_screen.timeout:
                self.drawer_changed = False
                self.eh.restart_timer = True
                self.eh.correct = False

        self.prev_drawer_id = self.svh.drawer_id

    def draw(self):
        self.screen.fill(SCREENBG)
        if self.drawer_changed:
            self.canvas.fill(CANVASBG)
            self._draw_info_screen()
        else:
            self._draw_sketch()  # using svh.cur_pos values.

            self.info_bar = self._draw_info_bar()
            self.screen.blit(self.info_bar, (0, 0))
            self.screen.blit(self.canvas, (0, INFOBARHEIGHT))
            if not self.svh.canDraw:
                self.input_box.draw()

        pygame.display.flip()

    def _draw_info_screen(self):
        # self.screen.fill(WHITE)
        # self.screen.blit(self.info_screen, (0, 0))
        self.info_screen.draw(self.prev_answer)

    def _draw_info_bar(self):
        # drawing role
        if self.svh.canDraw:
            drawing_role = self.desc_font.render(
                "Draw: {}".format(self.svh.answer), True, INFOBAR_TEXTCOLOR)
        else:
            drawing_role = self.desc_font.render(
                "Your turn to guess!", True, INFOBAR_TEXTCOLOR)
        # timer box
        self.timer_box = self._draw_timer_box()
        # round number
        round_number = self.desc_font.render(
            "Round: {}/{}".format(self.svh.cur_ans_index + 1, self.svh.entry_length), True, INFOBAR_TEXTCOLOR)
        round_number_width = round_number.get_width()
        # info bar copy
        self.info_bar = self.INFO_BAR.copy()
        # blitting onto info bar
        self.info_bar.blit(drawing_role, (20, 15))
        self.info_bar.blit(round_number, (INFOBARWIDTH -
                                          round_number_width - 20, 15))
        self.info_bar.blit(self.timer_box, ((
            INFOBARWIDTH - TIMERBOXWIDTH) / 2, (INFOBARHEIGHT - TIMERBOXHEIGHT) / 2))
        # info bar bottom border
        pygame.draw.rect(self.info_bar, INFOBAR_BORDERCOLOR, (0, INFOBARHEIGHT -
                                                              INFOBAR_BORDERHEIGHT, INFOBAR_BORDERWIDTH, INFOBAR_BORDERHEIGHT), 0)
        return self.info_bar

    def _draw_timer_box(self):
        self.timer_box = self.TIMER_BOX.copy()
        formatted_time = str(self.svh.count_down).zfill(
            2)  # add leading 0 to single digit number
        if self.svh.ticking == True:
            self.eh.ticking = True
            count_down = self.desc_font.render(
                "00:{}".format(formatted_time), True, RED)
        elif self.svh.ticking == False:
            self.eh.ticking = False
            count_down = self.desc_font.render(
                "00:{}".format(formatted_time), True, BLACK)
        count_down_width = count_down.get_width()
        count_down_height = count_down.get_height()
        self.timer_box.blit(count_down, ((
            TIMERBOXWIDTH - count_down_width) / 2, (TIMERBOXHEIGHT - count_down_height) / 2))
        self._draw_timer_box_border()
        return self.timer_box

    def _draw_timer_box_border(self):
        pygame.draw.rect(self.timer_box, INFOBAR_BORDERCOLOR,
                         (0, 0, TIMERBOXWIDTH, TIMERBOX_BORDER), 0)
        pygame.draw.rect(self.timer_box, INFOBAR_BORDERCOLOR,
                         (0, 0, TIMERBOX_BORDER, TIMERBOXHEIGHT), 0)

    def _draw_sketch(self):
        if self.svh.cur_pos != [[None, None], [None, None]]:
            p = self.svh.cur_pos
            for i in range(0, 9):
                pygame.draw.aaline(self.canvas, self.svh.color, (p[0][0] + self.matrix[i][0], p[0][1] +
                                                                 self.matrix[i][1]), (p[1][0] + self.matrix[i][0], p[1][1] + self.matrix[i][1]), 1)
