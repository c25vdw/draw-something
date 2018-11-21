import socket
import threading
"""
ServerHandler:
    own ip address
    server ip address
    game object

the run() function should be a while loop, which:
    1. receive updates from server's client handler,
    2. update the local game object(which is exposed to main)
    3. send actions from client, to server's client handler.
"""

class ServerHandler(socket.socket, threading.Thread):
    def __init__(self, client_ip, server_ip): # more
        socket.socket.__init__(self, type=socket.SOCK_DGRAM)
        threading.Thread.__init__(self)
        self.settimeout(2)
        self.setDaemon(True)
        self.bind(client_ip)
        self.server_ip = server_ip
        self.player_id = -1

    def run(self):
        self.connect()
        self.player_id = self.receive_player_id()
        while True:
            game_update_json = self.receive_game_update_json()
            self.pong_world.update_with_json(game_update_json)
            self.send_client_command()

    def receive_game_update_json(self):
        pass
    
    def receive_player_id(self):
        pass

