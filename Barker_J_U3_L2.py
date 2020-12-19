# Name:
# Date:
import copy
import random


class RandomPlayer:
    def __init__(self):
        self.white = "#ffffff"  # "O"
        self.black = "#000000"  # "X"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = None
        self.y_max = None
        self.first_turn = True

    def best_strategy(self, board, color):
        # returns best move
        # (column num, row num), 0
        best_move = random.choice(list(self.find_moves(board, color)))
        return best_move, 0

    def find_moves(self, board, color):
        # finds all possible moves
        # returns a set, e.g., {0, 1, 2, 3, ...., 24}
        # 0 5 10 15 20
        # 1 6 11 16 21
        # 2 7 12 17 22
        # 3 8 13 18 23
        # 4 9 14 19 24
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]

        b = [j for sub in board for j in sub]
        self.first_turn = False if "X" in b and "O" in b else True

        moves = set()
        for i in range(len(board)):
            for j in range(len(board[i])):
                if self.first_turn and board[i][j] == ".":
                    moves.add((i, j))
                elif (board[i][j] == "X" and color == "#000000") or (board[i][j] == "O" and color == "#ffffff"):
                    for increment in directions:
                        x = i + increment[0]
                        y = j + increment[1]
                        done = False
                        while 0 <= x < 5 and 0 <= y < 5:
                            if board[x][y] != '.':
                                done = True
                            if not done:
                                moves.add((x, y))
                            x += increment[0]
                            y += increment[1]
        # print(moves)
        return moves


# noinspection DuplicatedCode
class CustomPlayer:

    def __init__(self):
        self.white = "#ffffff"  # "O"/white color
        self.black = "#000000"  # "X"/black color
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = None
        self.y_max = None
        self.first_turn = True

    def best_strategy(self, board, color):
        # returns best move
        best_move = self.minimax(board, color, 4)  # X wins: 2, 3, 7... O wins: 1, 4, 5, 6...
        return best_move[1], 0

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

    def make_move(self, board, color, move):
        # returns board that has been updated
        boardC = copy.deepcopy(board)
        b = [j for sub in boardC for j in sub]
        if self.first_turn:
            self.first_turn = False if "X" in b and "O" in b else True

        for i in range(len(boardC)):
            for j in range(len(boardC[i])):
                if not self.first_turn and boardC[i][j] == ("X" if color == self.black else "O"):
                    boardC[i][j] = "W"
        boardC[move[0]][move[1]] = "X" if color == self.black else "O"
        return boardC

    def evaluate(self, board, color, possible_moves):
        # returns the utility value
        return len(possible_moves) - len(self.find_moves(board, self.opposite_color[color]))

    def find_moves(self, board, color):
        b = [j for sub in board for j in sub]
        if self.first_turn:
            self.first_turn = False if "X" in b and "O" in b else True

        moves = set()
        for i in range(len(board)):
            for j in range(len(board[i])):
                if self.first_turn and board[i][j] == ".":
                    moves.add((i, j))
                elif (board[i][j] == "X" and color == "#000000") or (board[i][j] == "O" and color == "#ffffff"):
                    for increment in self.directions:
                        x = i + increment[0]
                        y = j + increment[1]
                        done = False
                        while 0 <= x < 5 and 0 <= y < 5:
                            if board[x][y] != '.':
                                done = True
                            if not done:
                                moves.add((x, y))
                            x += increment[0]
                            y += increment[1]
        # print(moves)
        return moves
