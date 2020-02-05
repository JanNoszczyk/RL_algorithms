import numpy as np
import logging


class TicTacToe:
    def __init__(self, n):
        self.n = n
        self.current_move = 0
        self.last_player = None
        self.board = np.zeros((n, n))
        self.rows, self.columns = [0] * n, [0] * n
        self.diag, self.adiag = 0, 0
        self.possible_next_state = None

    def get_state(self):
        # Represent state as a state vector, reshaping board into a vector
        return str(self.board.reshape(self.n**2))

    def play(self, player, i, j):
        if 0 <= i < self.n and 0 <= j < self.n:
            if player in [1, 2] and player != self.last_player and self.board[i, j] == 0:
                print("Possible states are {} \n".format(self.draw_board(player)))
                self.last_player = player
                self.board[i, j] = player
                self.current_move += 1

                # For player 1 num is -1, for player 2 its 1
                player_num = 2*player - 3
                self.rows[i] += player_num
                self.columns[j] += player_num
                if i == j:
                    self.diag += player_num
                elif j == self.n - i - 1:
                    self.adiag += player_num

                print("Round number {} \n {} \n{} \n ".format(self.current_move, self.board, self.game_over()))
            else:
                logging.error("The chosen player move is illegal.")
        else:
            logging.error("The location ({}, {}) is outside of the board".format(i, j))

    def game_over(self):
        """
        Scan the board to check for a winner or see if its a draw.
        Player 1 is marked as -1, player 2 marked as 1
        """
        if -self.n in [self.diag, self.adiag] + self.rows + self.columns:
            return 1
        elif self.n in [self.diag, self.adiag] + self.rows + self.columns:
            return 2

        if self.current_move == self.n ** 2:
            # draw
            return -1
        else:
            return 0

    def draw_board(self, player):
        """
        Get a list of possible_next_states, for each empty field theres a corresponding action and new state
        :return:
        """
        possible_states = []
        for (x, y), val in np.ndenumerate(self.board):
            if val == 0:
                new_board = self.board.copy()
                new_board[x, y] = player
                possible_states.append(((x, y), str(new_board.reshape(self.n**2))))
        return possible_states



game = TicTacToe(3)
game.play(1, 0, 2)
game.play(2, 1, 0)
game.play(1, 2, 0)
game.play(2, 1, 1)
game.play(1, 0, 1)
game.play(2, 2, 2)
game.play(1, 1, 2)
game.play(2, 0, 0)
# game.play(1, 2, 1)