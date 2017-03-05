import tkinter
from tkinter import * 
from tkinter.font import Font

from ChessPieces import *

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

chessFont = Font(family='Tahoma', size=36, weight='bold')
labelFont = Font(family='Tahoma', size=24, weight='normal')

buttons = []
for r in range(8):
    row = []
    for c in range(8):
        button = Button(boardFrame, text='♔')
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
