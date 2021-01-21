# Name: Jeb Barker
# Date: 1/8/2021
import copy
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
        self.corners = {0, 7, 56, 63}
        self.gMoves = {2, 3, 4, 5, 16, 24, 32, 40, 58, 59, 60, 61, 23, 31, 39, 47}
        self.bMoves = {1, 6, 8, 15, 9, 14, 48, 49, 57, 54, 55, 62}

    def best_strategy(self, board, color):
        # returns best move
        self.x_max = len(board)
        self.y_max = len(board[0])
        if color == "#000000":
            color = "@"
        else:
            color = "O"

        best_move = self.alphabeta(board, color, 5, -10000, 10000)
        return best_move[1], 0

    def max_value(self, board, color, search_depth, alpha, beta):
        # return value and state: (val, state)
        poss = self.find_moves(board, color)
        if search_depth == 0 or len(poss) == 0:
            return self.evaluate(board, color, poss)
        v = (-10000, board)

        for s in poss:
            b = self.make_move(board, color, (s // 8, s % 8), poss[s])
            min = self.min_value(b, self.white if color == self.black else self.black, search_depth - 1, alpha, beta)
            try:
                min = min[0]
            except TypeError:
                pass
            v = max(v, (min, (s // 8, s % 8)), key=lambda item: item[0])
            if v[0] > beta:
                return v
            alpha = max(v[0], alpha)
        return v

    def min_value(self, board, color, search_depth, alpha, beta):
        # return value and state: (val, state)
        poss = self.find_moves(board, color)
        if search_depth == 0 or len(poss) == 0:
            return -self.evaluate(board, color, poss)
        v = (10000, board)

        for s in poss:
            b = self.make_move(board, color, (s // 8, s % 8), poss[s])
            maxV = self.max_value(b, self.white if color == self.black else self.black, search_depth - 1, alpha, beta)
            try:
                maxV = maxV[0]
            except TypeError:
                pass
            v = min(v, (maxV, (s // 8, s % 8)), key=lambda item: item[0])
            if v[0] < alpha:
                return v
            beta = min(beta, v[0])
        return v

    def alphabeta(self, board, color, search_depth, alpha, beta):
        # returns best "value" while also pruning
        return self.max_value(board, color, search_depth, alpha, beta)

    def make_key(self, board, color):
        # hashes the board
        return 1

    def stones_left(self, board):
        # returns number of stones that can still be placed
        return 1

    def make_move(self, board, color, move, flipped):
        # returns board that has been updated
        b = copy.deepcopy(board)
        b[move[0]][move[1]] = color
        for m in flipped:
            b[m[0]][m[1]] = color
        return b

    def evaluate(self, board, color, possible_moves):
        ms = self.score(board, color)
        os = self.score(board, self.white if color == self.black else self.black)
        gM = 0
        bM = 0
        coinDiff = (ms - (2 * os))
        mobility = (len(possible_moves) - 2 * len(self.find_moves(board, self.opposite_color[color])))
        corner = 0
        for c in self.corners:
            corner += 1 if board[c // 8][c % 8] == color else 0
            corner -= 1 if board[c // 8][c % 8] == self.opposite_color[color] else 0
        for c in self.gMoves:
            gM += 1 if board[c // 8][c % 8] == color else 0
            gM -= 1 if board[c // 8][c % 8] == self.opposite_color[color] else 0
        for c in self.bMoves:
            bM -= 1 if board[c // 8][c % 8] == color else 0
            bM += 1 if board[c // 8][c % 8] == self.opposite_color[color] else 0
        # print("coinDiff: ", coinDiff*.5, " + mobility: ", mobility*2.5, " + corner: ", corner*30)
        if ms+os < 5:
            return mobility
        else:
            return mobility + (corner * 80) + (gM*15)

    def score(self, board, color):
        # returns the score of the board
        count = 0
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == color:
                    count += 1
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
                    moves_found.update({i * self.y_max + j: flipped_stones})
        return moves_found


class Alpha_beta_AI_bot:

    def __init__(self):
        self.white = "o"
        self.black = "@"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = None
        self.y_max = None
        self.corners = {0, 7, 56, 63}

    def best_strategy(self, board, color):
        # returns best move
        self.x_max = len(board)
        self.y_max = len(board[0])
        if color == "#000000":
            color = "@"
        else:
            color = "O"

        best_move = self.alphabeta(board, color, 5, -10000, 10000)
        return best_move[1], 0

    def max_value(self, board, color, search_depth, alpha, beta):
        # return value and state: (val, state)
        poss = self.find_moves(board, color)
        if search_depth == 0 or len(poss) == 0:
            return self.evaluate(board, color, poss)
        v = (-10000, board)

        for s in poss:
            b = self.make_move(board, color, (s//8, s % 8), poss[s])
            min = self.min_value(b, self.white if color == self.black else self.black, search_depth - 1, alpha, beta)
            try:
                min = min[0]
            except TypeError:
                pass
            v = max(v, (min, (s//8, s % 8)), key=lambda item: item[0])
            if v[0] > beta:
                return v
            alpha = max(v[0], alpha)
        return v

    def min_value(self, board, color, search_depth, alpha, beta):
        # return value and state: (val, state)
        poss = self.find_moves(board, color)
        if search_depth == 0 or len(poss) == 0:
            return -self.evaluate(board, color, poss)
        v = (10000, board)

        for s in poss:
            b = self.make_move(board, color, (s//8, s % 8), poss[s])
            maxV = self.max_value(b, self.white if color == self.black else self.black, search_depth - 1, alpha, beta)
            try:
                maxV = maxV[0]
            except TypeError:
                pass
            v = min(v, (maxV, (s // 8, s % 8)), key=lambda item: item[0])
            if v[0] < alpha:
                return v
            beta = min(beta, v[0])
        return v

    def alphabeta(self, board, color, search_depth, alpha, beta):
        # returns best "value" while also pruning
        return self.max_value(board, color, search_depth, alpha, beta)

    def make_key(self, board, color):
        # hashes the board
        return 1

    def stones_left(self, board):
        # returns number of stones that can still be placed
        return 1

    def make_move(self, board, color, move, flipped):
        # returns board that has been updated
        b = copy.deepcopy(board)
        b[move[0]][move[1]] = color
        for m in flipped:
            b[m[0]][m[1]] = color
        return b

    def evaluate(self, board, color, possible_moves):
        coinDiff = (self.score(board, color) - 2*self.score(board, self.white if color == self.black else self.black))  # /(self.score(board, color) + self.score(board, self.white if color == self.black else self.black))
        mobility = (len(possible_moves) - 2*len(self.find_moves(board, self.opposite_color[color])))  # /(len(possible_moves) + len(self.find_moves(board, self.opposite_color[color])))
        corner = 0
        for c in self.corners:
            corner += 1 if c in possible_moves or board[c // 8][c % 8] == color else 0
        # print("coinDiff: ", coinDiff, " + mobility: ", mobility)
        return coinDiff/4 + (mobility*2) + (corner*5.5)


    def score(self, board, color):
        # returns the score of the board
        count = 0
        for i in range(len(board)):
            for j in range(len(board[0])):
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
                    moves_found.update({i*self.y_max+j: flipped_stones})
        return moves_found


class Minimax_AI_bot:

    def __init__(self):
        self.white = "o"
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

        best_move = self.minimax(board, color, 5)
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
            b = self.make_move(board, color, (s // 8, s % 8), poss[s])
            min = self.min_value(b, self.white if color == self.black else self.black, search_depth - 1)
            try:
                min = min[0]
            except TypeError:
                pass
            v = max(v, (min, (s // 8, s % 8)), key=lambda item: item[0])
        return v

    def min_value(self, board, color, search_depth):
        # return value and state: (val, state)
        poss = self.find_moves(board, color)
        if search_depth == 0 or len(poss) == 0:
            return -self.evaluate(board, color, poss)
        v = (10000, board)

        for s in poss:
            b = self.make_move(board, color, (s // 8, s % 8), poss[s])
            max = self.max_value(b, self.white if color == self.black else self.black, search_depth - 1)
            try:
                max = max[0]
            except TypeError:
                pass
            v = min(v, (max, (s // 8, s % 8)), key=lambda item: item[0])
        return v

    def make_move(self, board, color, move, flipped):
        # returns board that has been updated
        b = copy.deepcopy(board)
        b[move[0]][move[1]] = color
        for m in flipped:
            b[m[0]][m[1]] = color
        return b

    def evaluate(self, board, color, possible_moves):
        # returns the utility value
        coinDiff = 100*(self.score(board, color) - self.score(board, self.white if color == self.black else self.black))  # /(self.score(board, color) + self.score(board, self.white if color == self.black else self.black))
        mobility = 100*(len(possible_moves) - len(self.find_moves(board, self.opposite_color[color])))  # /(len(possible_moves) + len(self.find_moves(board, self.opposite_color[color])))
        return coinDiff + mobility

    def score(self, board, color):
        # returns the score of the board
        count = 0
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == color:
                    count += 1
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
                    moves_found.update({i * self.y_max + j: flipped_stones})
        return moves_found
