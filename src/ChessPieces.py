from abc import ABC, abstractmethod
from enum import Enum
from copy import deepcopy

from PgnParser import pgnMoveToGameState

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

initialBlackPawnRow = 1
initialWhitePawnRow = 6
emptyNum = 12

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
        board[initialBlackPawnRow][i] = pieceTypeToNumConv[Pieces.bPawn]

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
        board[initialWhitePawnRow][i] = pieceTypeToNumConv[Pieces.wPawn]

    return board

#this class contains all the data needed to store a state of the game
class GameState():
    def __init__(self, cloning=False):
        if(cloning == False):
            self.board = makeBoard()
            self.whiteHasCastled = False
            self.blackHasCastled = False
            self.whiteQSideRookMoved = False
            self.whiteKSideRookMoved = False
            self.blackQSideRookMoved = False
            self.blackKSideRookMoved = False
            self.isWhiteTurn = True
            self.enPassantMove = None

    def deepcopy(self):
        gs = GameState(cloning=True)
        gs.board = []
        for i in range(8):
            gs.board.append(self.board[i][:])
        gs.whiteHasCastled = self.whiteHasCastled
        gs.blackHasCastled = self.blackHasCastled
        gs.whiteQSideRookMoved = self.whiteQSideRookMoved 
        gs.whiteKSideRookMoved = self.whiteKSideRookMoved 
        gs.blackQSideRookMoved = self.blackQSideRookMoved 
        gs.blackKSideRookMoved = self.blackKSideRookMoved 
        gs.isWhiteTurn = self.isWhiteTurn 
        if(self.enPassantMove != None):
            gs.enPassantMove = self.enPassantMove[:] 
        else:
            gs.enPassantMove = None
        return gs 

def isWhitePiece(pieceNum):
    return (pieceNum <= 5)

def isBlackPiece(pieceNum):
    return (pieceNum > 5 and pieceNum < 12)

def isEmptyPiece(pieceNum):
    return pieceNum == emptyNum 

def cloneGameStateWithPieceMoved(gameState, oldRow, oldCol, newRow, newCol):
    newState = gameState.deepcopy()
    newState.isWhiteTurn = not newState.isWhiteTurn
    newState.board[newRow][newCol] = newState.board[oldRow][oldCol]
    newState.board[oldRow][oldCol] = emptyNum
    return newState

#functions to help with generating the possible moves in a given gamestate

def getAllPossibleMoves(gameState):
    moves = []
    isWhiteTurn = gameState.isWhiteTurn
    board = gameState.board
    for r in range(8):
        for c in range(8):
            if(isEmptyPiece(board[r][c])):
                continue
            elif(isWhiteTurn == isWhitePiece(board[r][c])):
                x = []
                if(board[r][c] == 5 or board[r][c] == 11):
                    x = getPawnMoves(gameState, r, c)
                elif(board[r][c] == 0 or board[r][c] == 6):
                    x = getKingMoves(gameState, r, c)
                elif(board[r][c] == 1 or board[r][c] == 7):
                    x = getQueenMoves(gameState, r, c)
                elif(board[r][c] == 2 or board[r][c] == 8):
                    x = getRookMoves(gameState, r, c)
                elif(board[r][c] == 3 or board[r][c] == 9):
                    x = getBishopMoves(gameState, r, c)
                elif(board[r][c] == 4 or board[r][c] == 10):
                    x = getKnightMoves(gameState, r, c)

                for move in x:
                    moves.append(move)

    return moves

def getAllPossiblePgnMoves(gameState):
    moves = []
    isWhiteTurn = gameState.isWhiteTurn
    board = gameState.board
    for r in range(8):
        for c in range(8):
            if(isEmptyPiece(board[r][c])):
                continue
            elif(isWhiteTurn == isWhitePiece(board[r][c])):
                x = []
                if(board[r][c] == 5 or board[r][c] == 11):
                    x = getPawnPgnMoves(gameState, r, c)
                elif(board[r][c] == 0 or board[r][c] == 6):
                    x = getKingPgnMoves(gameState, r, c)
                    y = getCastlePgnMoves(gameState)
                    for z in y:
                        x.append(z)
                elif(board[r][c] == 1 or board[r][c] == 7):
                    x = getQueenPgnMoves(gameState, r, c)
                elif(board[r][c] == 2 or board[r][c] == 8):
                    x = getRookPgnMoves(gameState, r, c)
                elif(board[r][c] == 3 or board[r][c] == 9):
                    x = getBishopPgnMoves(gameState, r, c)
                elif(board[r][c] == 4 or board[r][c] == 10):
                    x = getKnightPgnMoves(gameState, r, c)

                for move in x:
                    moves.append(move)

    return moves

