import json


class EventHub:
    def __init__(self):

        # local events
        self.cur_pos = [(None, None), (None, None)]
        self.color = (0, 0, 0)
        self.drawer_id = 1
        self.player_num = 0
        self.input_txt = ""
        self.client_answer = {}
        self.entries = {}
        self.selected_entry = []
        self.cur_ans_index = 0
        # server events
        self.score = {
            '1': 0,
            '2': 0
        }
        self.correct = False
        self.restart_timer = False
        self.ticking = False
        self.count_down = 0
        # for server usage
        self.answer = ""
        self.pause_game = False  # later
        self.prev_upload_id = self.drawer_id

        # NOTICE: more attributes might be implicitely inserted by game server or client handler. like answer_stream or so.

    def to_json(self):
        return json.dumps({
            "cur_pos": [self.cur_pos[0], self.cur_pos[1]],
            "color": [self.color[0], self.color[1], self.color[2]],
            "drawer_id": self.drawer_id,
            "cur_ans_index": self.cur_ans_index,
            "score": self.score,
            "entries": self.entries,
            "selected_entry": self.selected_entry,
            "input_txt": self.input_txt,
            "client_answer": self.client_answer,
            "correct": self.correct,
            "answer": self.answer,
            "restart_timer": self.restart_timer,
            "count_down": self.count_down,
            "ticking":self.ticking,
        })

    def flush_input_to_client_answer(self, player_id):
        self.client_answer[str(player_id)] = self.input_txt
        self.input_txt = ""

    def compare_then_update_answer(self, client_answer, player_id):
        # TODO: use answers read from game server, somehow use answer stream/sequence.
        isCorrect = False
        if (self.answer == client_answer and self.cur_ans_index < len(self.selected_entry) - 1):
            isCorrect = True
            self.cur_ans_index += 1
            self.answer = self.selected_entry[self.cur_ans_index]
            self.client_answer[str(player_id)] = ""
            print("server answer is now {}".format(self.answer))
        elif (self.answer == client_answer and self.cur_ans_index == len(self.selected_entry) - 1):
            isCorrect = True
            self.cur_ans_index = 0
            self.answer = self.selected_entry[self.cur_ans_index]
            self.client_answer[str(player_id)] = ""
            print("server answer is now {}".format(self.answer))
        return isCorrect

    def update_answer(self):
        if (self.cur_ans_index < len(self.selected_entry) - 1):
            self.cur_ans_index += 1
            self.answer = self.selected_entry[self.cur_ans_index]
        elif (self.cur_ans_index == len(self.selected_entry) - 1):
            self.cur_ans_index = 0
            self.answer = self.selected_entry[self.cur_ans_index]
