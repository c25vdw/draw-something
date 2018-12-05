import threading
import socket
import json


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_addr = s.getsockname()[0]
    return ip_addr


def parse_raw_data(data):
    # print("before loading to json: \n", data.decode())
    data = data.decode()
    # print(data)
    try:
        return json.loads(data)
    except:
        pass


class ServerHandlerG(threading.Thread):
    BUFFER_SIZE = 1024

    def __init__(self, event_hub, ip, server_ip):
        threading.Thread.__init__(self, name="server handler")
        self.eh = event_hub
        self.ip = ip
        self.server_ip = server_ip
        self.sock = socket.socket()
        print("client ipi: ~~~~~~~~~~~~~~~~~~~~~~`", self.ip)
        self.sock.bind(self.ip)
        self.player_id = 0

        # event hub proxy variables
        self.cur_pos = None  # array(tuple(2), tuple(2))
        self.color = None  # array(3)
        self.drawer_id = None  # int
        self.canDraw = None
        self.score = None
        self.client_answer = None
        self.input_txt = None

    def run(self):
        try:
            self.sock.connect(self.server_ip)
        except:
            self.sock.connect((self.server_ip[0], 12346))

        # waits for player_id
        player_id_raw = self.sock.recv(self.BUFFER_SIZE)
        self.player_id = parse_raw_data(player_id_raw)
        print("received player id: {}.".format(self.player_id))
        data = self.sock.recv(self.BUFFER_SIZE)
        data = parse_raw_data(data)
        print("data: ", data)
        self.eh.client_answer = data.get("client_answer")
        while True:
            # waits for server event hub snap
            server_eh_snap_raw = self.sock.recv(self.BUFFER_SIZE)
            server_eh = parse_raw_data(server_eh_snap_raw)
            if not server_eh:
                pass
            else:
                self.drawer_id = server_eh["drawer_id"]  # int
                self.canDraw = (self.player_id == server_eh["drawer_id"])
            # if not self.canDraw:
                # array(tuple(2), tuple(2))
                self.cur_pos = server_eh["cur_pos"]
                self.color = server_eh["color"]  # array(3)
                # self.score = server_eh["score"] # later
                self.client_answer = server_eh["client_answer"]
                self.input_txt = server_eh["input_txt"]  # later
                self.answer = server_eh["answer"]  # encrypt this??
                self.score = server_eh["score"]
                self.cur_ans_index = server_eh["cur_ans_index"]
                self.entry_length = len(server_eh["selected_entry"])
                self.count_down = server_eh["count_down"]
            # print("drawer id: ", server_eh["drawer"], ". self id: ", self.player_id)
            self.sock.sendall(self.eh.to_json().encode())
