import numpy as np
from tic_tac_toe import check_board


class Player:
    def __init__(self, n, number):
        self.n = n
        self.number = number
        self.player_number = 2*number - 3
        self.value_function = {}

    def get_value(self, state):
        state_hash = str(state.reshape(state.shape[0]*state.shape[1]))
        if state_hash not in self.value_function:
            outcome = check_board(state)
            if outcome == self.number:
                self.value_function[state_hash] = 1
            elif outcome == 0:
                self.value_function[state_hash] = 0.5
            else:
                self.value_function[state_hash] = 0
        return self.value_function[state_hash]



a = np.ones((4,4))*0.2
print(a.shape[0])
