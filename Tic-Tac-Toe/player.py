import numpy as np


class Player:
    def __init__(self, n, number):
        self.n = n
        self.number = number
        self.value_function = {}

    def get_value(self, state):
        if state in self.value_function:
            return self.value_function[state]
        else:




a = np.ones((3**2,3**2))*0.5
print(a)