# Name:
# Date:
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
        first_move = True
        b = [j for sub in board for j in sub]
        first_move = False if "X" in b and "O" in b else True

        moves = set()
        for i in range(len(board)):
            for j in range(len(board[i])):
                if first_move and board[i][j] == ".":
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
        self.white = "#ffffff"  # "O"
        self.black = "#000000"  # "X"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = None
        self.y_max = None
        self.first_turn = True

    def best_strategy(self, board, color):
        # returns best move
        return best_move, 0

    def minimax(self, board, color, search_depth):
        # returns best "value"
        return 1

    def negamax(self, board, color, search_depth):
        # returns best "value"
        return 1

    def alphabeta(self, board, color, search_depth, alpha, beta):
        # returns best "value" while also pruning
        pass

    def make_move(self, board, color, move):
        # returns board that has been updated
        boardC = board.copy()
        b = [j for sub in board for j in sub]
        index = b.index("X" if color == self.black else "O")
        boardC[index % 5][index // 5] = "W"
        boardC[move[0]][move[1]] = "X" if color == self.black else "O"
        return boardC

    def evaluate(self, board, color, possible_moves):
        # returns the utility value
        return 1

    def find_moves(self, board, color):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        first_move = True
        b = [j for sub in board for j in sub]
        first_move = False if "X" in b and "O" in b else True

        moves = set()
        for i in range(len(board)):
            for j in range(len(board[i])):
                if first_move and board[i][j] == ".":
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
