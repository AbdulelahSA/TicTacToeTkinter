import random
from tkinter import *
from tkinter.messagebox import *

# Variables to keep track of game state
mode = -1  # Mode: 1 for playing with computer, 2 for playing with another player
player1 = ""  # Symbol for player 1
player2 = ""  # Symbol for player 2
turn1 = 1  # Who plays first: 1 for player 1, 2 for player 2
nowturn = 1  # Whose turn it is currently
top = Tk()
top.title("x o game")

# Dictionary to represent the game board
board = {0: {0: StringVar(), 1: StringVar(), 2: StringVar()},
         1: {0: StringVar(), 1: StringVar(), 2: StringVar()},
         2: {0: StringVar(), 1: StringVar(), 2: StringVar()}}

# Function to place X or O on the board
def placement(place1, place2):
    global board, nowturn, mode

    # Check if the cell is empty
    if board[place1][place2].get() == '':
        # Set X or O based on the player's turn
        if nowturn == 1:
            board[place1][place2].set(player1)
            nowturn = 2
            l1.set(player2 + ' turn')
        else:
            board[place1][place2].set(player2)
            nowturn = 1
            l1.set(player1 + ' turn')

        # Check if someone won or the board is full
        winbool, winner = win()
        if winbool:
            gamefinish((winner + " is the winner"))
            gamerestart()
            return
        if full():
            gamefinish()
            gamerestart()
            return

        # If playing with computer, let computer make a move
        if mode == 1:
            availabl = [i for i in range(9) if board[i // 3][i % 3].get() == '']
            place = random.choice(availabl)
            board[place // 3][place % 3].set(player2)
            nowturn = 1
            l1.set(player1 + ' turn')

            winbool, winner = win()
            if winbool:
                gamefinish((winner + " is the winner"))
                gamerestart()
                return
            if full():
                gamefinish()
                gamerestart()
                return
        else:
            pass
    else:
        pass

# Function to check if someone has won
def win():
    streak = [''] * 3  # Initialize a list for streaks

    # Check rows
    for i in range(3):
        for j in range(3):
            streak[j] = board[i][j].get()
        if streak[0] == streak[1] == streak[2] != '':
            return True, streak[0]

    # Check columns
    for i in range(3):
        for j in range(3):
            streak[j] = board[j][i].get()
        if streak[0] == streak[1] == streak[2] != '':
            return True, streak[0]

    # Check diagonals
    if board[0][0].get() == board[1][1].get() == board[2][2].get() != '':
        return True, board[0][0].get()
    if board[0][2].get() == board[1][1].get() == board[2][0].get() != '':
        return True, board[0][2].get()

    # No winner
    return False, ''

# Function to check if the board is full
def full():
    for i in range(3):
        for j in range(3):
            if board[i][j].get() == '':
                return False
    return True

# Function to display the winner or draw message
def gamefinish(winner='draw'):
    showinfo("Game finish", winner)

# Function to restart the game
def gamerestart():
    if askquestion('game restart', 'another game?') == 'yes':
        newgame()
    else:
        top.quit()

# Function to start a new game
def newgame():
    global mode, player1, player2, turn1, board, nowturn

    # Reset board
    for i in range(3):
        for j in range(3):
            board[i][j].set('')

    # Choose game mode: with computer or with another player
    if askquestion('Game mode', 'select yes if you want to play with computer.\nselect no if you want to play with other player.') == 'yes':
        mode = 1
    else:
        mode = 2

    # Choose X or O for player 1
    if askquestion('x o select', 'select yes if you want player 1 to use X.\nselect no if you want player 1 to use O.') == 'yes':
        player1 = 'X'
        player2 = 'O'
    else:
        player1 = 'O'
        player2 = 'X'

    # Choose who plays first
    if askquestion('turn select', 'select yes if you want player 1 to play first.\nselect no if you want player 1 to play second.') == 'yes':
        turn1 = 1
        l1.set(player1 + " turn")
    else:
        turn1 = 2
        l1.set(player2 + ' turn')
    nowturn = turn1

# Initialize board and start the game
for i in range(3):
    for j in range(3):
        board[i][j].set('')
l1 = StringVar()
label1 = Label(top, textvariable=l1)
l1.set('')
label1.grid(column=0, row=0, columnspan=4)

# Create buttons for the board
buttons = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
for i in range(3):
    for j in range(3):
        buttons[i][j] = Button(top, textvariable=board[i][j], command=lambda index1=i, index2=j: placement(index1, index2), height=5, width=10)
        buttons[i][j].grid(column=i+1, row=j+1)

# Start a new game
newgame()
top.mainloop()
