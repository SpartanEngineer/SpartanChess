from ChessPieces import *
from sklearn import neural_network
import numpy as np

from PgnParser import parsePgnFile

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
    #TODO- implement this
    return regressor.predict(features)

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

def trainRegressorsFromScratch(pgnFilePath):
    #initial regressor setup/declaration
    whiteRegressor = neural_network.MLPRegressor()
    blackRegressor = neural_network.MLPRegressor()
    features = getFeatures(GameState())
    target = np.array([0.5])
    whiteRegressor.partial_fit(features, target)
    blackRegressor.partial_fit(features, target)

    if(pgnFilePath != ''):
        #parse pgn file
        pgnGames = parsePgnFile(pgnFilePath)

        #train the regressors
        trainRegressors(pgnGames, whiteRegressor, blackRegressor)

    return [whiteRegressor, blackRegressor]

def trainRegressors(pgnGames, whiteRegressor, blackRegressor):
    for game in pgnGames:
        result = game.result #0=draw, 1=white win, 2=black win, 3=unknown
        if(result == '*'):
            continue
        gs = GameState()
        whiteGameStates, blackGameStates = [], []
        for move in game.moves:
            nextGs = pgnMoveToGameState(move, gs)
            if(gs.isWhiteTurn):
                whiteGameStates.append(nextGs)
            else:
                blackGameStates.append(nextGs)
            gs = nextGs

        #update values here
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
            whiteRegressor.partial_fit(whiteFeatures[i],
                    np.array([whiteActualValues[i]]).ravel())

        for i in range(len(blackActualValues)):
            blackRegressor.partial_fit(blackFeatures[i],
                    np.array([blackActualValues[i]]).ravel())
