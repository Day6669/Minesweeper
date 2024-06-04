import random
from dataclasses import dataclass
import time

# define globals
WIDTH = 0
HEIGHT = 0
board = None
BombsFlagged = 0
flagsUsed = 0


@dataclass
# Creates a class containing three of the values necessary for the game to function
class Tile:
    value: int
    opened: bool = False
    isBomb: bool = False
    isFlagged: bool = False


def create_board(bombs):  # makes a list and then prints it
    # Adds a bunch of empty tiles into an array and then adds the array onto the board
    arr = [[Tile(value=0) for _ in range(WIDTH)] for _ in range(HEIGHT)]
    bombsBoard = placeBombs(bombs, arr)
    # Assigns how close tiles are to a bomb tile when you successfully select a empty tile
    realBoard = assignNumbers(bombsBoard)

    # test to see of the file exists
    try:
        # if we open it successfully then it exists
        file = open('leaderboard.txt', 'r')
        file.close()
    except:
        # if it errors then is doesn't exist and we need to make one
        with open('leaderboard.txt', 'w') as leaderboard:
            leaderboard.write('Name     | Difficulty         | Time\n')
            leaderboard.write('-------------------------------------\n')

    return realBoard


def tileValue(row, col, board):
    """
    Calculate the number of bombs around a tile
    """
    # get the surrounding tiles
    coords = [(row-1, col-1), (row-1, col), (row-1, col+1), (row, col-1),
              (row, col+1), (row+1, col-1), (row+1, col), (row+1, col+1)]
    # set a counter at 0 bombs
    value = 0
    # loop surrounding tiles
    for coord in coords:
        # check if in range and if it is a bomb add 1 to counter
        newRow, newCol = coord
        if (newRow >= 0 and newRow <= HEIGHT-1) and (newCol >= 0 and newCol <= WIDTH-1):
            if board[newRow][newCol].isBomb:
                value = value + 1
    return value


def assignNumbers(boardNew):
    # add the cues to the board
    for row in range(HEIGHT):
        for col in range(WIDTH):
            # skip the bomb tiles
            if boardNew[row][col].isBomb:
                continue
            value = tileValue(row, col, boardNew)
            boardNew[row][col].value = value
    return boardNew


def placeBombs(n, arr):
    bombCount = 0
    # keep going until you have desired bombs otherwise you could have 1 less if
    # it tries to place a bomb on top of a tile which already has a bomb
    while bombCount < n:
        # Randomly places bombs on a row
        row = random.randint(0, WIDTH - 1)
        # Randomly places bombs in a column
        column = random.randint(0, HEIGHT - 1)
        # only place if it isn't already a bomb
        if not arr[column][row].isBomb:
            arr[column][row] = Tile(value=-1, isBomb=True)
            bombCount += 1

    return arr


def displayBoard():
    # print the board array on the screen

    # generate a list of numbers for columns and convert to strings
    colValues = map(str, list(range(1, WIDTH+1)))
    # name each column 4 wide
    formattedCols = map(lambda number: number.center(4), colValues)
    print(f"     |  {' '.join(formattedCols)}")
    print(" - " * ((WIDTH*2)-2))
    for row in range(HEIGHT):
        print(f"{str(row+1).center(4)} | ", end="")
        for col in range(WIDTH):
            tile = board[row][col]
            if tile.isBomb and tile.opened:
                print('  *  ', end="")
            elif tile.isFlagged and not tile.opened:
                print("  F  ", end="")
            elif tile.value == 0 and tile.opened:
                print('     ', end="")
            elif tile.opened:
                print(f"  {tile.value}  ", end="")
            else:
                print("  □  ", end="")
        print(" |\n")


def getInput(type_, bound):
    # keep asking for input until it is valid
    while True:
        inputValue = input(f"Pick a {type_} >> ")
        if inputValue.isnumeric():
            inputValue = int(inputValue)-1
            if inputValue >= 0 and inputValue <= bound-1:
                break
            else:
                print("Values out of range of the board\n")
        else:
            print("Please enter a number\n")
    return inputValue


