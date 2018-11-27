import threading
import socket
import json
from time import sleep
from event_hub import EventHub

def get_first_json_string(json_str):
    brackets = 0
    end = 0
    for i, char in enumerate(json_str):
        if char == "{":
            brackets += 1
        elif char == "}":
            brackets -= 1
        
        if brackets == 0:
            end = i
            break
    return json_str[:end] + '}'
            

class ClientHandlerG(threading.Thread):
    BUFFER_SIZE = 1024
    def __init__(self, client_sock, player_id, event_hub):
        threading.Thread.__init__(self, name="client handler")
        self.sock = client_sock
        self.player_id = player_id
        self.eh = event_hub

    def check_client_answer(self, ca):
        if self.eh.compare_then_update_answer(ca):
            print("player {}: correct answer".format(self.player_id))
            self.eh.client_answer = ""

            if self.eh.drawer_id == 1:
                self.eh.drawer_id = 2
            else:
                self.eh.drawer_id = 1
            
            return
    
    def run(self):
        # send player id: either 1 or 2, then connection should start
        self.sock.send(str(self.player_id).encode('utf-8'))
        sleep(1)
        while True:
            self.sock.send(self.eh.to_json().encode('utf-8')) # send update to sh
            eh_snap_raw = self.sock.recv(self.BUFFER_SIZE) # receive from client update
            eh_snap = eh_snap_raw.decode('utf-8')
            eh_snap = get_first_json_string(eh_snap)
            eh_snap = json.loads(eh_snap)
            self.canDraw = (self.player_id == eh_snap["drawer"])
            # print("receiving eh snap: ", eh_snap, type(eh_snap))
            # if self.eh.
            if not self.canDraw:
                self.check_client_answer(self.eh.client_answer)

            self.canDraw = (self.eh.drawer_id == self.player_id)
            
            if self.canDraw:
                self.eh.cur_pos = eh_snap["cur_pos"]  # array(tuple(2), tuple(2))
                self.eh.color = eh_snap["color"]
                self.eh.input_txt = eh_snap["input_txt"]  # array(3)
            else:
                self.eh.client_answer = eh_snap["client_answer"] # later
                self.eh.input_txt = eh_snap["input_txt"] # later
                # print(eh_snap["input_txt"]) 
            self.eh.drawer = eh_snap["drawer"]  # int
            self.eh.score = eh_snap["score"] # later

            self.sock.send(self.eh.to_json().encode('utf-8'))
