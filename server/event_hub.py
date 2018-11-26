import json


class EventHub:
    def __init__(self):

        # local events
        self.cur_pos = [(None, None), (None, None)]
        self.color = (0, 0, 0)
        self.drawer_id = 1
        self.input_txt = ""
        self.client_answer = ""

        # server events
        self.score = {
            'player_1': 0,
            'player_2': 0
        }
        self.correct = False

        # for server usage
        self.answer = "dog"
        self.pause_game = False # later
        self.prev_upload_id = self.drawer_id

    def to_json(self):
        return json.dumps({
            "cur_pos": [self.cur_pos[0], self.cur_pos[1]],
            "color": [self.color[0], self.color[1], self.color[2]],
            "drawer": self.drawer_id,
            "score": {
                "player_1": self.score["player_1"],
                "player_2": self.score["player_2"]
            },
            "input_txt": self.input_txt,
            "client_answer": self.client_answer,
            "correct": self.correct,
        })

    def flush_input_to_client_answer(self):
        self.client_answer = self.input_txt
        self.input_txt = ""

    def compare_then_update_answer(self, client_answer):
        isCorrect = False
        if (self.answer == client_answer):
            isCorrect = True
            self.answer = self.answer + "1"
            print("server answer is now {}".format(self.answer))
        return isCorrect