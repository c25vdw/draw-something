"""
run game server.
it will:

1. listens for two clients to connect.
2. init two client handlers when connected.
3. run into infinite loop and update the game,
    while the game is updated through client handler, by the clients' blocked pygame's actions.
"""
from server.game_server import GameServerG

def run_server():
    server = GameServerG()
    server.start()

if __name__ == "__main__":
    run_server()