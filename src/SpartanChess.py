import tkinter
from tkinter import * 
from tkinter.font import Font
from functools import partial

from ChessPieces import *
from ChessLearning import *

#python 3
def updateButtons(board, buttons):
    for r in range(8):
        for c in range(8):
            buttons[r][c]["text"] = unicodeConv[globalGameState.board[r][c]]

def checkerTheButtons(buttons):
    for r in range(8):
        i = 1 if(r % 2 == 0) else 0
        for c in range(8):
            if(i % 2 == 0):
                buttons[r][c]['bg'] = 'light grey'
            else:
                buttons[r][c]['bg'] = 'white'
            i += 1

def displayPossibleMoves(gameState, buttons, row=None, col=None):
    checkerTheButtons(buttons)
    moves = getAllValidMoves(gameState)
    for move in moves:
        r, c = move[0]
        if(row != None and col != None):
            if(r != row or c != col):
                continue

        buttons[r][c]['bg'] = 'green'
        rowEnd, colEnd = move[1]
        if(isEmptyPiece(globalGameState.board[rowEnd][colEnd])):
            buttons[rowEnd][colEnd]['bg'] = 'blue'
        else:
            buttons[rowEnd][colEnd]['bg'] = 'red'

def buttonClick(row, col):
    displayPossibleMoves(globalGameState, buttons, row, col)

globalGameState = GameState()

root = Tk()

Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)
root.wm_title("SpartanChess")

topLevelFrame = Frame(root)
topLevelFrame.grid(row=0, column=0, sticky=N+S+E+W)

boardFrame = Frame(topLevelFrame)
boardFrame.grid(row=0, column=0, sticky=N+S+E+W)

Grid.rowconfigure(topLevelFrame, 0, weight=1)
Grid.columnconfigure(topLevelFrame, 0, weight=5)
Grid.columnconfigure(topLevelFrame, 1, weight=1)

chessFont = Font(family='Tahoma', size=24, weight='bold')
labelFont = Font(family='Tahoma', size=24, weight='normal')

buttons = []
for r in range(8):
    row = []
    for c in range(8):
        button = Button(boardFrame, text='♔', command=partial(buttonClick, r, c))
        button.grid(row=r, column=c+1, sticky=N+S+E+W)
        button.configure(font=chessFont)
        row.append(button)

    colLabel = Label(boardFrame, text=rowToNotation[r], font=labelFont)
    colLabel.grid(row=r, column=0, sticky=N+S+E+W)
    rowLabel = Label(boardFrame, text=colToNotation[r], font=labelFont)
    rowLabel.grid(row=8, column=r+1, sticky=N+S+E+W)

    buttons.append(row)

updateButtons(globalGameState.board, buttons)
checkerTheButtons(buttons)
root.mainloop()
