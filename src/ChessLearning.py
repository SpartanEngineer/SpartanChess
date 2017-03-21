def getFeatures(gameState):
    board = gameState.board
    features = []
    for p in range(12):
        a = [[1 if(board[i][j] == p) else 0 for i in range(8)] for j in range(8)]
        features.append(a)
    return features

def evaluateGameState(gameState, regressor):
    features = getFeatures(gameState)
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
