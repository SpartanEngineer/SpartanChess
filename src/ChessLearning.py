from ChessPieces import *
from sklearn import neural_network
import numpy as np

from PgnParser import parsePgnFile

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

    #parse pgn file
    pgnGames = parsePgnFile(pgnFilePath)

    #train the regressors
    trainRegressors(pgnGames, whiteRegressor, blackRegressor)

    return [whiteRegressor, blackRegressor]

def trainRegressors(pgnGames, whiteRegressor, blackRegressor):
    #TODO- implement this
    for game in pgnGames:
        pass
