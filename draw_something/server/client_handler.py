import threading
import socket
import json
from time import sleep
import sys
from server.event_hub import EventHub

def empty_answer(client_answer):
    for answer in client_answer:
        client_answer[answer] =""

class ClientHandlerG(threading.Thread):
    BUFFER_SIZE = 1024
    def __init__(self, client_sock, player_id, event_hub):
        threading.Thread.__init__(self, name="client handler")
        self.sock = client_sock
        self.player_id = player_id
        self.eh = event_hub

    def check_client_answer(self, ca, eh_snap):
        if self.eh.compare_then_update_answer(ca,self.player_id):
            print(ca)
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
        sleep(1)
        self.sock.sendall(self.eh.to_json().encode())
        while True:
            # self.sock.sendall(self.eh.to_json().encode()) # send update to sh
            self.sock.sendall(self.eh.to_json().encode())

            eh_snap = self.wait_for_eh_snap() # wait and parse eh from client.

            # print("receiving eh snap: ", eh_snap, type(eh_snap))
            # if self.eh.
            self.check_client_answer(eh_snap.get("client_answer")[str(self.player_id)],eh_snap)
            
            self.canDraw = (self.eh.drawer_id == self.player_id)

            if self.canDraw:
                self.eh.cur_pos = eh_snap.get("cur_pos")  # array(tuple(2), tuple(2))
                self.eh.color = eh_snap.get("color")
            else: # later
                self.eh.input_txt = eh_snap.get("input_txt") 
                # later
                # print(eh_snap["input_txt"]) 
            # self.eh.drawer_id = eh_snap.get("drawer_id")  # int
            # self.eh.score = eh_snap.get("score") # later
            # self.sock.sendall(self.eh.to_json().encode())
            