def getGameState(gameState, move):
    result = gameState.deepcopy()
    result.isWhiteTurn = not result.isWhiteTurn
    start, end = move
    result.board[end[0]][end[1]] = result.board[start[0]][start[1]]
    result.board[start[0]][start[1]] = 12 
    return result

def hasBothKings(gameState):
    hasWhiteKing = False
    hasBlackKing = False
    
    for i in range(8):
        for j in range(8):
            if(gameState.board[i][j] == 6):
                hasBlackKing = True
                if(hasBlackKing and hasWhiteKing):
                    return True
            elif(gameState.board[i][j] == 0):
                hasWhiteKing = True
                if(hasBlackKing and hasWhiteKing):
                    return True

    return hasWhiteKing and hasBlackKing

def isValidGameState(gameState):
    nextGameState = gameState.deepcopy()
    moves = getAllPossibleMoves(nextGameState)
    for move in moves:
        end = move[1]
        endPiece = nextGameState.board[end[0]][end[1]]
        if(endPiece == 0 or endPiece == 6):
            return False

    return True

def getAllValidMoves(gameState):
    allPossibleMoves = getAllPossibleMoves(gameState)
    validMoves = [allPossibleMoves[i] for i in range(len(allPossibleMoves))
            if(isValidGameState(getGameState(gameState, allPossibleMoves[i])))]
    return validMoves 

def getAllValidPgnMoves(gameState):
    allPossibleMoves = getAllPossiblePgnMoves(gameState)
    validMoves = []
    for move in allPossibleMoves:
        if(isValidGameState(pgnMoveToGameState(move, gameState))):
            validMoves.append(move)
    return validMoves 

def getAllValidGameStates(gameState):
    validGameStates = []
    for move in getAllPossiblePgnMoves(gameState):
        gs = pgnMoveToGameState(move, gameState)
        if(isValidGameState(gs)):
            validGameStates.append(gs)
    return validGameStates

def getGenericPgnMoves(gameState, moves, pieceStr):
    board = gameState.board
    result = []
    for move in moves:
        start = move[0]
        destination = move[1]
        pieceNum = board[destination[0]][destination[1]]

        capture = not isEmptyPiece(pieceNum)

        startStr = convertToNotation(start[0], start[1])
        destinationStr = convertToNotation(destination[0], destination[1])

        if(capture):
            pgnMove = pieceStr + startStr + 'x' + destinationStr
        else:
            pgnMove = pieceStr + startStr + destinationStr

        result.append(pgnMove)
    return result

def getPawnMoves(gameState, row, col):
    moves = []
    board = gameState.board
    isWhite = (board[row][col] == 5)
    isInitialLocation = (row == initialWhitePawnRow) if(isWhite) else (row ==
            initialBlackPawnRow)

    if(isWhite and row > 0):
        if(board[row-1][col] == emptyNum):
            moves.append( [(row, col), (row-1, col)] )
        if(isInitialLocation and row > 1 and board[row-1][col] == emptyNum and
                board[row-2][col] == emptyNum):
            moves.append( [(row, col), (row-2, col)] )
        if(col > 0 and isBlackPiece(board[row-1][col-1])):
            moves.append( [(row, col), (row-1, col-1)] )
        if(col < 7 and isBlackPiece(board[row-1][col+1])):
            moves.append( [(row, col), (row-1, col+1)] )

        #handle enpassant captures 
        if(row == 3):
            if(col > 0):
                if(board[3][col-1] == 11 and gameState.enPassantMove == (3, col-1)):
                    moves.append( [(row, col), (row-1, col-1)] )
            if(col < 7):
                if(board[3][col+1] == 11 and gameState.enPassantMove == (3, col+1)):
                    moves.append( [(row, col), (row-1, col+1)] )

    elif(not isWhite and row < 7):
        if(board[row+1][col] == emptyNum):
            moves.append( [(row, col), (row+1, col)] )
        if(isInitialLocation and row < 6 and board[row+1][col] == emptyNum and
                board[row+2][col] == emptyNum):
            moves.append( [(row, col), (row+2, col)] )
        if(col > 0 and isWhitePiece(board[row+1][col-1])):
            moves.append( [(row, col), (row+1, col-1)] )
        if(col < 7 and isWhitePiece(board[row+1][col+1])):
            moves.append( [(row, col), (row+1, col+1)] )

        #handle enpassant captures 
        if(row == 4):
            if(col > 0):
                if(board[4][col-1] == 5 and gameState.enPassantMove == (4, col-1)):
                    moves.append( [(row, col), (row+1, col-1)] )
            if(col < 7):
                if(board[4][col+1] == 5 and gameState.enPassantMove == (4, col+1)):
                    moves.append( [(row, col), (row+1, col+1)] )

    return moves

