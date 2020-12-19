# Original idea from Richard Zhan (class of 2020)
# Modified by N. Kim on Dec 2019

import sys
import os
import time
import tkinter as tk
from Barker_J_U3_L2 import CustomPlayer, RandomPlayer

# constants
delay_time = 1.5
turn_off_printing = False
tile_size = 50
padding = 5
x_max = 5
y_max = 5
board_x = x_max * tile_size + (x_max + 1) * padding - 2
board_y = y_max * tile_size + (y_max + 1) * padding - 2
white = "#ffffff"
black = "#000000"
grey = "#505050"
green = "#00ff00"
yellow = "#ffff00"
brown = "#654321"
blue = "#0000ff"
cyan = "#00ffff"
red = "#ff0000"
asterisk = " " + u'\u2217'
directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
opposite_color = {black: white, white: black}

# variables
player_types = {0: "Player", 1: "Random", 2: "Custom"}
players = {black: None, white: None, None: None}
player_max_times = {black: 0, white: 0}
player_total_times = {black: 0, white: 0}
p1_name = ""
p2_name = ""
root = None
canvas = None
turn = white
board = []
possible_moves = {i for i in range(x_max * y_max)}
first_turn = 0


# commands


def whose_turn(my_board, prev_turn):
    global possible_moves, first_turn
    cur_turn = opposite_color[prev_turn]
    possible_moves = find_moves(my_board, cur_turn)
    first_turn += 1
    if len(possible_moves) > 0:
        return cur_turn
    return None


def find_moves(my_board, my_color):
    global first_turn
    moves_found = set()
    for i in range(len(my_board)):
        for j in range(len(my_board[i])):
            if first_turn < 2 and my_board[i][j] == '.':
                moves_found.add(i * y_max + j)
            elif (my_color == black and my_board[i][j] == 'X') or (my_color == white and my_board[i][j] == 'O'):
                for incr in directions:
                    x_pos = i + incr[0]
                    y_pos = j + incr[1]
                    stop = False
                    while 0 <= x_pos < x_max and 0 <= y_pos < y_max:
                        if my_board[x_pos][y_pos] != '.':
                            stop = True
                        if not stop:
                            moves_found.add(x_pos * y_max + y_pos)
                        x_pos += incr[0]
                        y_pos += incr[1]
    return moves_found


def print_board(my_board):
    # return  # comment to print board each time
    print("\t", end="")
    for i in range(x_max):
        print(chr(ord("a") + i), end=" ")
    print()
    for i in range(y_max):
        print(i + 1, end="\t")
        for j in range(x_max):
            print(my_board[j][i], end=" ")
        print()
    print()


def draw_rect(x_pos, y_pos, possible=False, wall=False):
    coord = [x_pos * (padding + tile_size) + padding + 1, y_pos * (padding + tile_size) + padding + 1,
             (x_pos + 1) * (padding + tile_size), (y_pos + 1) * (padding + tile_size)]
    if possible:
        canvas.create_rectangle(coord, fill=cyan, activefill=yellow)
    elif wall:
        canvas.create_rectangle(coord, fill=red)
    else:
        canvas.create_rectangle(coord, fill=green)


def draw_circle(x_pos, y_pos, fill_color):
    coord = [x_pos * (padding + tile_size) + 2 * padding + 1, y_pos * (padding + tile_size) + 2 * padding + 1,
             (x_pos + 1) * (padding + tile_size) - padding, (y_pos + 1) * (padding + tile_size) - padding]
    canvas.create_oval(coord, fill=fill_color)


def make_move(x, y):
    if x * y_max + y not in possible_moves:
        return False
    next_turn(x, y)
    return True


def click(event=None):
    x = int((event.x - padding) / (padding + tile_size))
    y = int((event.y - padding) / (padding + tile_size))
    if x * y_max + y not in possible_moves:
        return
    next_turn(x, y)


def next_turn(x_pos, y_pos):
    global turn, possible_moves
    for pos in possible_moves:
        draw_rect(int(pos / y_max), pos % y_max)
    if turn == black:
        color_symbol = "X"
    else:
        color_symbol = "O"
    board[x_pos][y_pos] = color_symbol
    draw_circle(x_pos, y_pos, turn)
    possible_moves -= {x_pos * x_max + y_pos}
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == color_symbol and (i != x_pos or j != y_pos):
                board[i][j] = 'W'
            if board[i][j] == 'X':
                draw_circle(i, j, black)
            elif board[i][j] == 'O':
                draw_circle(i, j, white)
            elif board[i][j] == 'W':
                draw_rect(i, j, wall=True)
    winner_candidate = color_symbol
    turn = whose_turn(board, turn)
    if turn is None:
        print_board(board)
        print("{} win".format(winner_candidate))

        return
    for pos in possible_moves:
        draw_rect(int(pos / y_max), pos % y_max, True)
    print_board(board)
    if players[turn] != "Player":
        root.update()
        '''you may change the code below'''
        # time.sleep(delay_time)
        #         start = time.time()
        move, val = players[turn].best_strategy(board, turn)
        #         time_used = round(time.time()-start, 3)
        #         player_max_times[turn] = max(player_max_times[turn], time_used)
        #         player_total_times[turn] = player_total_times[turn]+time_used
        next_turn(move[0], move[1])


