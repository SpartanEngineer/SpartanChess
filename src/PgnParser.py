import re, codecs, copy

from ChessPieces import *

class PgnGame:
    def __init__(self, data):
        self.eventName = ""
        self.date = ""
        self.blackPlayer = ""
        self.whitePlayer = ""
        self.site = ""
        self.result = 0
        self.moves = []
        self.parse(data)

    def parse(self, data):
        n = len(data)
        lineNum = 0
        while(lineNum < n and data[lineNum][0] == '['):
            line = data[lineNum]
            if('"' in line):
                content = line.split('"')[1] #get the content in between quotes
                if(line.startswith('[Event')):
                    self.eventName = content
                elif(line.startswith('[Date')):
                    self.date = content 
                elif(line.startswith('[Black')):
                    self.blackPlayer = content
                elif(line.startswith('[White')):
                    self.whitePlayer = content
                elif(line.startswith('[Site')):
                    self.site = content
                elif(line.startswith('[Result')):
                    resultConv = {'1/2-1/2':0, '1-0':1, '0-1':2, '*':3}
                    self.result = resultConv[content]
            lineNum += 1
            if(lineNum < n and data[lineNum] == ''):
                lineNum += 1

        while(lineNum < n):
            line = re.compile("[0-9]+\.").split(data[lineNum])
            split2 = "".join(line).split(' ')
            for s in split2:
                if(s != ''):
                    self.moves.append(s)
            lineNum += 1

        self.moves.pop() #get rid of the game result (which is the last item in the split)

    def __str__(self):
        d = {}
        d['Event'] = self.eventName
        d['Date'] = self.date
        d['Black'] = self.blackPlayer
        d['White'] = self.whitePlayer
        d['Site'] = self.site
        d['Result'] = self.result
        d['Moves'] = self.moves
        return str(d) 

def parsePgnFile(filePath):
    games = []
    with codecs.open(filePath, 'r', encoding='utf-8', errors='ignore') as fileobject:
        lines = []
        empties = 0
        for lineraw in fileobject:
            line = lineraw.strip()
            if(line == ''):
                empties += 1

            if(empties == 2):
                game = PgnGame(lines)
                games.append(game)
                empties = 0
                lines = []
            else:
                lines.append(line)
    
    return games

def parsePgnMove(move):
    d = {}
    d['destination'] = ''
    d['rank'] = ''
    d['file'] = ''
    d['piece'] = 'P'
    d['capture'] = False
    d['promote'] = ''
    d['check'] = False
    d['checkMate'] = False

    n = len(move)
    i = 0
    while(i < n):
        c = move[i]
        if(i == 0 and c.isupper()):
            d['piece'] = c
        elif(c == 'x'):
            d['capture'] = True
        elif(i + 1 < n and c.islower() and move[i+1].isnumeric()):
            if(d['destination'] != ''):
                d['file'] = d['destination'][0]
                d['rank'] = d['destination'][1]
            d['destination'] = c + move[i+1]
            i += 1
        elif(i + 1 < n and c == '=' and move[i+1].isupper()):
            d['promote'] = move[i+1]
            i += 1
        elif(c.islower()):
            d['file'] = c
        elif(c.isnumeric()):
            d['rank'] = c
        elif(c == '+'):
            d['check'] = True
        elif(c == '#'):
            d['checkMate'] = True
        elif(c == ';'):
            break
        elif(c == '{'):
            while(c != '}'):
                i += 1
                if(i >= n):
                    break
                c = a[i]

        i += 1

    return d

def getPieceNumberFromLetter(pieceLetter, isWhite):
    piece = 12
    if(pieceLetter == 'P'):
        piece = 5 if(isWhite) else 11
    if(pieceLetter == 'N'):
        piece = 4 if(isWhite) else 10
    elif(pieceLetter == 'B'):
        piece = 3 if(isWhite) else 9
    elif(pieceLetter == 'K'):
        piece = 0 if(isWhite) else 6
    elif(pieceLetter == 'Q'):
        piece = 1 if(isWhite) else 7
    elif(pieceLetter == 'R'):
        piece = 2 if(isWhite) else 8

    return piece

def pgnMoveToGameState(move, gameState):
    #pawn promotions have an = appended to the destination square: e8=Q
    board = gameState.board
    newGameState = copy.deepcopy(gameState)
    isWhiteTurn = gameState.isWhiteTurn
    if(move == '0-0'):
        if(isWhiteTurn):
            newGameState.whiteHasCastled = True
            newGameState.board[7][6] = 0
            newGameState.board[7][5] = 2
        else:
            newGameState.blackHasCastled = True
            newGameState.board[0][6] = 6
            newGameState.board[0][5] = 8
    elif(move == '0-0-0'):
        if(isWhiteTurn):
            newGameState.whiteHasCastled = True
            newGameState.board[7][2] = 0
            newGameState.board[7][3] = 2
        else:
            newGameState.blackHasCastled = True
            newGameState.board[0][2] = 6
            newGameState.board[0][3] = 8
    else:
        d = parsePgnMove(move)

        start = (-1, -1)
        destination = convertToRowCol(d['destination'])
        pieceLetter = d['piece']
        piece = getPieceNumberFromLetter(pieceLetter, isWhiteTurn)

        if(d['file'] != ''):
            start[1] = notationToCol[d['file']]

        if(d['rank'] != ''):
            start[0] = notationToRow[d['rank']]

        if(start[0] == -1 or start[1] == -1):
            possible = []
            for i in range(8):
                for j in range(8):
                    if(board[i][j] == piece):
                        possible.append((i, j))

            if(len(possible) == 1):
                start = possible[0]
            else:
                for candidate in possible:
                    row, col = candidate
                    possibleMoves = []
                    done = False

                    if(pieceLetter == 'P'):
                        possibleMoves = getPawnMoves(gameState, row, col)
                    elif(pieceLetter == 'R'):
                        possibleMoves == getRookMoves(gameState, row, col)
                    elif(pieceLetter == 'N'):
                        possibleMoves = getKnightMoves(gameState, row, col)
                    elif(pieceLetter == 'B'):
                        possibleMoves = getBishopMoves(gameState, row, col)
                    elif(pieceLetter == 'K'):
                        possibleMoves = getKingMoves(gameState, row, col)
                    elif(pieceLetter == 'Q'):
                        possibleMoves = getQueenMoves(gameState, row, col)

                    for move in possibleMoves:
                        if(move[1] == destination):
                            start = candidate
                            done = True
                            break
                    
                    if(done):
                        break

        newGameState.board[start[0]][start[1]] = emptyNum

        if(d['promote'] != ''):
            promotedPiece = getPieceNumberFromLetter(d['promote'])
            newGameState.board[destination[0]][destination[1]] = promotedPiece 
        else:
            newGameState.board[destination[0]][destination[1]] = piece

    newGameState.isWhiteTurn = not isWhiteTurn
    return newGameState

filePath = '../dataset/test.pgn'
games = parsePgnFile(filePath)
print("finished parsing pgn file")
