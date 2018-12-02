"""
run game server.

this should only be called by ../run_server.py
"""


def run():
    from server.game_server import GameServerG
    server = GameServerG()
    server.start()