def move(row, column):
    # open the passed in tile
    board[row][column].opened = True

    # get coords of surrounding tiles
    coords = [
        (row-1, column-1), (row-1, column), (row-1, column + 1),
        (row, column-1),               (row, column + 1),
        (row+1, column-1), (row+1, column), (row+1, column + 1),
    ]

    # if you see a tile with a value then stop the call
    if board[row][column].value != 0:
        return

    # loop surrounding tiles
    for coord in coords:
        newRow, newCol = coord
        # if in bounds then recursive call if it hasn't been opended
        if newRow >= 0 and newRow <= HEIGHT-1 and newCol >= 0 and newCol <= WIDTH-1:
            if not board[newRow][newCol].opened:
                move(newRow, newCol)


def makeMove(row, col):
    # get a tile from the board
    tile = board[row][col]
    global BombsFlagged, flagsUsed

    # checks if you want to open or flag
    option = input("Do you want to (O) Open or (F) Flag the tile ").upper()

    if option == "O":  # if we want to open we open the bomb if its a bomb if its not a bomb we call recursive move
        if tile.isBomb:
            tile.opened = True
            # setting game over
            return True
        else:
            move(row, col)

    elif option == "F":  # if we want to flag only flag if its not opened
        if not tile.opened:
            if tile.isFlagged:
                flagsUsed -= 1
                tile.isFlagged = False
            else:
                # if it isnt open then flag it and increment bomb and flag counters
                tile.isFlagged = True
                flagsUsed += 1
                if tile.isBomb:
                    BombsFlagged += 1
        else:
            print("You can't flag an open tile")


def formatTime(time):
    # convert the time taken to minutes
    mins = time / 60
    return f'Time Taken: {round(mins,2)}m'


# opens a file and adds your name and time
def saveLeaderboard(name, time, difficulty):
    with open("leaderboard.txt", "a") as file:
        file.write(f'{name} | {difficulty} | {time}')


def getDiff(option):  # converts a number to a difficulty
    if option == 1:
        return 'Beginner'
    elif option == 2:
        return 'Medium'
    elif option == 3:
        return 'Hard'


if __name__ == "__main__":
    print('Welcome to Minesweeper!!')
    print('========================\n')

    print('Please Choose a Game mode:')
    print('''
        1) Beginner
        2) Medium
        3) Hard
    ''')

    # keep asking for input until its correct
    invalidInput = True
    while invalidInput:
        option = input(">> ")
        # check if number
        if option.isnumeric():
            uOption = int(option)
            # check range
            if uOption >= 1 and uOption <= 3:
                invalidInput = False
            else:
                print("Please choose one between 1 and 3")
        else:
            print("Please Enter a Number!")

    # sets the board and bomb size based on the difficulty returns a tuple
    if uOption == 1:
        size = (9, 9, 10)
    elif uOption == 2:
        size = (16, 16, 40)
    elif uOption == 3:
        size = (30, 16, 99)

    # assigns values to variables from size
    WIDTH = size[0]
    HEIGHT = size[1]
    _,  _, bombsTotal = size

    # makes board
    board = create_board(bombsTotal)
    # takes the current time
    start = time.time()
    displayBoard()

    gameOver = False
    bombsLeft = bombsTotal

    # main game loop
    while not gameOver:
        # caculate metrics for game over
        bombsLeft = bombsTotal-BombsFlagged
        flagsLeft = bombsTotal - flagsUsed
        print('=============')
        print('Flags Left ', flagsLeft)
        # win condition
        if bombsLeft == 0 or flagsLeft == 0:
            gameOver = True
            continue

        row = getInput("row", HEIGHT)
        col = getInput("column", WIDTH)

        gameOver = makeMove(row, col)
        displayBoard()

    else:
        # game over condition
        bombsLeft = size[2]-BombsFlagged
        # elapsed time
        end = time.time()
        if bombsLeft == 0 and flagsLeft == 0:
            print('You win!')
            t = formatTime(end-start)
            print(t)
            name = input("What is your name?")
            # get difficulty
            diff = getDiff(option)
            saveLeaderboard(name, t, diff)
        else:
            print("You are dead! All hope in humanity is lost.")
