import socket
from random import randint
from time import sleep
import sys

from server.client_handler import ClientHandlerG as ClientHandler
from server.huffman_handler import HuffmanHandler
from server.event_hub import EventHub


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_addr = s.getsockname()[0]
    return ip_addr


class GameServerG:
    def __init__(self):
        self.player_num = int(input("Enter number of players: "))
        self.level = self.get_level(default=2)
        print("level is: ",self.level)
        self.ch_list = []
        self.eh = EventHub()

        self.init_sock_for_setup()
        self.init_eh_entries()
        self.init_player_props()
        # now server event_hub has access to entries(answers), selected_entry

    def get_level(self, default=2):
        level = input("Nice!\nNow enter difficulty(1 to 3, default 2) > ")
        def error_exit():
            print("should be a integer between 1 and 3.")
            sys.exit(1)
        if level is '':
            error_exit()
        else:
            level = int(level)
            if level > 3 or level < 1:
                error_exit()
            return level

    def init_eh_entries(self):
        ''' read from compressed file and create {entries}, {selected_entry} attributes for self.eh
            these are not present on clients' event hub.
        '''
        hh = HuffmanHandler()
        self.eh.entries = hh.get_entries()
        # self._choose_random_entry()
        self._choose_entry_from_level()

    def init_sock_for_setup(self):
        '''create self.sock_for_setup, start listening on port 12345'''
        self.sock_for_setup = socket.socket()
        self.sock_for_setup.setblocking(True)  # no timeout.
        self.ip = get_ip_address()
        self.sock_for_setup.bind((self.ip, 12345))

        self.sock_for_setup.listen(self.player_num)  # listens on public:12345
        print("listening for {} clients on address: {}".format(self.player_num, (self.ip, '12345')))

    def _choose_entry_from_level(self):
        self.eh.selected_entry = self.eh.entries[str(self.level)]

    def _choose_random_entry(self):
        entriesLen = len(self.eh.entries)
        chosenEntry = str(randint(1, entriesLen))
        self.eh.selected_entry = self.eh.entries[chosenEntry]
        print(self.eh.selected_entry)
        return

    def init_player_props(self):
        '''
        assign player_num, answer and client_answer(placeholders) to eh.
        '''
        self.eh.player_num = self.player_num
        self.eh.answer = self.eh.selected_entry[0]
        print("First answer is ", self.eh.answer)
        for i in range(1,self.eh.player_num+1):
            self.eh.client_answer[str(i)] = "" 


    def start(self):
        # set up connection, initialize two client_handler that takes the incoming socket and does updatings.
        # 1. send the client socket their id
        for player in range(1, self.player_num + 1):
            (client_sock, client_ip) = self.sock_for_setup.accept()
            ch = ClientHandler(client_sock, player, self.eh)
            self.ch_list.append(ch)
            print(player)

        # sleep so that client don't receive data mixed together.
        sleep(1)
        for ch in self.ch_list:
            ch.start()

        while True:
            sleep(1000)  # stand by so the client handler threads don't die.
        return
