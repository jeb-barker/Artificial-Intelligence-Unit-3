# Name: Jeb Barker
# Date: 1/8/2021

import random


class RandomBot:
    def __init__(self):
        self.white = "O"
        self.black = "@"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = None
        self.y_max = None

    def best_strategy(self, board, color):
        # returns best move
        self.x_max = len(board)
        self.y_max = len(board[0])
        if color == "#000000":
            color = "@"
        else:
            color = "O"

        ''' Your code goes here '''
        best_move = random.choice(list(self.find_moves(board, color)))
        return best_move, 0

    def stones_left(self, board):
        # returns number of stones that can still be placed (empty spots)
        return 1

    def find_flipped(self, my_board, x, y, my_color):
        if my_board[x][y] != ".":
            return []
        if my_color == self.black:
            my_color = "@"
        else:
            my_color = "O"
        flipped_stones = []
        for incr in self.directions:
            temp_flip = []
            x_pos = x + incr[0]
            y_pos = y + incr[1]
            while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
                if my_board[x_pos][y_pos] == ".":
                    break
                if my_board[x_pos][y_pos] == my_color:
                    flipped_stones += temp_flip
                    break
                temp_flip.append([x_pos, y_pos])
                x_pos += incr[0]
                y_pos += incr[1]
        return flipped_stones

    def find_moves(self, my_board, my_color):
        moves_found = {}
        for i in range(len(my_board)):
            for j in range(len(my_board[i])):
                flipped_stones = self.find_flipped(my_board, i, j, my_color)
                if len(flipped_stones) > 0:
                    moves_found.update({(i, j): flipped_stones})
        return moves_found


class Best_AI_bot:

    def __init__(self):
        self.white = "o"
        self.black = "@"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = None
        self.y_max = None

    def best_strategy(self, board, color):
        # returns best move
        best_move = self.minimax(board, color, 3)
        return best_move, 0

    def minimax(self, board, color, search_depth):
        # returns best "value"
        return self.max_value(board, color, search_depth)

    def max_value(self, board, color, search_depth):
        # return value and state: (val, state)
        poss = self.find_moves(board, color)
        if search_depth == 0 or len(poss) == 0:
            return self.evaluate(board, color, poss)
        v = (-10000, board)

        for s in poss:
            b = self.make_move(board, color, s)
            min = self.min_value(b, self.white if color == self.black else self.black, search_depth - 1)
            try:
                min = min[0]
            except TypeError:
                pass
            v = max(v, (min, s), key=lambda item: item[0])
        return v

    def min_value(self, board, color, search_depth):
        # return value and state: (val, state)
        poss = self.find_moves(board, color)
        if search_depth == 0 or len(poss) == 0:
            return -self.evaluate(board, color, poss)
        v = (10000, board)

        for s in poss:
            b = self.make_move(board, color, s)
            max = self.max_value(b, self.white if color == self.black else self.black, search_depth - 1)
            try:
                max = max[0]
            except TypeError:
                pass
            v = min(v, (max, s), key=lambda item: item[0])
        return v

    def negamax(self, board, color, search_depth):
        # returns best "value"
        return 1

    def alphabeta(self, board, color, search_depth, alpha, beta):
        # returns best "value" while also pruning
        pass

    def make_key(self, board, color):
        # hashes the board
        return 1

    def stones_left(self, board):
        # returns number of stones that can still be placed
        return 1

    def make_move(self, board, color, move, flipped):
        # returns board that has been updated
        b = board.copy()
        b[move[0]][move[1]] = color
        for m in flipped:
            b[m[0]][m[1]] = color
        return b

    def evaluate(self, board, color, possible_moves):
        # returns the utility value
        return self.score(board, color) - self.score(board, self.white if color == self.black else self.black)

    def score(self, board, color):
        # returns the score of the board
        count = 0
        for i in board:
            for j in board:
                if board[i][j] == color:
                    count+=1
        return count

    def find_flipped(self, my_board, x, y, my_color):
        if my_board[x][y] != ".":
            return []
        if my_color == self.black:
            my_color = "@"
        else:
            my_color = "O"
        flipped_stones = []
        for incr in self.directions:
            temp_flip = []
            x_pos = x + incr[0]
            y_pos = y + incr[1]
            while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
                if my_board[x_pos][y_pos] == ".":
                    break
                if my_board[x_pos][y_pos] == my_color:
                    flipped_stones += temp_flip
                    break
                temp_flip.append([x_pos, y_pos])
                x_pos += incr[0]
                y_pos += incr[1]
        return flipped_stones

    def find_moves(self, my_board, my_color):
        moves_found = {}
        for i in range(len(my_board)):
            for j in range(len(my_board[i])):
                flipped_stones = self.find_flipped(my_board, i, j, my_color)
                if len(flipped_stones) > 0:
                    moves_found.update({(i, j): flipped_stones})
        return moves_found
