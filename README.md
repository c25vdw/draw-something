# draw-something
draw something with your LAN friends!

This is a draw-something game running on LAN, built using pygame and socket(TCP).

### construction sequence

- [x] game object, client's game actions object.

- [x] server handler, client handler and game server.

### milestones

1. by the end of the first week: (after weekend)

    - either can draw and the other will see, vise versa

2. right before demo

    - guessing, round and difficulty.

3. better UI
    
    - countdown, input box and screen showing scores.

### Usage

1. connect all players(laptops) under LAN, each with a local ip address starting with `192`.
2. `python run_server.py` to start a server. you will need to choose one player(laptop) to host the server.
3. `python run_client.py` to start a player. (the number of player is not limiting, but should equal to the input number given to server).

---
this project is a team of two project, done for University of Alberta CMPUT274 final project.
