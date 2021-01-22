import copy
import random


class RandomBot:
    def __init__(self):
        self.white = "O"
        self.black = "X"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = None
        self.y_max = None

    def best_strategy(self, board, color):
        # returns best move
        self.x_max = len(board)
        self.y_max = len(board[0])
        if color == "#000000":
            color = "X"
        else:
            color = "O"

        ''' Your code goes here '''
        a = self.find_moves(board, color)
        print(a)
        best_move = random.choice(list(a))
        print(best_move)
        bx = best_move//self.y_max
        by = best_move % self.y_max
        print(bx, ", ", by, "\n\n----------")
        return (bx, by), 0

    def find_moves(self, my_board, my_color):
        moves_found = set()
        for i in range(len(my_board)):
            j = 6
            # if my_board[i][j] == '.':
            for incr in [[0, -1]]:
                y_pos = j + incr[1]
                stop = False
                while 0 <= y_pos < self.y_max and not stop:
                    if my_board[i][y_pos] == '.':
                        moves_found.add(i * self.y_max + y_pos)
                        stop = True
                    y_pos += incr[1]
        return moves_found


class Best_AI_bot:

    def __init__(self):
        self.white = "O"
        self.black = "X"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = None
        self.y_max = None

    def best_strategy(self, board, color):
        # returns best move
        self.x_max = len(board)
        self.y_max = len(board[0])
        if color == "#000000":
            color = "X"
        else:
            color = "O"

        best_move = self.alphabeta(board, color, 5, -10000, 10000)
        return (best_move[1] // self.y_max, best_move[1] % self.y_max), 0

    def max_value(self, board, color, search_depth, alpha, beta):
        # return value and state: (val, state)
        poss = self.find_moves(board, color)
        # print(poss)
        if search_depth == 0 or len(poss) == 0 or self.is_done(board, color) is None:
            return self.evaluate(board, color, poss)
        v = (-10000, board)

        for s in poss:
            b = self.make_move(board, color, s)
            min = self.min_value(b, self.white if color == self.black else self.black, search_depth - 1, alpha,
                                 beta)
            try:
                min = min[0]
            except TypeError:
                pass
            v = max(v, (min, s), key=lambda item: item[0])
            if v[0] > beta:
                return v
            alpha = max(v[0], alpha)
        return v

    def min_value(self, board, color, search_depth, alpha, beta):
        # return value and state: (val, state)
        poss = self.find_moves(board, color)
        if search_depth == 0 or len(poss) == 0 or self.is_done(board, color) is None:
            return -self.evaluate(board, color, poss)
        v = (10000, board)

        for s in poss:
            b = self.make_move(board, color, s)
            maxV = self.max_value(b, self.white if color == self.black else self.black, search_depth - 1, alpha, beta)
            try:
                maxV = maxV[0]
            except TypeError:
                pass
            v = min(v, (maxV, s), key=lambda item: item[0])
            if v[0] < alpha:
                return v
            beta = min(beta, v[0])
        return v

    def alphabeta(self, board, color, search_depth, alpha, beta):
        # returns best "value" while also pruning
        return self.max_value(board, color, search_depth, alpha, beta)

    def make_move(self, board, color, move):
        # returns board that has been updated
        b = copy.deepcopy(board)
        b[move // self.x_max][move % self.y_max] = color
        return b

    def is_done(self, my_board, color):
        for i in range(len(my_board)):
            for j in range(len(my_board[i])):
                if (color == self.black and my_board[i][j] == 'X') or (color == self.white and my_board[i][j] == 'O'):
                    for incr in self.directions:
                        x_pos = i + incr[0]
                        y_pos = j + incr[1]
                        count = 1
                        stop = False
                        while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max and not stop:
                            if my_board[x_pos][y_pos] != my_board[i][j]:
                                count = 1
                                stop = True
                            else:
                                count += 1
                            if count == 4:
                                return None
                            x_pos += incr[0]
                            y_pos += incr[1]
        return 1

    def evaluate(self, board, color, possible_moves):
        cons = []
        for i in range(len(board)):
            for j in range(len(board[i])):
                if (color == self.black and board[i][j] == 'X') or (color == self.white and board[i][j] == 'O'):
                    for incr in self.directions:
                        x_pos = i + incr[0]
                        y_pos = j + incr[1]
                        count = 1
                        stop = False
                        while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max and not stop:
                            if board[x_pos][y_pos] != board[i][j]:
                                # cons.append(count)
                                count = 1
                                stop = True
                            else:
                                count += 1
                            if count == 4:
                                cons.append(count)
                            x_pos += incr[0]
                            y_pos += incr[1]
        return sum(cons)

    def find_moves(self, my_board, my_color):
        moves_found = set()
        for i in range(len(my_board)):
            j = 6
            # if my_board[i][j] == '.':
            for incr in [[0, -1]]:
                y_pos = j + incr[1]
                stop = False
                while 0 <= y_pos < self.y_max and not stop:
                    if my_board[i][y_pos] == '.':
                        moves_found.add(i * self.y_max + y_pos)
                        stop = True
                    y_pos += incr[1]
        return moves_found
