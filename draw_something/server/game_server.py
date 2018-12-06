import socket
import random
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
        print("level is: ", self.level)
        self.ch_list = []
        self.all_disconnected = False
        self.eh = EventHub()

        self.init_sock_for_setup()
        self.init_eh_entries()  # define entries
        self.init_eh_score()  # define score
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
        # self.choose_random_entry()
        self.choose_entry_from_level()

    def init_eh_score(self):
        score = {}
        for i in range(1, self.player_num + 1):
            score[str(i)] = 0
        self.eh.score = score

    def init_sock_for_setup(self):
        '''create self.sock_for_setup, start listening on port 12345'''
        self.sock_for_setup = socket.socket()
        self.sock_for_setup.setblocking(True)  # no timeout.
        self.ip = get_ip_address()
        self.sock_for_setup.bind((self.ip, 12345))

        self.sock_for_setup.listen(self.player_num)  # listens on public:12345
        print("listening for {} clients on: {}".format(
            self.player_num, (self.ip, '12345')))

    def choose_entry_from_level(self):
        self.eh.selected_entry = self.eh.entries[str(self.level)]
        # self.eh.selected_entry = ["cat","dog"]

    def choose_random_entry(self):
        entriesLen = len(self.eh.entries)
        chosenEntry = str(random.randint(1, entriesLen))
        self.eh.selected_entry = self.eh.entries[chosenEntry]
        print(self.eh.selected_entry)
        return

    def init_player_props(self):
        '''
        assign player_num, answer and client_answer(placeholders) to eh.
        '''
        self.eh.player_num = self.player_num
        random.shuffle(self.eh.selected_entry)
        self.eh.answer = self.eh.selected_entry[0]

        print("First answer is ", self.eh.answer)
        for i in range(1, self.eh.player_num + 1):
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
        sleep(0.5)
        for ch in self.ch_list:
            ch.start()

        while not self.all_disconnected:
            sleep(1)
            self.check_client_connections()
            # stand by so the client handler threads don't die.
        return

    def check_client_connections(self):
        # check if all clients are disconnected with the server.
        self.all_disconnected = True
        for client in self.ch_list:
            if not client.should_stop:
                self.all_disconnected = False
                break