def init(choice_menu, e1, e2, v1, v2):
    global turn_off_printing, turn, root, canvas, p1_name, p2_name, players, player_types
    if turn_off_printing:
        sys.stdout = open(os.devnull, 'w')
    p1_name = e1.get()
    p2_name = e2.get()
    players[black] = player_types[v1.get()]
    players[white] = player_types[v2.get()]
    p1_name = players[black]
    p2_name = players[white]
    if players[black] == "Random":
        players[black] = RandomPlayer()
    elif players[black] == "Custom":
        players[black] = CustomPlayer()
    if players[white] == "Random":
        players[white] = RandomPlayer()
    elif players[white] == "Custom":
        players[white] = CustomPlayer()
    choice_menu.destroy()
    root = tk.Tk()
    root.title("Isolation Game")
    root.resizable(width=False, height=False)
    canvas = tk.Canvas(root, width=board_x, height=board_y, bg=brown)
    canvas.bind("<Button-1>", click)
    canvas.grid(row=0, column=0, columnspan=2)
    for i in range(x_max):
        board.append([])
        for j in range(y_max):
            draw_rect(i, j)
            board[i].append(".")
    turn = whose_turn(board, turn)
    for pos in possible_moves:
        draw_rect(int(pos / y_max), pos % y_max, True)
    print_board(board)
    print("whose turn", players[turn])
    if players[turn] != "Player":
        root.update()
        '''you may change the code below'''
        # time.sleep(delay_time)
        move, idc = players[turn].best_strategy(board, turn)
        next_turn(move[0], move[1])
    root.mainloop()


def menu():
    global p1_name, p2_name, radio_on, radio_off
    choice_menu = tk.Tk()
    choice_menu.title("Menu")
    choice_menu.resizable(width=False, height=False)
    tk.Label(text="Black", font=("Arial", 30), bg=black, fg=grey).grid(row=0, column=0,
                                                                       sticky=tk.W + tk.E + tk.N + tk.S)
    tk.Label(text="White", font=("Arial", 30), bg=white, fg=black).grid(row=0, column=1,
                                                                        sticky=tk.W + tk.E + tk.N + tk.S)
    v1 = tk.IntVar()
    v2 = tk.IntVar()
    v1.set(0)
    v2.set(0)
    tk.Radiobutton(text="Player", compound=tk.LEFT, font=("Arial", 20), bg=black, fg=grey, anchor=tk.W, variable=v1,
                   value=0).grid(row=1, column=0, sticky=tk.W + tk.E + tk.N + tk.S)
    tk.Radiobutton(text="Player", font=("Arial", 20), bg=white, fg=black, anchor=tk.W, variable=v2, value=0).grid(row=1,
                                                                                                                  column=1,
                                                                                                                  sticky=tk.W + tk.E + tk.N + tk.S)
    tk.Radiobutton(text="Random", font=("Arial", 20), bg=black, fg=grey, anchor=tk.W, variable=v1, value=1).grid(row=2,
                                                                                                                 column=0,
                                                                                                                 sticky=tk.W + tk.E + tk.N + tk.S)
    tk.Radiobutton(text="Random", font=("Arial", 20), bg=white, fg=black, anchor=tk.W, variable=v2, value=1).grid(row=2,
                                                                                                                  column=1,
                                                                                                                  sticky=tk.W + tk.E + tk.N + tk.S)
    tk.Radiobutton(text="Custom", font=("Arial", 20), bg=black, fg=grey, anchor=tk.W, variable=v1, value=2).grid(row=3,
                                                                                                                 column=0,
                                                                                                                 sticky=tk.W + tk.E + tk.N + tk.S)
    tk.Radiobutton(text="Custom", font=("Arial", 20), bg=white, fg=black, anchor=tk.W, variable=v2, value=2).grid(row=3,
                                                                                                                  column=1,
                                                                                                                  sticky=tk.W + tk.E + tk.N + tk.S)
    e1 = tk.Entry(font=("Arial", 15), bg=black, fg=grey, width=12)
    e2 = tk.Entry(font=("Arial", 15), bg=white, fg=black, width=12)
    e1.insert(0, "Player 1 Name")
    e2.insert(0, "Player 2 Name")
    e1.grid(row=99, column=0, sticky=tk.W + tk.E + tk.N + tk.S)
    e2.grid(row=99, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
    tk.Button(text="Begin", font=("Arial", 15), bg=white, fg=black,
              command=lambda: init(choice_menu, e1, e2, v1, v2)).grid(row=100, column=0, columnspan=2,
                                                                      sticky=tk.W + tk.E + tk.N + tk.S)
    choice_menu.mainloop()


menu()