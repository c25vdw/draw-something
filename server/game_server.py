"""
GameServer:
    the main thread running a pygame.

    draw_game: the game object, passed to its two client handlers so that it gets modified.
"""
import sys
sys.path.append('..')
from server.client_handler import ClientHandler
from server.event_hub import EventHub
import threading
import socket
import time


class GameServer(threading.Thread, socket.socket):
    TIMEOUT = 2.0
    DEFAULT_PORT = 12345
    BUFFER_SIZE = 1024
    COMMAND_RATE = 60
    COMMAND_CLIENT_CONNECT = "client connect"
    FPS = 1

    def __init__(self, port=None):
        threading.Thread.__init__(self, name="Server thread")
        socket.socket.__init__(self, type=socket.SOCK_DGRAM)

        self.port = self.DEFAULT_PORT if port is None else port
        self.bind(('localhost', self.port))
        self.clients = []
        self.client_handlers = []
        self.player_addresses = {}

        # self.draw_game = DrawGame()
        self.event_hub = EventHub()
    
    def run(self):
        print('Hosting at:', self.getsockname())

        print('Starting server.')

        for i in [1,2]:
            player_id = i

            print('Waiting for client #{}'.format(player_id))
            c = self.wait_client()
            print("client {} connected, ip: {}".format(player_id, c))
            self.clients.append(c)

            print('Initializing client handler id: {} to addr: {}'.format(player_id, c))
            self.create_client_handler(c, player_id)

        for ch in self.client_handlers:
            ch.start()

        print('Starting game.')
        # clock = pygame.time.Clock()
        while True:
            time.sleep(1000)
        return

    def wait_client(self):
        data, addr = self.recvfrom(self.BUFFER_SIZE)
        print('data:', data, 'address_info:', addr)

        if data:
            decoded = data.decode('utf-8')
            if decoded != self.COMMAND_CLIENT_CONNECT:
                raise ValueError('Expecting "{}", but got "{}"'.format(self.COMMAND_CLIENT_CONNECT, decoded))
            # print('Client address found:', address_info)
            return addr

    def create_client_handler(self, client_ip, client_player_id):
        ch = ClientHandler(self.port + client_player_id, client_player_id, client_ip, self.event_hub)
        self.client_handlers.append(ch)
        self.player_addresses[client_player_id - 1] = client_ip
        


def test_import():
    game = DrawGame()
    server = GameServer()
    print(server.event_hub.to_json())

    server.start()

# test_import()