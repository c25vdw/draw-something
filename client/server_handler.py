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
    def __init__(self, client_ip, server_ip, local_draw_game, local_actions,): # more
        pass

