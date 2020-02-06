import numpy as np
from player import Player
from tic_tac_toe import TicTacToe

def play_game(p1, p2, env, i, draw=False):
    if i % 10 != 0: draw = False
    # Loops until the game is over
    # current_player = None
    current_player = p1 if np.random.randint(1, 3) == 1 else p2
    while not env.game_over():
        # Switch players in the new round
        # p1 always starts first
        if current_player == p1:
            current_player = p2
        else:
            current_player = p1

        # Draw the board before the user who wants to see it makes a move
        if draw:
            if draw == 1 and current_player == p1:
                env.draw_board()
            if draw == 2 and current_player == p2:
                env.draw_board()

        # Current player makes a move
        current_player.take_action(env, i)

        # Update state history
        state = env.get_state()
        p1.update_state_history(state)
        p2.update_state_history(state)

    if draw:
        env.draw_board()

    # Do the value function update
    p1.update(env)
    p2.update(env)

def train():
    n = 3
    alpha = 0.1
    p1, p2 = Player(n, 1, alpha), Player(n, 2, alpha)
    for i in range(100):
        print("\n\nPlaying game number {}".format(i))
        env = TicTacToe(n)
        play_game(p1, p2, env, i, draw=1)
        end_state = env.get_game_status()
        if end_state == -1:
            print("\nDraw\n")
        elif end_state == 0:
            print("\nGame does not seem to have finished\n")
        else:
            print("\nPlayer {} won\n".format(end_state))
train()