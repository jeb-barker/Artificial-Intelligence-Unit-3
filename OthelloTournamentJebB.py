import copy
import multiprocessing


class Strategy:

    def __init__(self):
        self.white = "o"
        self.black = "x"
        self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.opposite_color = {self.black: self.white, self.white: self.black}
        self.x_max = None
        self.y_max = None
        self.corners = {0, 7, 56, 63}
        self.gMoves = {2, 3, 4, 5, 16, 24, 32, 40, 58, 59, 60, 61, 23, 31, 39, 47}
        self.bMoves = {1, 6, 8, 15, 9, 14, 48, 49, 57, 54, 55, 62}
        self.logging = True

    def best_strategy(self, board, player, best_move, still_running):
        # returns best move
        self.x_max = 8
        self.y_max = 8

        best_movee = self.alphabeta(board, player, 5, -10000, 10000, still_running)
        best_move.value = best_movee[1]
        # return best_movee[1]

    def max_value(self, board, player, search_depth, alpha, beta, still_running):
        # return value and state: (val, state)
        poss = self.legal_moves(board, player)
        # print(poss)
        if search_depth == 0 or len(poss) == 0 or still_running == 0:
            return self.evaluate(board, player, poss)
        v = (-10000, board)

        for s in poss:
            b = self.make_move(board, player, s, poss[s])
            min = self.min_value(b, self.white if player == self.black else self.black, search_depth - 1, alpha, beta,
                                 still_running)
            try:
                min = min[0]
            except TypeError:
                pass
            v = max(v, (min, s), key=lambda item: item[0])
            if v[0] > beta:
                return v
            alpha = max(v[1], alpha)
        return v

    def min_value(self, board, color, search_depth, alpha, beta, still_running):
        # return value and state: (val, state)
        poss = self.legal_moves(board, color)
        if search_depth == 0 or len(poss) == 0 or still_running == 0:
            return -self.evaluate(board, color, poss)
        v = (10000, board)

        for s in poss:
            b = self.make_move(board, color, s, poss[s])
            maxV = self.max_value(b, self.white if color == self.black else self.black, search_depth - 1, alpha, beta,
                                  still_running)
            try:
                maxV = maxV[0]
            except TypeError:
                pass
            v = min(v, (maxV, s), key=lambda item: item[0])
            if v[0] < alpha:
                return v
            beta = min(beta, v[0])
        return v

    def alphabeta(self, board, color, search_depth, alpha, beta, still_running):
        # returns best "value" while also pruning
        return self.max_value(board, color, search_depth, alpha, beta, still_running)

    def make_move(self, board, color, move, flipped):
        # returns board that has been updated
        b = [char for char in board]
        b[move] = color
        for m in flipped:
            b[m[0]] = color
        return "".join(b)

    def evaluate(self, board, color, possible_moves):
        ms = self.score(board, color)
        os = self.score(board, self.white if color == self.black else self.black)
        gM = 0
        bM = 0
        coinDiff = (ms - (2 * os))
        mobility = (len(possible_moves) - 2 * len(self.legal_moves(board, self.opposite_color[color])))
        corner = 0
        for c in self.corners:
            corner += 1 if board[c] == color else 0
            corner -= 1 if board[c] == self.opposite_color[color] else 0
        for c in self.gMoves:
            gM += 1 if board[c] == color else 0
            gM -= 1 if board[c] == self.opposite_color[color] else 0
        for c in self.bMoves:
            bM -= 1 if board[c] == color else 0
            bM += 1 if board[c] == self.opposite_color[color] else 0
        # print("coinDiff: ", coinDiff*.5, " + mobility: ", mobility*2.5, " + corner: ", corner*30)
        if ms + os < 5:
            return mobility
        else:
            return mobility + (corner * 80) + (gM * 15)

    def score(self, board, color):
        # returns the score of the board
        count = 0
        for i in range(self.y_max):
            for j in range(self.y_max):
                if board[i * self.y_max + j] == color:
                    count += 1
        return count

    def find_flipped(self, my_board, pos, my_color):
        # # print(x * self.y_max + y)
        #
        # if my_board[pos] != ".":
        #     return []
        # flipped_stones = []
        # for incr in self.directions:
        #     temp_flip = []
        #     pos2 = pos + incr
        #     while pos:
        #         try:
        #             if my_board[pos2] == ".":
        #                 break
        #             if my_board[pos2] == my_color:
        #                 flipped_stones += temp_flip
        #                 break
        #             temp_flip.append([pos2])
        #             pos2 += incr
        #         except IndexError:
        #             break
        #
        # return flipped_stones
        x = pos // 8
        y = pos % 8
        if my_board[pos] != ".":
            return []
        flipped_stones = []
        for incr in self.directions:
            temp_flip = []
            x_pos = x + incr[0]
            y_pos = y + incr[1]
            pos2 = x_pos * self.y_max + y_pos
            while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
                if my_board[pos2] == ".":
                    break
                if my_board[pos2] == my_color:
                    flipped_stones += temp_flip
                    break
                temp_flip.append([pos2])
                x_pos += incr[0]
                y_pos += incr[1]
                pos2 = x_pos * self.y_max + y_pos
        return flipped_stones

    def legal_moves(self, my_board, my_color):
        moves_found = {}
        for i in range(0, len(my_board)):
            flipped_stones = self.find_flipped(my_board, i, my_color)
            if len(flipped_stones) > 0:
                moves_found.update({i: flipped_stones})
        return moves_found


s = Strategy()
a = multiprocessing.Value
print(s.best_strategy("..................o.ox....oooo.o..oooxo.....xxx.................", "x", a, 1))

# ........
# ........
# ........
# ...ox...
# ...xo...
# ........
# ........
# ........
