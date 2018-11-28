import socket
from time import sleep
from server.event_hub import EventHub
from server.ch import ClientHandlerG as ClientHandler
from server.huffman_handler import HuffmanHandler

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_addr = s.getsockname()[0]
    return ip_addr

class GameServerG:
    def __init__(self):
        self.sock_for_setup = socket.socket()
        self.sock_for_setup.setblocking(True) # no timeout.
        self.ip = get_ip_address()
        try:
            self.sock_for_setup.bind((self.ip, 12345))
        except:
            self.sock_for_setup.bind((self.ip, 12346))
        self.sock_for_setup.listen(2) # listens on public:12345

        print("listening on address {}".format((self.ip, '12345')))
        self.ch_list = []
        self.eh = EventHub()

        hh = HuffmanHandler()
        self.entries = hh.get_entries()
        self.eh.entries = self.entries # now server event_hub has access to entries(answers)

    def start(self):
        # set up connection,
        # 1. send the client socket their id
        for player in [1,2]:
            (client_sock, client_ip) = self.sock_for_setup.accept()
            ch = ClientHandler(client_sock, player, self.eh)
            self.ch_list.append(ch)
        sleep(1)
        for ch in self.ch_list:
            ch.start()

        while True:
            sleep(1000)
        return