def getPawnPgnMoves(gameState, row, col):
    isWhiteTurn = gameState.isWhiteTurn
    board = gameState.board
    moves = []
    for move in getPawnMoves(gameState, row, col):
        start = move[0]
        destination = move[1]
        capture = destination[1] != start[1]

        if(isEmptyPiece(board[destination[0]][destination[1]]) and capture == True):
            enPassant = True
        else:
            enPassant = False

        if(destination[0] == 0 and isWhiteTurn):
            promote = True
        elif(destination[0] == 7 and not isWhiteTurn):
            promote = True
        else:
            promote = False

        startStr = convertToNotation(start[0], start[1])
        destinationStr = convertToNotation(destination[0], destination[1])

        if(capture):
            pgnMove = startStr + 'x' + destinationStr
        else:
            pgnMove = startStr + destinationStr

        if(promote):
            for c in ['Q', 'N', 'B', 'R']:
                x = pgnMove + '=' + c
                moves.append(x)
        else:
            moves.append(pgnMove)

    return moves

def getRookMoves(gameState, row, col):
    moves = []
    board = gameState.board
    isWhite = isWhitePiece(board[row][col]) 

    for r in range(row-1, -1, -1):
        if( (isWhite and isWhitePiece(board[r][col])) or (not isWhite and isBlackPiece(board[r][col]))):
            break
        moves.append( [(row, col), (r, col)] )
        if( (isWhite and isBlackPiece(board[r][col])) or (not isWhite and isWhitePiece(board[r][col]))):
            break

    for r in range(row+1, 8):
        if( (isWhite and isWhitePiece(board[r][col])) or (not isWhite and isBlackPiece(board[r][col]))):
            break
        moves.append( [(row, col), (r, col)] )
        if( (isWhite and isBlackPiece(board[r][col])) or (not isWhite and isWhitePiece(board[r][col]))):
            break

    for c in range(col-1, -1, -1):
        if( (isWhite and isWhitePiece(board[row][c])) or (not isWhite and isBlackPiece(board[row][c]))):
            break
        moves.append( [(row, col), (row, c)] )
        if( (isWhite and isBlackPiece(board[row][c])) or (not isWhite and isWhitePiece(board[row][c]))):
            break

    for c in range(col+1, 8):
        if( (isWhite and isWhitePiece(board[row][c])) or (not isWhite and isBlackPiece(board[row][c]))):
            break
        moves.append( [(row, col), (row, c)] )
        if( (isWhite and isBlackPiece(board[row][c])) or (not isWhite and isWhitePiece(board[row][c]))):
            break

    return moves

def getRookPgnMoves(gameState, row, col):
    moves = getRookMoves(gameState, row, col)
    return getGenericPgnMoves(gameState, moves, 'R')

def getKnightMoves(gameState, row, col):
    moves = []
    board = gameState.board
    isWhite = isWhitePiece(board[row][col]) 

    spots = []
    spots.append((row+1, col-2))
    spots.append((row+1, col+2))
    spots.append((row-1, col-2))
    spots.append((row-1, col+2))
    spots.append((row+2, col-1))
    spots.append((row+2, col+1))
    spots.append((row-2, col-1))
    spots.append((row-2, col+1))

    for (r, c) in spots:
        if(r < 0 or r > 7 or c < 0 or c > 7):
            continue
        if(isEmptyPiece(board[r][c]) or isWhite != isWhitePiece(board[r][c])):
            moves.append( [(row, col), (r, c)] )

    return moves

def getKnightPgnMoves(gameState, row, col):
    moves = getKnightMoves(gameState, row, col)
    return getGenericPgnMoves(gameState, moves, 'N')

def getKingMoves(gameState, row, col):
    moves = []
    board = gameState.board
    isWhite = isWhitePiece(board[row][col]) 

    spots = []
    spots.append((row+1, col+1))
    spots.append((row+1, col-1))
    spots.append((row+1, col))
    spots.append((row, col+1))
    spots.append((row, col-1))
    spots.append((row-1, col+1))
    spots.append((row-1, col-1))
    spots.append((row-1, col))

    for (r, c) in spots:
        if(r < 0 or r > 7 or c < 0 or c > 7):
            continue
        if(isEmptyPiece(board[r][c]) or isWhite != isWhitePiece(board[r][c])):
            moves.append( [(row, col), (r, c)] )

    return moves

def getKingPgnMoves(gameState, row, col):
    moves = getKingMoves(gameState, row, col)
    return getGenericPgnMoves(gameState, moves, 'K')

