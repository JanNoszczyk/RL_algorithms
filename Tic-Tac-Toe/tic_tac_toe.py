import numpy as np
import logging


def check_board(board):
    """
    Scan the board to check for a winner or see if its a draw.
    Player 1 is marked as -1, player 2 marked as 1
    """
    n = board.shape[0]
    for row in range(n):
        row_sum = np.sum(board[row, :])
        if row_sum == -n:
            return 1
        elif row_sum == n:
            return 2

    for col in range(n):
        col_sum = np.sum(board[:, col])
        if col_sum == -n:
            return 1
        elif col_sum == n:
            return 2

    diag_1, diag_2 = np.trace(board), np.trace(np.fliplr(board))
    if diag_1 == -n or diag_2 == -n:
        return 1
    elif diag_1 == n or diag_2 == n:
        return 2

    for val in np.nditer(board):
        if val == 0:
            return 0
    return -1


class TicTacToe:
    def __init__(self, n):
        self.n = n
        self.current_move = 0
        self.last_player = None
        self.board = np.zeros((n, n))
        self.possible_next_state = None

    def get_state(self):
        return self.board
        # Represent state as a state vector, reshaping board into a vector
        # return str(self.board.reshape(self.n**2))

    def play(self, player, i, j):
        if 0 <= i < self.n and 0 <= j < self.n:
            if player in [1, 2] and player != self.last_player and self.board[i, j] == 0:
                # print("Possible states are {} \n".format(self.draw_board(player)))
                self.last_player = player
                self.current_move += 1

                # For player 1 num is -1, for player 2 its 1
                player_num = 2*player - 3
                self.board[i, j] = player_num

                print("Round number {} \n {} \n{} \n ".format(self.current_move, self.draw_board(), self.game_over()))
            else:
                logging.error("The chosen player move is illegal.")
        else:
            logging.error("The location ({}, {}) is outside of the board".format(i, j))

    def game_over(self):
        return check_board(self.board)

    def get_possible_states(self, player):
        """
        Get a list of possible_next_states, for each empty field theres a corresponding action and new state
        :return:
        """
        possible_states = []
        for (x, y), val in np.ndenumerate(self.board):
            if val == 0:
                new_board = self.board.copy()
                new_board[x, y] = player
                possible_states.append(((x, y), new_board))
        return possible_states

    def draw_board(self):
        horizontal_lines = "-------------"
        print(horizontal_lines)
        for i in range(self.n):
            row_string = "|"
            for j in range(self.n):
                val = self.board[i, j]
                if val != 0: val = (val + 3)/2
                row_string += " {} |".format(int(val))
            print(row_string)
            print(horizontal_lines)


def test_tic_tac():
    game = TicTacToe(3)
    game.play(1, 0, 2)
    game.play(2, 1, 0)
    game.play(1, 2, 0)
    game.play(2, 1, 1)
    game.play(1, 0, 1)
    game.play(2, 2, 2)
    game.play(1, 1, 2)
    game.play(2, 0, 0)
    assert game.game_over() == 2
test_tic_tac()