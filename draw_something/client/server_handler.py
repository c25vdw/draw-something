import threading
import socket
import random
import json

from server.event_hub import EventHub

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_addr = s.getsockname()[0]
    return ip_addr

def get_first_json_string(json_str):
    has_bracket = False
    for m in json_str:
        if m == '{':
            has_bracket = True
            break
    if not has_bracket:
        return json_str
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

def parse_raw_data(data):
    # print("before loading to json: \n", data.decode())
    _data = data.decode()
    data = get_first_json_string(_data)
    # print(data)
    try:
        return json.loads(data)
    except:
        print("bad data\n{}\n{}\n".format(_data, data))
        # pass

class ServerHandlerG(threading.Thread):
    BUFFER_SIZE = 1024
    def __init__(self,  event_hub, ip, server_ip):
        threading.Thread.__init__(self, name="server handler")
        self.eh = event_hub
        self.ip = ip
        self.server_ip = server_ip
        self.sock = socket.socket()
        print("client ipi: ~~~~~~~~~~~~~~~~~~~~~~`",self.ip)
        self.sock.bind(self.ip)
        self.player_id = 0
        
        # event hub proxy variables
        self.cur_pos = None  # array(tuple(2), tuple(2))
        self.color = None  # array(3)
        self.drawer_id =None # int
        self.canDraw = None
        self.score =None
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
                self.cur_pos = server_eh["cur_pos"]  # array(tuple(2), tuple(2))
                self.color = server_eh["color"]  # array(3)
                # self.score = server_eh["score"] # later
                self.client_answer = server_eh["client_answer"] # later
                
                self.input_txt = server_eh["input_txt"] # later
            # print("drawer id: ", server_eh["drawer"], ". self id: ", self.player_id)
            self.sock.sendall(self.eh.to_json().encode())

