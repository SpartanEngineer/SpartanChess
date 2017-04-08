from ChessPieces import *
from sklearn import neural_network
import numpy as np

def getFeatures(gameState):
    board = gameState.board
    features = []
    for p in range(12):
        a = [[1 if(board[i][j] == p) else 0 for i in range(8)] for j in range(8)]
        for x in a:
            for y in x:
                features.append(y)
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

    return result

regressor = neural_network.MLPRegressor()
features = getFeatures(GameState())
target = np.array([0.5])
regressor.partial_fit(features, target)
