import numpy as np
import logging
from tic_tac_toe import check_board


class Player:
    def __init__(self, n, player, alpha):
        self.n = n
        self.player = player
        self.player_num = 2 * player - 3
        self.value_function = {}
        self.state_history = []
        self.alpha = alpha

    @staticmethod
    def get_state_hash(state):
        return str(state.reshape(state.shape[0] * state.shape[1]))

    def get_value(self, state):
        state_hash = self.get_state_hash(state)
        if state_hash not in self.value_function:
            outcome = check_board(state)
            if outcome == self.player:
                self.value_function[state_hash] = 1
            elif outcome == 0:
                self.value_function[state_hash] = 0.5
            else:
                self.value_function[state_hash] = 0
        return self.value_function[state_hash]

    def update_state_history(self, state):
        self.state_history.append(state)

    def take_action(self, env, i):
        possible_states = env.get_possible_states(self.player)

        epsilon = 1 / i if i > 0 else 1
        p = np.random.random()
        if p > epsilon:
            # Exploit
            max_value, max_action = 0, None
            for action, state in possible_states:
                cur_value = self.get_value(state)
                if cur_value > max_value:
                    max_value = cur_value
                    max_action = action
        else:
            # Explore
            max_action = possible_states[np.random.randint(0, len(possible_states))][0]

        if max_action:
            env.play(self.player, max_action[0], max_action[1])
        else:
            logging.debug("No action was taken by player {}, the possible next states were {}".format(self.player, possible_states))

    def update(self, env):
        self.state_history.append(env.get_state())
        for i in range(len(self.state_history)-1, 0, -1):
            s, sp = self.state_history[i-1], self.state_history[i]
            vs, vsp = self.get_value(s), self.get_value(sp)
            self.value_function[self.get_state_hash(s)] = vs + self.alpha*(vsp - vs)
        self.state_history = []
