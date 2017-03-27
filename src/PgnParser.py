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

def notationMoveToGameState(move, gameState):
    #pawn promotions have an = appended to the destination square: e8=Q
    newGameState = copy.deepcopy(gameState)
    isWhiteTurn = gameState.isWhiteTurn
    if(move == '0-0'):
        #TODO- implement kingside castle
        if(isWhiteTurn):
            newGameState.whiteHasCastled = True
        else:
            newGameState.blackHasCastled = True
    elif(move == '0-0-0'):
        #TODO- implement queenside castle
        if(isWhiteTurn):
            newGameState.whiteHasCastled = True
        else:
            newGameState.blackHasCastled = True
    else:
        #TODO- finish implementing
        destination = convertToRowCol(move[-2:])
        start = [0, 0]
        piece = 5 if(isWhiteTurn) else 11

        if(move[0] == 'N'):
            piece = 4 if(isWhiteTurn) else 10
        elif(move[0] == 'B'):
            piece = 3 if(isWhiteTurn) else 9
        elif(move[0] == 'K'):
            piece = 0 if(isWhiteTurn) else 6
        elif(move[0] == 'Q'):
            piece = 1 if(isWhiteTurn) else 7
        elif(move[0] == 'R'):
            piece = 2 if(isWhiteTurn) else 8

    newGameState.isWhiteTurn = not isWhiteTurn
    return newGameState

filePath = '../dataset/test.pgn'
games = parsePgnFile(filePath)
print("finished parsing pgn file")
