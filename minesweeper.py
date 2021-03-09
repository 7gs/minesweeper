import random
import pandas as pd

def createBoard(rows, cols, mine_count):
    
    mine_locations = []
    board_list = []
    count = 0
    on_left = False
    on_right = False
    on_top = False
    on_bottom = False

    while len(mine_locations) < 10:
       
        new_spot = random.randint(0, num_cells)

        if new_spot not in mine_locations:
            mine_locations.append(new_spot)

    for i in range (1, num_cells + 1):

        if i <= cols:
            on_top = True
        if i > (num_cells - cols):
            on_bottom = True
        if i % cols + 1 == 1:
            on_right = True
        if (i - 1) % cols == 0:
            on_left = True

        if i in mine_locations:
            board_list.append("x")
        else:
            # check square to the left
            if i - 1 in mine_locations and not on_left:
                count += 1
            # check square to the right
            if i + 1 in mine_locations and not on_right:
                count += 1
            # check square directly above
            if i - cols in mine_locations and not on_top:
                count += 1
            # check square above and to the right
            if i - cols + 1 in mine_locations and not on_top and not on_right:
                count += 1
            # check square above and to the left
            if i - cols - 1 in mine_locations and not on_top and not on_left:
                count += 1
            # check square below
            if i + cols in mine_locations and not on_bottom:
                count += 1
            # check square below and to the right
            if i + cols + 1 in mine_locations and not on_bottom and not on_right:
                count += 1
            # check square below and to the left
            if i + cols - 1 in mine_locations and not on_bottom and not on_left:
                count += 1
            
            if count == 0:
                board_list.append(" ")
            else:
                board_list.append(count)
        
        count = 0
        on_top = False
        on_bottom = False
        on_left = False
        on_right = False
    
    return board_list

def printBoard(board_to_print):

    printable_board = []
    new_row = []

    for i in board_to_print:
        new_row.append(i)
        
        if len(new_row) == actual_cols:
            printable_board.append(new_row)
            new_row = []

    df = pd.DataFrame(printable_board)
    
    print("")
    print("***********************")
    print("*** Flags left: " + str(flags))
    print("***********************")
    print("")
    print(df)
    print("")

    return

def processAction(move, target_index):

    global running
    global flags
    global revealed

    on_left = False
    on_right = False
    on_bottom = False
    on_top = False
    
    commands = "fpqFPQ"

    if move in commands:

        if move == "f" or move == "F":

            if dummy_board[target_index] == "F":
                dummy_board[target_index] = "-"
                flags += 1
            else:
                dummy_board[target_index] = "F"
                flags -= 1

        elif move == "p" or move == "P":
            
            if board[target_index] == "x":
                
                revealMines()
                printBoard(dummy_board)
                print("*****************")
                print("** GAME_OVER!! **")
                print("*****************")
                print("")
                running = False

            elif board[target_index] == " ":
            
                spot_list = []
                
                if target_index <= actual_cols:
                    on_top = True
                if target_index >= (num_cells - actual_cols):
                    on_bottom = True
                if (target_index + 1) % actual_cols == 0:
                    on_right = True
                if target_index % actual_cols == 0:
                    on_left = True

                # check square to left
                if not on_left and board[target_index - 1] == " " and dummy_board[target_index - 1] == "-":
                    spot_list.append(target_index - 1)
                # check square to right
                if not on_right and board[target_index + 1] != "x" and dummy_board[target_index + 1] == "-":
                    spot_list.append(target_index + 1)
                # check square above
                if not on_top and board[target_index - actual_cols] != "x" and dummy_board[target_index - actual_cols] == "-":
                    spot_list.append(target_index - actual_cols)
                # check square above and to right
                if not on_top and not on_right and board[target_index - actual_cols + 1] != "x" and dummy_board[target_index - actual_cols + 1] == "-":
                    spot_list.append(target_index - actual_cols + 1)
                # check square above and to left
                if not on_top and not on_left and board[target_index - actual_cols - 1] != "x" and dummy_board[target_index - actual_cols - 1] == "-":
                    spot_list.append(target_index - actual_cols - 1)
                # check square below
                if not on_bottom and board[target_index + actual_cols] != "x" and dummy_board[target_index + actual_cols] == "-":
                    spot_list.append(target_index + actual_cols)
                # check square below and to right
                if not on_bottom and not on_right and board[target_index + actual_cols + 1] != "x" and dummy_board[target_index + actual_cols + 1] == "-":
                    spot_list.append(target_index + actual_cols + 1)
                # check square below and to left
                if not on_bottom and not on_left and board[target_index + actual_cols - 1] != "x" and dummy_board[target_index + actual_cols - 1] == "-":
                    spot_list.append(target_index + actual_cols - 1)

                dummy_board[target_index] = " "
                                
                for i in spot_list:
                    processAction("P", i)

            else:
                dummy_board[target_index] = board[target_index]


        elif move == "q" or move == "Q":
            running = False

    else:
        print("")
        print("************************************")
        print("**** That is an invalid command ****")
        print("************************************")

    return

def revealMines():

    global dummy_board
    
    for x in range (0, num_cells):
        if board[x] == "x":
            dummy_board[x] = "x"

    return

def checkForWin():

    exposed_count = 0

    for i in range (0, num_cells):

        if dummy_board[i] != "-" and dummy_board[i] != "F":
            exposed_count += 1

    if exposed_count == num_cells - actual_mines:
        return True

    return False

#### Game Settings ####

# beginner mode parameters
beg_rows = 9
beg_cols = 9
beg_mines = 10

# intermediate mode parameters
int_rows = 16
int_cols = 16
int_mines = 40

# expert mode parameters
exp_rows = 16
exp_cols = 30
exp_mines = 99


#### Main Program ####
print("")
print("***********************")
print("Welcome to Minesweeper!")
print("***********************")
print("")

difficulty = int(input("Please choose your difficulty: 1 - Beginner, 2 - Intermediate, 3 - Expert:"))

actual_rows = 0
actual_cols = 0
actual_mines = 0
dummy_board = []
running = True
revealed = 0

if difficulty == 1:
    actual_rows = beg_rows
    actual_cols = beg_cols
    actual_mines = beg_mines
elif difficulty == 2:
    actual_rows = int_rows
    actual_cols = int_cols
    actual_mines = int_mines
elif difficulty == 3:
    actual_rows = exp_rows
    actual_cols = exp_cols
    actual_mines = exp_mines

flags = actual_mines
num_cells = actual_rows * actual_cols

board = createBoard(actual_rows, actual_cols, actual_mines)

for i in range(1, (actual_rows * actual_cols) + 1):
    dummy_board.append("-")

while running:

    # Print board
    printBoard(dummy_board)

    # Request action
    print("Actions: F = Flag, P = Press, Q = Quit")
    print("Move Syntax: [action] [row] [col]")
    print("")
    action = (input("What is your move?"))

    #parse input
    move_list = action.split(" ")
    move = move_list[0]
    shrow = int(move_list[1])
    shcol = int(move_list[2])
    target_index = (shrow * actual_cols) + shcol

    processAction(move, target_index)

    if checkForWin():
        printBoard(dummy_board)
        print("*****************")
        print("*** YOU WIN!! ***")
        print("*****************")
        running = False