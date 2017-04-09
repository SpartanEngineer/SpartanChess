import tkinter
from tkinter import * 
from tkinter.font import Font
from functools import partial

from ChessPieces import *
from ChessLearning import *
from PgnParser import *
from PromotionChooserDialog import *

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

def updateStatusLabel(statusLabel, gameState):
    if(globalGameState.isWhiteTurn):
        statusLabel['text'] = 'white turn'
    else:
        statusLabel['text'] = 'black turn'


def displayPossibleMoves(gameState, buttons, pgnMoves, row=None, col=None):
    global globalGameState, globalPgnMoves, selectedLocation
    for move in pgnMoves:
        if(move == 'O-O' or move == 'O-O-O'):
            if(move == 'O-O'):
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
                return True

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
                    return False
            globalGameState = pgnMoveToGameState(theMove, gameState)
            globalPgnMoves = getAllValidPgnMoves(globalGameState)
            return True
        elif(row == r and col == c):
            buttons[r][c]['bg'] = 'green'
            if(isEmptyPiece(globalGameState.board[rowEnd][colEnd])):
                buttons[rowEnd][colEnd]['bg'] = 'blue'
            else:
                buttons[rowEnd][colEnd]['bg'] = 'red'

            #handle pawn captures (even if they are enpassant)
            if(d['piece'] == 'P' and c != colEnd):
                buttons[rowEnd][colEnd]['bg'] = 'red'

    if(isEmptyPiece(gameState.board[row][col])):
        selectedLocation = [-1, -1]
    elif(isWhitePiece(gameState.board[row][col]) == gameState.isWhiteTurn):
        selectedLocation = [row, col]
    else:
        selectedLocation = [-1, -1]

    return False

def boardButtonClick(row, col):
    global movesDisplayed, globalPgnMoves
    movesDisplayed = False
    checkerTheButtons(buttons)
    moveMade = displayPossibleMoves(globalGameState, buttons,
            globalPgnMoves, row, col)

    if(moveMade):
        checkerTheButtons(buttons)
        updateButtons(globalGameState.board, buttons)
        updateStatusLabel(statusLabel, globalGameState)

    if(globalPgnMoves == []):
        if(globalGameState.isWhiteTurn):
            s = 'game over black wins!!!'
        else:
            s = 'game over white wins!!!'
        statusLabel['text'] = s
        tkinter.messagebox.showinfo(s, s)

    if(moveMade and globalPgnMoves != []):
        makeAiMove(globalGameState)
        checkerTheButtons(buttons)
        updateButtons(globalGameState.board, buttons)
        updateStatusLabel(statusLabel, globalGameState)
        globalPgnMoves = getAllValidPgnMoves(globalGameState)

def makeAiMove(gameState):
    regressor = regressors[0] if(gameState.isWhiteTurn) else regressors[1]
    nextGameState = getBestPossibleGameState(gameState, regressor)
    global globalGameState
    globalGameState = nextGameState

def startNewGame(whichSide):
    global selectedLocation, globalGameState, globalPgnMoves, movesDisplayed
    selectedLocation = [-1, -1]
    globalGameState = GameState()
    movesDisplayed = False
    if(whichSide == 0):
        makeAiMove(globalGameState)
    globalPgnMoves = getAllValidPgnMoves(globalGameState)
    updateButtons(globalGameState.board, buttons)
    checkerTheButtons(buttons)
    updateStatusLabel(statusLabel, globalGameState)

def newGameClick():
    startNewGame(playAsWhich.get())

def displayMovesClick():
    global selectedLocation, movesDisplayed
    selectedLocation = [-1, -1]
    checkerTheButtons(buttons)
    if(movesDisplayed == False):
        movesDisplayed = True
        for r in range(8):
            for c in range(8):
                displayPossibleMoves(globalGameState, buttons, globalPgnMoves, row=r, col=c)
                selectedLocation = [-1, -1]
    else:
        movesDisplayed = False

filePath = '/home/dmoney/Desktop/programming/python_scratch/SpartanChess/dataset/test.pgn'
regressors = trainRegressorsFromScratch(filePath)

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
        button = Button(boardFrame, text='♔', command=partial(boardButtonClick, r, c))
        button.grid(row=r, column=c+1, sticky=N+S+E+W)
        button.configure(font=chessFont)
        row.append(button)

    colLabel = Label(boardFrame, text=rowToNotation[r], font=labelFont)
    colLabel.grid(row=r, column=0, sticky=N+S+E+W)
    rowLabel = Label(boardFrame, text=colToNotation[r], font=labelFont)
    rowLabel.grid(row=8, column=r+1, sticky=N+S+E+W)

    buttons.append(row)

for i in range(9):
    Grid.rowconfigure(boardFrame, i, weight=1)
    Grid.columnconfigure(boardFrame, i, weight=1)

optionsFrame = Frame(topLevelFrame)
optionsFrame.grid(row=0, column=1, sticky=N+S+E+W)

newGameButton = Button(optionsFrame, text="New Game?", command=newGameClick)
newGameButton.grid(row=0, column=0, sticky=N+S+E+W)

playAsWhich = IntVar() 
radio1 = Radiobutton(optionsFrame, text="Play as black?", variable=playAsWhich, value=0)
radio1.grid(row=1, column=0, sticky=N+S+E+W)
radio2 = Radiobutton(optionsFrame, text="Play as white?", variable=playAsWhich, value=1)
radio2.grid(row=2, column=0, sticky=N+S+E+W)
radio2.invoke()

displayMovesButton = Button(optionsFrame, text="Display moves", command=displayMovesClick)
displayMovesButton.grid(row=3, column=0, sticky=N+S+W+E)

statusLabel = Label(optionsFrame, text="click new game!")
statusLabel.grid(row=4, column=0, sticky=N+S+W+E)

for i in range(5):
    Grid.rowconfigure(optionsFrame, i, weight=1)
Grid.rowconfigure(optionsFrame, 5, weight=20)
Grid.columnconfigure(optionsFrame, 0, weight=1)

newGameClick()
root.mainloop()
