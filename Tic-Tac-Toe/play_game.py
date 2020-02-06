

def play_game(p1, p2, env, draw=False):
    # Loops until the game is over
    current_player = None
    i = 0
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

        i += 1

    if draw:
        env.draw_board()

    # Do the value function update
    p1.update(env)
    p2.update(env)