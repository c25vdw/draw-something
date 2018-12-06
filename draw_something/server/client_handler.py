import threading
import json
import pygame
import math
from time import sleep

class ClientHandlerG(threading.Thread):
    BUFFER_SIZE = 1024
    COUNTDOWN = 15

    def __init__(self, client_sock, player_id, event_hub):
        threading.Thread.__init__(self, name="client handler")
        self.daemon = True
        self.sock = client_sock
        self.player_id = player_id
        self.eh = event_hub
        self.should_stop = False

    def check_client_answer(self, client_answer):
        if self.eh.compare_then_update_answer(client_answer, self.player_id):
            print("player {}: correct answer".format(self.player_id))
            if self.eh.drawer_id < self.eh.player_num:
                self.eh.drawer_id += 1
            elif self.eh.drawer_id == self.eh.player_num:
                self.eh.drawer_id = 1
            print("Current drawer: ", self.eh.drawer_id)
            # increment score of this client.
            self.eh.score[str(self.player_id)] += 1
            self.eh.ticking = False
            print("current score: ", self.eh.score)
            return

    def server_send_answer(self):
        self.eh.update_answer()
        if self.eh.drawer_id < self.eh.player_num:
            self.eh.drawer_id += 1
        elif self.eh.drawer_id == self.eh.player_num:
            self.eh.drawer_id = 1
        return

    def wait_for_eh_snap(self):
        # receive from client update
        try:
            eh_snap_raw = self.sock.recv(self.BUFFER_SIZE)
        except ConnectionResetError:
            self.ends_and_wait_for_gameserver_ends()
        eh_snap = eh_snap_raw.decode()
        # eh_snap = get_first_json_string(eh_snap)
        try:
            eh_snap = json.loads(eh_snap)
        except json.decoder.JSONDecodeError:
            self.ends_and_wait_for_gameserver_ends()
        return eh_snap

    def ends_and_wait_for_gameserver_ends(self):
        self.should_stop = True
        sleep(1000)

    def run(self):
        # send player id: either 1 or 2, then connection should start
        self.sock.sendall(str(self.player_id).encode())
        sleep(0.5)

        self.sock.sendall(self.eh.to_json().encode())
        sleep(0.5)
        pygame.init()
        self.start_time = pygame.time.get_ticks()
        self.times_up = False
        self.toggle_tick = True
        self.should_compute_winner = True
        while True:
            self.sock.sendall(self.eh.to_json().encode(
                'utf-8'))  # send update to sh

            eh_snap = self.wait_for_eh_snap()  # wait and parse eh from client.

            if eh_snap.get("restart_timer"):
                self.start_time = pygame.time.get_ticks()
                self.times_up = False

            if eh_snap.get("correct") == False:
                self.time_passed = (pygame.time.get_ticks(
                ) - self.start_time) / 1000  # time counter

            if self.time_passed < self.COUNTDOWN and eh_snap.get("correct") == False:
                self.eh.count_down = math.trunc(
                    self.COUNTDOWN - self.time_passed)
                self.check_client_answer(eh_snap.get(
                    "client_answer")[str(self.player_id)])
                self.update_can_draw()  # self.canDraw changed here.
                self.update_eh_from_snap(eh_snap)  # depends on self.canDraw
            elif self.time_passed > 15:
                self.eh.ticking = False
                if self.player_id == 1 and self.times_up == False:
                    self.server_send_answer()
                    self.times_up = True
                self.update_can_draw()  # self.canDraw changed here.
                self.update_eh_from_snap(eh_snap)  # depends on self.canDraw

            if self.player_id == 1 and self.COUNTDOWN - self.time_passed <= 5 and eh_snap.get("correct") == False:
                if self.toggle_tick == True:
                    self.tick_start = pygame.time.get_ticks()
                    self.toggle_tick = False
                elif self.toggle_tick == False:
                    self.tick_passed = pygame.time.get_ticks() - self.tick_start
                    if self.tick_passed >= 200:
                        self.eh.ticking = not eh_snap.get("ticking")
                        print(self.eh.ticking)
                        self.toggle_tick = True

            if self.player_id ==1 and self.eh.end_game and self.should_compute_winner:
                self.compute_winner()
                self.should_compute_winner = False

    def update_can_draw(self):
        self.canDraw = (self.eh.drawer_id == self.player_id)

    def update_eh_from_snap(self, eh_snap):
        ''' eh_snap is the client eventhub copy we receive. decide which to take into server's eventhub.
        '''
        if self.canDraw:
            # array(tuple(2), tuple(2))
            self.eh.cur_pos = eh_snap.get("cur_pos")
            self.eh.color = eh_snap.get("color")
        else:
            self.eh.input_txt = eh_snap.get("input_txt")

    def compute_winner(self):
        score = self.eh.score
        temp_winner = max(score, key=score.get)
        for i in score:
            if score[i] == score[temp_winner]:
                self.eh.winner.append(i)
