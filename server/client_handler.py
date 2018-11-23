import threading
import socket
import json
from pygame.time import Clock
import random
class ClientHandler(socket.socket, threading.Thread):
    BUFFER_SIZE = 2048
    FPS = 60
    def __init__(self, port, player_id, client_ip, event_hub):
        socket.socket.__init__(self, type=socket.SOCK_DGRAM)
        threading.Thread.__init__(self, name='ClientHandler')
        self.settimeout(None)
        self.bind(('localhost', port))
        self.setDaemon(True)

        self.player_id = player_id
        self.client_ip = client_ip
        self.event_hub = event_hub
        self.port = port

        self.canDraw = (self.player_id == self.event_hub.drawer_id)
        self.send_client_player_id()
        self.cached_client_eh = None
        self.oldCanDraw = self.canDraw

    def send_client_player_id(self):
        self.sendto(str(self.player_id).encode('utf-8'), self.client_ip)

    def run(self):
        clock = Clock()
        while True:
            clock.tick(self.FPS)
            self.send_update_to_client()
            cu, client_addr = self.receive_client_update()  # blocks
            self.update_with_client_update(cu)

    def send_update_to_client(self):
        self.sendto(self.event_hub.to_json().encode('utf-8'), self.client_ip)

    def receive_client_update(self):
        data, addr = self.recvfrom(self.BUFFER_SIZE)
        if data:
            decoded = data.decode('utf-8')
            try:
                cu = json.loads(decoded)
            except ValueError as err:
                print(err)
                raise ValueError(
                    'Expecting a JSON string from client, but got something else:', decoded)
            return cu, addr
        return None, None

    def generate_answer(self):
        self.event_hub.answer = "cat"
        return 

    def update_with_client_update(self, client_update_json):
        if not self.canDraw:
            self.check_client_answer(self.event_hub.client_answer)
        self.canDraw = (self.event_hub.drawer_id == self.player_id)

        # TODO: add client guesser's upload
        if (self.canDraw):
            self.event_hub.cur_pos = client_update_json["cur_pos"]
            self.event_hub.color = client_update_json["color"]
        else:
            self.event_hub.input_txt = client_update_json["input_txt"]
            self.event_hub.client_answer = client_update_json["client_answer"]
            
        self.cached_client_eh = client_update_json

    def check_client_answer(self, ca):
        if self.event_hub.compare_then_update_answer(ca):
            print("player {}: correct answer".format(self.player_id))
            self.event_hub.client_answer = ""

            if self.event_hub.drawer_id == 1:
                self.event_hub.drawer_id = 2
            else:
                self.event_hub.drawer_id = 1

            return
