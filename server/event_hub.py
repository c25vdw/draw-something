import json

class EventHub:
    def __init__(self):
        self.cur_pos = (None, None)
        self.color = (0, 0, 0)
        self.drawer_id = 1
        self.score = {
            'player_1': 0,
            'player_2': 0
        }
    
    def to_json(self):
        return json.dumps({
            "cur_pos": [self.cur_pos[0], self.cur_pos[1]],
            "color": [self.color[0], self.color[1], self.color[2]],
            "drawer": self.drawer_id,
            "score": {
                "player_1": self.score["player_1"],
                "player_2": self.score["player_2"]
            }
        })
    
    