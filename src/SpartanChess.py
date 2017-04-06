import tkinter
from tkinter import * 
from tkinter.font import Font
from functools import partial

from ChessPieces import *
from ChessLearning import *
from PgnParser import *
from PromotionChooserDialog import *

selectedLocation = [-1, -1]
globalGameState = GameState()
globalPgnMoves = getAllValidPgnMoves(globalGameState)

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

def displayPossibleMoves(gameState, buttons, pgnMoves, row=None, col=None):
    global globalGameState, globalPgnMoves, selectedLocation
    checkerTheButtons(buttons)
    for move in pgnMoves:
        if(move == '0-0' or move == '0-0-0'):
            if(move == '0-0'):
                rCol = 7
            else:
                rCol = 0
            if(gameState.isWhiteTurn):
                rRow = 7
            else:
                rRow = 0

            if(row == rRow and col == 4):
                selectedLocation = [rRow, 4]
                buttons[r][c]['bg'] = 'green'
                buttons[rRow][rCol]['bg'] = 'yellow'
            elif(row == rRow and col == rCol and selectedLocation[0] == rRow and selectedLocation[1] ==
                    4):
                selectedLocation = [-1, -1]
                globalGameState = pgnMoveToGameState(move, gameState)
                globalPgnMoves = getAllValidPgnMoves(globalGameState)
                checkerTheButtons(buttons)
                updateButtons(globalGameState.board, buttons)
                return

            continue

        d = parsePgnMove(move)
        start = [-1, -1]
        if(d['file'] != ''):
            start[1] = ChessPieces.notationToCol[d['file']]

        if(d['rank'] != ''):
            start[0] = ChessPieces.notationToRow[d['rank']]

        r, c = start[0], start[1]
        if(row != None and col != None):
            if( (r != row or c != col) and (selectedLocation == [-1, -1]) ):
                continue

        destination = convertToRowCol(d['destination'])
        rowEnd, colEnd = destination[0], destination[1]

        if(selectedLocation[0] == start[0] and selectedLocation[1] == start[1] and
                rowEnd == row and colEnd == col):
            selectedLocation = [-1, -1]
            theMove = move
            if(d['promote'] != ''):
                chooserDialog = PromotionChooserDialog(root)
                theMove = move[:-1] + chooserDialog.pieceLetter
                if(chooserDialog.canceled == True):
                    return
            globalGameState = pgnMoveToGameState(theMove, gameState)
            globalPgnMoves = getAllValidPgnMoves(globalGameState)
            updateButtons(globalGameState.board, buttons)
            return
        elif(row == r and col == c):
            buttons[r][c]['bg'] = 'green'
            if(isEmptyPiece(globalGameState.board[rowEnd][colEnd])):
                buttons[rowEnd][colEnd]['bg'] = 'blue'
            else:
                buttons[rowEnd][colEnd]['bg'] = 'red'

    if(isEmptyPiece(gameState.board[row][col])):
        selectedLocation = [-1, -1]
    elif(isWhitePiece(gameState.board[row][col]) == gameState.isWhiteTurn):
        selectedLocation = [row, col]
    else:
        selectedLocation = [-1, -1]

def buttonClick(row, col):
    displayPossibleMoves(globalGameState, buttons,
            globalPgnMoves, row, col)
    if(globalPgnMoves == []):
        print('game over')

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
