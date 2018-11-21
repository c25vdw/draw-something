"""where the client pygame GUI starts,

step 1: init pygame, ask for server ip address

step 2: init this client's **server handler**, which
    1. takes the initialized game object as own param.
    2. updates the game, by lazily receiving JSON from server's client handler(later), in a while loop, which blocks by socket.
    3. is a thread (and a child of socket), and runs itself at init, far before we enter while loop. (and is already looping)

step 3: enter pygame while loop
    the game object inited in step 1, updated in step 2(infinitely in another thread), is here updated and drawn out.

we need:
    1. before while loop:
        game object: local_drawgame = DrawGame()
        this client's server handler: my_server_handler = ServerHandler(1. local_drawgame, 2. local ip address, some other stuff)

    2. inside while loop:
        there will be no reference to my_server_handler, while it changes our game object stealthly.
        the only thing we do is drawing out the game object.
"""