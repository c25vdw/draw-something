"""
run game server.
it will:

1. listens for two clients to connect.
2. init two client handlers when connected.
3. run into infinite loop and update the game,
    while the game is updated through client handler, by the clients' blocked pygame's actions.
"""
from game_server import GameServerG

server = GameServerG()
server.start()