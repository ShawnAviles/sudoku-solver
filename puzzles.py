# Shawn Aviles 12/4/2021
# I pledge my honor that I have abided by the Stevens Honor System
import random

board1 = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]

board2 = [
    [0, 2, 0, 8, 0, 0, 0, 4, 3],
    [0, 5, 0, 3, 0, 9, 0, 0, 0],
    [4, 0, 0, 0, 0, 0, 1, 9, 0],
    [6, 8, 0, 1, 3, 2, 0, 0, 0],
    [7, 3, 0, 0, 9, 8, 0, 6, 0],
    [0, 1, 9, 0, 6, 4, 0, 3, 0],
    [3, 4, 0, 0, 0, 0, 7, 8, 6],
    [1, 0, 7, 0, 8, 7, 0, 5, 0],
    [0, 0, 8, 4, 0, 7, 0, 0, 9]
]

board3 = [ 
    [3, 0, 6, 5, 0, 8, 4, 0, 0], 
    [5, 2, 0, 0, 0, 0, 0, 0, 0], 
    [0, 8, 7, 0, 0, 0, 0, 3, 1], 
    [0, 0, 3, 0, 1, 0, 0, 8, 0], 
    [9, 0, 0, 8, 6, 3, 0, 0, 5], 
    [0, 5, 0, 0, 9, 0, 6, 0, 0], 
    [1, 3, 0, 0, 0, 0, 2, 5, 0], 
    [0, 0, 0, 0, 0, 0, 0, 7, 4], 
    [0, 0, 5, 2, 0, 6, 3, 0, 0] ]

def getPuzzle():
    r = random.randint(0,2)
    if r == 0:
        board = board1
    elif r == 1:
        board = board2   
    else:
        board = board3
    return board