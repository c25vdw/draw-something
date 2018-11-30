import threading
import socket
import json
from time import sleep
import sys
from server.event_hub import EventHub
from client.game import FPS

def empty_answer(client_answer):
    for answer in client_answer:
        client_answer[answer] = ""

class ClientHandlerG(threading.Thread):
    BUFFER_SIZE = 1024
    def __init__(self, client_sock, player_id, event_hub):
        threading.Thread.__init__(self, name="client handler")
        self.sock = client_sock
        self.player_id = player_id
        self.eh = event_hub

    def check_client_answer(self, client_answer):
        if self.eh.compare_then_update_answer(client_answer,self.player_id):
            print("player {}: correct answer".format(self.player_id))
            if self.eh.drawer_id < self.eh.player_num:
                self.eh.drawer_id += 1
            elif self.eh.drawer_id == self.eh.player_num:
                self.eh.drawer_id = 1
            print("Player id: ",self.player_id)
            print("Current drawer: ",self.eh.drawer_id)
        return

    def wait_for_eh_snap(self):
        eh_snap_raw = self.sock.recv(self.BUFFER_SIZE) # receive from client update
        eh_snap = eh_snap_raw.decode()
        # eh_snap = get_first_json_string(eh_snap)
        eh_snap = json.loads(eh_snap)

        return eh_snap

    def run(self):
        # send player id: either 1 or 2, then connection should start
        self.sock.sendall(str(self.player_id).encode())
        sleep(0.5)

        self.sock.sendall(self.eh.to_json().encode())
        sleep(0.5)

        while True:
            self.sock.sendall(self.eh.to_json().encode('utf-8')) # send update to sh

            eh_snap = self.wait_for_eh_snap() # wait and parse eh from client.

            self.check_client_answer(eh_snap.get("client_answer")[str(self.player_id)])

            self.update_can_draw() # self.canDraw changed here.
            self.update_eh_from_snap(eh_snap) # depends on self.canDraw
    
    def update_can_draw(self):
        self.canDraw = (self.eh.drawer_id == self.player_id)

    def update_eh_from_snap(self, eh_snap):
        ''' eh_snap is the client eventhub copy we receive. decide which to take into server's eventhub.
        '''
        if self.canDraw:
            self.eh.cur_pos = eh_snap.get("cur_pos")  # array(tuple(2), tuple(2))
            self.eh.color = eh_snap.get("color")
        else:
            self.eh.input_txt = eh_snap.get("input_txt")
            