def getBishopMoves(gameState, row, col):
    moves = []
    board = gameState.board
    isWhite = isWhitePiece(board[row][col]) 

    r, c = row+1, col+1
    while(r >= 0 and r < 8 and c >= 0 and c < 8):
        if(not isEmptyPiece(board[r][c])):
            if(isWhite != isWhitePiece(board[r][c])):
                moves.append( [(row, col), (r, c)] )
            break
        else:
            moves.append( [(row, col), (r, c)] )
        r += 1
        c += 1

    r, c = row-1, col+1
    while(r >= 0 and r < 8 and c >= 0 and c < 8):
        if(not isEmptyPiece(board[r][c])):
            if(isWhite != isWhitePiece(board[r][c])):
                moves.append( [(row, col), (r, c)] )
            break
        else:
            moves.append( [(row, col), (r, c)] )
        r -= 1
        c += 1

    r, c = row+1, col-1
    while(r >= 0 and r < 8 and c >= 0 and c < 8):
        if(not isEmptyPiece(board[r][c])):
            if(isWhite != isWhitePiece(board[r][c])):
                moves.append( [(row, col), (r, c)] )
            break
        else:
            moves.append( [(row, col), (r, c)] )
        r += 1
        c -= 1

    r, c = row-1, col-1
    while(r >= 0 and r < 8 and c >= 0 and c < 8):
        if(not isEmptyPiece(board[r][c])):
            if(isWhite != isWhitePiece(board[r][c])):
                moves.append( [(row, col), (r, c)] )
            break
        else:
            moves.append( [(row, col), (r, c)] )
        r -= 1
        c -= 1

    return moves

def getBishopPgnMoves(gameState, row, col):
    moves = getBishopMoves(gameState, row, col)
    return getGenericPgnMoves(gameState, moves, 'B')

def getQueenMoves(gameState, row, col):
    moves = []

    bishopMoves = getBishopMoves(gameState, row, col)
    for move in bishopMoves:
        moves.append(move)

    rookMoves = getRookMoves(gameState, row, col)
    for move in rookMoves:
        moves.append(move)

    return moves

def getQueenPgnMoves(gameState, row, col):
    moves = getQueenMoves(gameState, row, col)
    return getGenericPgnMoves(gameState, moves, 'Q')

def getEnemyMoves(gameState):
    gs = gameState.deepcopy()
    gs.isWhiteTurn = not gameState.isWhiteTurn
    return getAllValidMoves(gs)

def getCastlePgnMoves(gameState):
    isWhiteTurn = gameState.isWhiteTurn
    moves = []
    if(isWhiteTurn and gameState.whiteHasCastled):
        return moves
    elif(not isWhiteTurn and gameState.blackHasCastled):
        return moves
    elif(isWhiteTurn and gameState.whiteQSideRookMoved and
            gameState.whiteKSideRookMoved):
        return moves
    elif(not isWhiteTurn and gameState.blackQSideRookMoved and
            gameState.blackKSideRookMoved):
        return moves

    board = gameState.board
    enemyMoves = []

    if(isWhiteTurn):
        if(not gameState.whiteQSideRookMoved):
            #check for queenside castle
            if(isEmptyPiece(board[7][1]) and isEmptyPiece(board[7][2]) and
                    isEmptyPiece(board[7][3])):
                attacked = False
                if(enemyMoves == []):
                    enemyMoves = getEnemyMoves(gameState)
                for move in enemyMoves:
                    if(move[1][0] == 7 and move[1][1] >= 1 and move[1][1] <= 4):
                        attacked = True
                        break

                if(attacked == False):
                    moves.append('O-O-O')

        if(not gameState.whiteKSideRookMoved):
            #check for kingside castle
            if(isEmptyPiece(board[7][5]) and isEmptyPiece(board[7][6])):
                attacked = False
                if(enemyMoves == []):
                    enemyMoves = getEnemyMoves(gameState)
                for move in enemyMoves:
                    if(move[1][0] == 7 and move[1][1] >= 4 and move[1][1] <= 6):
                        attacked = True
                        break

                if(attacked == False):
                    moves.append('O-O')

    else:
        if(not gameState.blackQSideRookMoved):
            #check for queenside castle
            if(isEmptyPiece(board[0][1]) and isEmptyPiece(board[0][2]) and
                    isEmptyPiece(board[0][3])):
                attacked = False
                if(enemyMoves == []):
                    enemyMoves = getEnemyMoves(gameState)
                for move in enemyMoves:
                    if(move[1][0] == 0 and move[1][1] >= 1 and move[1][1] <= 4):
                        attacked = True
                        break

                if(attacked == False):
                    moves.append('O-O-O')
        if(not gameState.blackKSideRookMoved):
            #check for kingside castle
            if(isEmptyPiece(board[0][5]) and isEmptyPiece(board[0][6])):
                attacked = False
                if(enemyMoves == []):
                    enemyMoves = getEnemyMoves(gameState)
                for move in enemyMoves:
                    if(move[1][0] == 0 and move[1][1] >= 4 and move[1][1] <= 6):
                        attacked = True
                        break

                if(attacked == False):
                    moves.append('O-O')

    return moves
