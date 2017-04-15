import re, codecs, copy

import ChessPieces

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
    newGameState.enPassantMove = None
    isWhiteTurn = gameState.isWhiteTurn
    if(move.startswith('O-O-O')):
        #queenside castle
        if(isWhiteTurn):
            newGameState.whiteHasCastled = True
            newGameState.board[7][2] = 0
            newGameState.board[7][3] = 2
            newGameState.board[7][4] = 12
            newGameState.board[7][0] = 12 
        else:
            newGameState.blackHasCastled = True
            newGameState.board[0][2] = 6
            newGameState.board[0][3] = 8
            newGameState.board[0][4] = 12
            newGameState.board[0][0] = 12
    elif(move.startswith('O-O')):
        if(isWhiteTurn):
            newGameState.whiteHasCastled = True
            newGameState.board[7][6] = 0
            newGameState.board[7][5] = 2
            newGameState.board[7][4] = 12
            newGameState.board[7][7] = 12 
        else:
            newGameState.blackHasCastled = True
            newGameState.board[0][6] = 6
            newGameState.board[0][5] = 8
            newGameState.board[0][4] = 12
            newGameState.board[0][7] = 12 
    else:
        d = parsePgnMove(move)

        start = [-1, -1]
        destination = ChessPieces.convertToRowCol(d['destination'])
        pieceLetter = d['piece']
        piece = getPieceNumberFromLetter(pieceLetter, isWhiteTurn)

        if(d['file'] != ''):
            start[1] = ChessPieces.notationToCol[d['file']]

        if(d['rank'] != ''):
            start[0] = ChessPieces.notationToRow[d['rank']]

        if(start[0] == -1 or start[1] == -1):
            possible = []
            for i in range(8):
                for j in range(8):
                    if(board[i][j] == piece):
                        if(start[0] == -1 and start[1] == -1):
                            possible.append((i, j))
                        elif(start[0] == -1 and start[1] == j):
                            possible.append((i, j))
                        elif(start[1] == -1 and start[0] == i):
                            possible.append((i, j))

            if(len(possible) == 1):
                start = possible[0]
            else:
                for candidate in possible:
                    row, col = candidate
                    possibleMoves = []
                    done = False

                    if(pieceLetter == 'P'):
                        possibleMoves = ChessPieces.getPawnMoves(gameState, row, col)
                    elif(pieceLetter == 'R'):
                        possibleMoves == ChessPieces.getRookMoves(gameState, row, col)
                    elif(pieceLetter == 'N'):
                        possibleMoves = ChessPieces.getKnightMoves(gameState, row, col)
                    elif(pieceLetter == 'B'):
                        possibleMoves = ChessPieces.getBishopMoves(gameState, row, col)
                    elif(pieceLetter == 'K'):
                        possibleMoves = ChessPieces.getKingMoves(gameState, row, col)
                    elif(pieceLetter == 'Q'):
                        possibleMoves = ChessPieces.getQueenMoves(gameState, row, col)

                    for move in possibleMoves:
                        if(move[1] == destination):
                            start = candidate
                            done = True
                            break

                    if(done):
                        break

        if(pieceLetter == 'P' and start[1] != destination[1] and
                newGameState.board[destination[0]][destination[1]] ==
                ChessPieces.emptyNum and gameState.enPassantMove != None):
            #handle en passant capture
            epMove = gameState.enPassantMove
            newGameState.board[epMove[0]][epMove[1]] = ChessPieces.emptyNum

        newGameState.board[start[0]][start[1]] = ChessPieces.emptyNum

        if(d['promote'] != ''):
            promotedPiece = getPieceNumberFromLetter(d['promote'], isWhiteTurn)
            newGameState.board[destination[0]][destination[1]] = promotedPiece 
        else:
            newGameState.board[destination[0]][destination[1]] = piece

        if(pieceLetter == 'R'):
            if(isWhiteTurn):
                if(start[0] == 7 and start[1] == 0):
                    newGameState.whiteQSideRookMoved = True
                elif(start[0] == 7 and start[1] == 7):
                    newGameState.whiteKSideRookMoved = True
            else:
                if(start[0] == 0 and start[1] == 0):
                    newGameState.blackQSideRookMoved = True
                elif(start[0] == 0 and start[1] == 7):
                    newGameState.blackKSideRookMoved = True
        elif(pieceLetter == 'K'):
            if(isWhiteTurn):
                newGameState.whiteHasCastled = True
            else:
                newGameState.blackHasCastled = True
        elif(pieceLetter == 'P'):
            if(abs(start[0] - destination[0]) == 2):
                newGameState.enPassantMove = (destination[0], destination[1])


    newGameState.isWhiteTurn = not isWhiteTurn
    return newGameState

#filePath = '../dataset/test.pgn'
#games = parsePgnFile(filePath)
#print("finished parsing pgn file")
