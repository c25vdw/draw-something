import pygame
import json
class Player(pygame.sprite.Sprite):
    def __init__(self, id):
        super().__init__()
        self.score = 0
        self.id = id
        self.isDrawer = (id is 1)
        self.world = None
    
    def update(self):
        pass

    def __repr__(self):
        return 'Player{this.number} :: score={this.score}; isDrawer={this.isDrawer}'.format(this=self)
    

class DrawGame(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.player1 = Player(1)
        self.player2 = Player(2)

        self.player1.world = self
        self.player2.world = self
        
        self.add(self.player1, self.player2)

    def update(self):
        super().update()

    def game_json(self):
        # returns the json format of all the points, in sequence of adding. update done in player.update()
        json.dumps("""""")

    def update_with_json(self, json_obj):
        pass