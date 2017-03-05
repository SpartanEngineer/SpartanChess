from abc import ABC, abstractmethod
from enum import Enum

#conversion code + piece definition code

class Pieces(Enum):
    wKing = 0
    wQueen = 1
    wRook = 2
    wBishop = 3
    wKnight = 4
    wPawn = 5
    bKing = 6
    bQueen = 7
    bRook = 8
    bBishop = 9
    bKnight = 10
    bPawn = 11
    empty = 12

pieceTypeToNumConv = {Pieces.wKing:0,
                        Pieces.wQueen:1,
                        Pieces.wRook:2,
                        Pieces.wBishop:3,
                        Pieces.wKnight:4,
                        Pieces.wPawn:5,
                        Pieces.bKing:6,
                        Pieces.bQueen:7,
                        Pieces.bRook:8,
                        Pieces.bBishop:9,
                        Pieces.bKnight:10,
                        Pieces.bPawn:11,
                        Pieces.empty:12}

unicodeConv = {0 : '♔',
               1 : '♕',
               2 : '♖',
               3 : '♗',
               4 : '♘',
               5 : '♙',
               6 : '♚',
               7 : '♛',
               8 : '♜',
               9 : '♝',
               10 : '♞',
               11 : '♟',
               12 : ' '}

#convert between chess notation and our row, col format
notationToRow = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
notationToCol = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
rowToNotation = {0:"8", 1:"7", 2:"6", 3:"5", 4:"4", 5:"3", 6:"2", 7:"1"}
colToNotation = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h"}

def convertToNotation(row, col):
    return colToNotation[col] + rowToNotation[row]

def convertToRowCol(notation):
    return (notationToRow[notation[1]], notationToCol[notation[0]])

#code to make the initial board
def makeBoard():
    board = [[pieceTypeToNumConv[Pieces.empty] for x in range(8)] for y in range(8)]

    #setting up initial black positions
    board[0][0] = pieceTypeToNumConv[Pieces.bRook]
    board[0][1] = pieceTypeToNumConv[Pieces.bKnight]
    board[0][2] = pieceTypeToNumConv[Pieces.bBishop]
    board[0][3] = pieceTypeToNumConv[Pieces.bQueen]
    board[0][4] = pieceTypeToNumConv[Pieces.bKing]
    board[0][5] = pieceTypeToNumConv[Pieces.bBishop]
    board[0][6] = pieceTypeToNumConv[Pieces.bKnight]
    board[0][7] = pieceTypeToNumConv[Pieces.bRook]
    for i in range(8):
        board[1][i] = pieceTypeToNumConv[Pieces.bPawn]

    #setting up inital white positions
    board[7][0] = pieceTypeToNumConv[Pieces.wRook]
    board[7][1] = pieceTypeToNumConv[Pieces.wKnight]
    board[7][2] = pieceTypeToNumConv[Pieces.wBishop]
    board[7][3] = pieceTypeToNumConv[Pieces.wQueen]
    board[7][4] = pieceTypeToNumConv[Pieces.wKing]
    board[7][5] = pieceTypeToNumConv[Pieces.wBishop] 
    board[7][6] = pieceTypeToNumConv[Pieces.wKnight] 
    board[7][7] = pieceTypeToNumConv[Pieces.wRook]
    for i in range(8):
        board[6][i] = pieceTypeToNumConv[Pieces.wPawn]

    return board

#this class contains all the data needed to store a state of the game
class GameState():
    def __init__(self):
        self.board = makeBoard()
        self.hasCastled = False
        self.isWhiteTurn = True
