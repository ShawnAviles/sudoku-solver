# Shawn Aviles 12/4/2021
# I pledge my Honor that I have abided by the Stevens Honor System -Shawn Aviles
# Note: All the sources to produce this project are cited below. No code was just copied and pasted from online. 
# Tutorials were followed, notes for undertstanding were commented, and adjustments were made when producing this project 
# https://www.geeksforgeeks.org/sudoku-backtracking-7/      - algoritim background
# https://youtu.be/jO6qQDNa2UY                              - pygame basics
# https://youtu.be/eqUwSA0xI-s                              - Sodoku Solver 1 Tutorial
# https://youtu.be/lK4N8E6uNr4                              - Sodoku Solver 2 Tutorial

# GUI
import pygame
from sodokuSolver import solve, isValid, findEmpty 
import puzzles
import time
import random

pygame.font.init()
WHITE = (255, 255, 255)
BLACK = (0,0,0)

# grid holds a bunch of different cube objects in a row-column structure 
# the whole grid 
class Grid:
    # starting boards
    board = puzzles.getPuzzle()

    # constructor 
    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win

    # board (gui that user sees) and model (is what the computer uses) are separate things
    # model is what it attempts to solve
    # updated integer values that are entered not penciled in
    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    # sets permanent value for cube objects after checking that it is valid to do so
    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if isValid(self.model, val, (row,col)) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    # sets temporary value for cube object
    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    # displays grid in window
    def draw(self):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            # thickness increases for every 3 lines 
            # rows
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, WHITE, (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.win, WHITE, (i * gap, 0), (i * gap, self.height), thick)
        
        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win, i, j)

    # selects square that clicked
    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    # clears selected cube to defualt blank 0 value
    # only works on temp not value
    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    # returns position of the cube clicked
    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    # returns true if all values != 0 (checks that they're answered correect) 
    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    # solves the gui using similar method as solve() in sodokuSolver file
    def solve_gui(self):
        self.update_model()
        find = findEmpty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if isValid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False
    
    # setter for cubes to access later to reset
    def set_cubes(self, val):
        self.cubes = val


# individual cubes in grid
class Cube:
    rows = 9
    cols = 9

    # constructor
    def __init__(self, value, row, col, width, height):
        self.value = value      # the set value (from solved board)
        self.temp = 0           # value user enters (greyed out)
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.textColor = WHITE   # default white color 

    # functions draws squares
    def draw(self, win, i, j):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128)) # grey temp value user inputs before clicking enter
            text_rect = text.get_rect(center = (gap/2 + gap * j, gap/2 + gap * i))
            win.blit(text, text_rect)
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (self.textColor))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    # used when solving the gui
    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, BLACK, (x, y, gap, gap), 0) # color of cube when solving 

        text = fnt.render(str(self.value), 1, (self.textColor))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3) 
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    # setters
    def set(self, val):
        self.value = val
        
    # used when changing text to grey when "RESET" button appears
    def set_textColor(self, r, g, b):
        self.textColor = r, g ,b

    def set_temp(self, val):
        self.temp = val

# redraws and updates window every loop
def redraw_window(win, board, time, strikes, done):
    # background color
    win.fill(BLACK) 
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 30)
    text = fnt.render("Time: " + format_time(time), 1, WHITE)
    win.blit(text, (560 - 175, 560))
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    # Draw grid and board
    board.draw()
    # Draw reset button
    if done:
        pygame.draw.rect(win, BLACK, (560/2 - 70, 500/2 - 25, 138, 45)) 
        fnt = pygame.font.SysFont("comicsans", 50)
        text = fnt.render("RESET", 1, WHITE)
        text_rect = text.get_rect(center = (560/2, 500/2))
        win.blit(text,text_rect)
        pygame.draw.rect(win, (0, 0, 255), (560/2 - 70, 500/2 - 25, 138, 45), 6) 
    


# display time in bottom right corner
def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60

    secS = str(sec)
    minuteS = str(minute)
    hourS = str(hour)
    
    # formats numbers to all take up two spots
    if sec == 0:
        secS = "00"
    elif sec < 10:
        secS = "0" + secS
    
    if minute == 0:
        minuteS = "00"
    elif minute < 10:
        minuteS = "0" + minuteS
        
    if hour == 0:
        hourS = "00"
    elif hour < 10:
        hourS = "0" + hourS
    
    mat = hourS + ":"+ minuteS + ":" + secS
    return mat


def main():
    rows, cols, width, height = 9, 9, 540, 540
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    board = Grid(rows, cols, width, height, win)
    key = None
    run = True
    start = time.time()     # total seconds from epoch (time at start of code when window opens)
    strikes = 0
    done = False            # updated when board is solved, allows end_time to be saved once and gameOver effect to occur once
    end_time = 0
    gameOver = False        # user lost - >5 strikes
    
    
    # constantly updating the board and checking for inputs
    while run:
        # current seconds - seconds from opening window = time elapsed with game open
        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if not done:    # take input if game running
                # if button pressed on keyboard
                if event.type == pygame.KEYDOWN:
                    # K_X are keyboard keys aboveletters (~60% keyboard)
                    # K_KPX are keyboard keys from keypad right of letters (~100% keyboard)
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        key = 1
                    if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        key = 2
                    if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        key = 3
                    if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        key = 4
                    if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        key = 5
                    if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        key = 6
                    if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                        key = 7
                    if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        key = 8
                    if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                        key = 9
                    if event.key == pygame.K_DELETE:
                        board.clear()
                        key = None

                    if event.key == pygame.K_SPACE:
                        board.solve_gui()

                    if event.key == pygame.K_RETURN and not done:
                        i, j = board.selected
                        if board.cubes[i][j].temp != 0:     #checks something is entered 
                            if board.place(board.cubes[i][j].temp):
                                print("Success")
                            else:
                                if strikes < 5:
                                    strikes += 1
                                    print("Wrong")
                                else: 
                                    gameOver = True
                            key = None

            if event.type == pygame.MOUSEBUTTONDOWN and not done:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
            
            # when game is done and press reset
            if event.type == pygame.MOUSEBUTTONDOWN and done:
                pos = pygame.mouse.get_pos()
                if (pos[0] >= 560/2 - 70 and pos[0] <= 560/2 - 70 + 138) and (pos[1] >= 500/2 - 25 and pos[1] <= 500/2 - 25 + 45):
                    strikes = 0
                    [[board.cubes[i][j].set_textColor(255,255,255) for j in range(board.cols)] for i in range(board.rows)]
                    board.set_cubes([[Cube(board.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)])
                    start = time.time()
                    done = False
                    gameOver = False
                     
        if board.selected and key != None:
            board.sketch(key)

        # ends timer
        if (board.is_finished() and not done) or (gameOver and not done):
            end_time = round(time.time() - start)
            play_time = end_time
            print("Game Over")
            [[board.cubes[i][j].set_textColor(90,90,90) for j in range(board.cols)] for i in range(board.rows)]
            done = True
            
        # displays end_time if it exists
        if end_time > 0 and done:
            redraw_window(win, board, end_time, strikes, done)
        else:
            redraw_window(win, board, play_time, strikes, done)
        pygame.display.update()
        
main()
pygame.quit()