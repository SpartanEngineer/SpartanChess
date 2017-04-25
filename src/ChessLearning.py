from ChessPieces import *
from sklearn import neural_network, linear_model
import numpy as np
import codecs
import time

from PgnParser import parsePgnFile, PgnGame, getNGamesInPgnFile

winValue = 100
drawValue = 0
lossValue = -100

def getFeatures(gameState):
    board = gameState.board
    features = []
    for p in range(12):
        for i in range(8):
            for j in range(8):
                if(board[i][j] == p):
                    features.append(1)
                else:
                    features.append(0)
    return np.array([features])

def evaluateGameState(gameState, regressor):
    features = getFeatures(gameState)
    return regressor.predict(features)

# alpha beta pruning algorithm
def evaluateGameStateAlphaBeta(gameState, depth, maximizingPlayer, alpha, beta, 
        blackRegressor, whiteRegressor):
    if(depth == 0):
        regressor = blackRegressor if(gameState.isWhiteTurn) else whiteRegressor
        return evaluateGameState(gameState, regressor)

    states = getAllValidGameStates(gameState)

    if(states == []):
        return winValue if(maximizingPlayer) else lossValue

    if(maximizingPlayer):
        value = -float("inf")
        for state in states:
            value = max(value, evaluateGameStateAlphaBeta(state, depth-1, False,
                alpha, beta, blackRegressor, whiteRegressor))
            alpha = max(alpha, value)
            if(beta <= alpha):
                break

        return value
    else:
        value = float("inf")
        for state in states:
            value = min(value, evaluateGameStateAlphaBeta(state, depth-1, True, alpha,
                beta, blackRegressor, whiteRegressor))
            beta = min(beta, value)
            if(beta <= alpha):
                break

        return value

    return None

def getBestPossibleGameState(gameState, regressor):
    states = getAllValidGameStates(gameState)
    evaluations = [evaluateGameState(state, regressor) for state in states]
    result = states[0]
    maxValue = evaluations[0]

    for i in range(1, len(states)):
        if(evaluations[i] > maxValue):
            result = states[i]
            maxValue = evaluations[i]

    result.isWhiteTurn = not gameState.isWhiteTurn
    return result

def getBestPossibleGameStateAlphaBeta(gameState, blackRegressor, whiteRegressor, depth):
    states = getAllValidGameStates(gameState)

    if(len(states) == 1):
        return states[0]

    evaluations = [evaluateGameStateAlphaBeta(state, depth, True, -float("inf"),
        float("inf"), blackRegressor, whiteRegressor) for state in states]
    result = states[0]
    maxValue = evaluations[0]

    for i in range(1, len(states)):
        if(evaluations[i] > maxValue):
            result = states[i]
            maxValue = evaluations[i]

    result.isWhiteTurn = not gameState.isWhiteTurn
    return result

def trainRegressorsFromScratch(pgnFilePath):
    #initial regressor setup/declaration
    #whiteRegressor = neural_network.MLPRegressor()
    #blackRegressor = neural_network.MLPRegressor()
    whiteRegressor = linear_model.SGDRegressor()
    blackRegressor = linear_model.SGDRegressor()
    features = getFeatures(GameState())
    target = np.array([0.5])
    whiteRegressor.partial_fit(features, target)
    blackRegressor.partial_fit(features, target)

    if(pgnFilePath != ''):
        #train the regressors
        trainRegressorsFromPgnFile(pgnFilePath, whiteRegressor, blackRegressor)

    return [whiteRegressor, blackRegressor]

def trainRegressor(pgnGame, whiteRegressor, blackRegressor):
    result = pgnGame.result #0=draw, 1=white win, 2=black win, 3=unknown
    if(result >= 3):
        return
    gs = GameState()
    whiteGameStates, blackGameStates = [], []
    for move in pgnGame.moves:
        nextGs = pgnMoveToGameState(move, gs)
        if(gs.isWhiteTurn):
            whiteGameStates.append(nextGs)
        else:
            blackGameStates.append(nextGs)
        gs = nextGs

    whiteFeatures, blackFeatures = [], []
    whiteEstimatedValues, blackEstimatedValues = [], []
    for state in whiteGameStates:
        whiteEstimatedValues.append(evaluateGameState(state,
            whiteRegressor))
        whiteFeatures.append(getFeatures(state))
    for state in blackGameStates:
        blackEstimatedValues.append(evaluateGameState(state,
            blackRegressor))
        blackFeatures.append(getFeatures(state))

    whiteActualValues, blackActualValues = [], []
    for i in range(len(whiteEstimatedValues)-1):
        whiteActualValues.append(whiteEstimatedValues[i+1])
    for i in range(len(blackEstimatedValues)-1):
        blackActualValues.append(blackEstimatedValues[i+1])

    if(result == 0):
        whiteActualValues.append(drawValue)
        blackActualValues.append(drawValue)
    elif(result == 1):
        whiteActualValues.append(winValue)
        blackActualValues.append(lossValue)
    elif(result == 2):
        whiteActualValues.append(lossValue)
        blackActualValues.append(winValue)

    for i in range(len(whiteActualValues)):
        if(i >= len(whiteFeatures)):
            break
        whiteRegressor.partial_fit(whiteFeatures[i],
                np.array([whiteActualValues[i]]).ravel())

    for i in range(len(blackActualValues)):
        if(i >= len(blackFeatures)):
            break
        blackRegressor.partial_fit(blackFeatures[i],
                np.array([blackActualValues[i]]).ravel())

def trainRegressorsFromGames(pgnGames, whiteRegressor, blackRegressor):
    for game in pgnGames:
        trainRegressor(game, whiteRegressor, blackRegressor)

#trains the regressors without having to load all the data into memory at once
def trainRegressorsFromPgnFile(pgnFilePath, whiteRegressor, blackRegressor):
    totalGames = getNGamesInPgnFile(pgnFilePath)
    startTime = time.time()
    print('totalGames:', totalGames)
    with codecs.open(pgnFilePath, 'r', encoding='utf-8', errors='ignore') as fileobject:
        lineNum, gameNum = 0, 0
        lines = []
        empties = 0
        for lineraw in fileobject:
            line = lineraw.strip()
            if(line == ''):
                empties += 1

            if(empties == 2):
                gameNum += 1
                try:
                    game = PgnGame(lines)
                    trainRegressor(game, whiteRegressor, blackRegressor)
                except:
                    print "caught exception"
                if(gameNum % 100 == 0):
                    #print('lines: ' + str(lineNum), 'games: ' + str(gameNum))
                    print(estimateTimeLeft(startTime, gameNum, totalGames))
                if(gameNum >= totalGames):
                    break
                empties = 0
                lines = []
            else:
                lines.append(line)

            lineNum += 1

    #millionbase has 2197188 games, 39860739 lines
    #~7 minutes to parse
    timeElapsed = time.time() - startTime
    print('lines: ' + str(lineNum), 'games: ' + str(gameNum))
    print('time to train regressors:', timeElapsed)
    print('time per game:', timeElapsed/gameNum)

def estimateTimeLeft(startTime, amountDone, amountTotal):
    percentDone = (amountDone / amountTotal) * 100
    amountLeft = amountTotal - amountDone
    timePer = (time.time() - startTime) / amountDone
    timeRemaining = timePer * amountLeft
    s = '%d/%d (%d%%) : ~%d seconds left' % (amountDone, amountTotal,
            percentDone, timeRemaining)
    return s
