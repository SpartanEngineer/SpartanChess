import re, codecs, copy

#kingside castling == 0-0
#queenside castling == 0-0-0

#pawn promotions have an = appended to the destination square: e8=Q

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
            for s in line:
                if(s != ''):
                    self.moves.append(s.strip())
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
                return games
                empties = 0
                lines = []
            else:
                lines.append(line)
    
    return games

def notationMoveToGameState(move, gameState):
    newGameState = copy.deepcopy(gameState)
    #TODO- implement this
    return newGameState

filePath = '../dataset/test.pgn'
games = parsePgnFile(filePath)
print("finished parsing pgn file")
