# Shawn Aviles 12/4/2021
# I pledge my honor that I have abided by the Stevens Honor System

# TOPICS LEARNED - creating basic GUI & recursive back tracking

board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

# function returns solved sodoku puzzle via recursion
def solve(bo):
    # finds position of empty space on board
    find = findEmpty(bo)
    
    # base case - 
    # if everything is filled then we are done with the puzzle
    # else save position values of the empty space and move to next step
    if not find:
        return True
    else:
        row, col = find
    
    # attempts to place a digit 1-9 in emptySpace
    for i in range(1,10):
        # checks if the digit is Valid (according to Sodoku Rules)
        if isValid(bo, i, (row, col)):
            # if valid, save digit in the empty space on board
            bo[row][col] = i
            
            # returns true and stops recursion when board is filled
            if solve(bo):
                return True
            
            # if the next digit is not valid (which is when "solve(bo)" is false)
            # then we back track and reset empty space to 0 
            # we keep doing this until solution is satisfactory 
            bo[row][col] = 0
            
    # if none of the digits are valid return false 
    return False


# function check for if number is valid 
def isValid(bo, num, pos):
    # check row 
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos [0] != i:
            return False
        
    # check box
    boxX = pos[1] // 3
    boxY = pos[0] // 3
    
    for i in range(boxY * 3, boxY * 3 + 3):
        for j in range (boxX * 3, boxX * 3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False
            
    return True


# function interprets 9x9 array and displays board 
def printBoard(bo):
    # row
    for i in range (len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - -")
        
        # column
        for j in range(len(bo[i])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")


# function returns position of first empty space on the board 
def findEmpty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[i])):
            if bo[i][j] == 0:
                return (i,j) # returns row and column indices

printBoard(board)
solve(board)
print("---------------------------------")
printBoard(board)
