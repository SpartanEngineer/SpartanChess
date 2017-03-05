from abc import ABC, abstractmethod
from enum import Enum

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

class ChessPiece(ABC):
    @abstractmethod
    def __init__(self, row, col, initialSpot, isWhite, pieceType, nType):
        self.row = row
        self.col = col
        self.pieceType = pieceType
        self.nType = nType
        self.isWhite = isWhite
        self.initialSpot = initialSpot

    @abstractmethod
    def getMoves(self, board):
        pass

class Pawn(ChessPiece):
    def __init__(self, row, col, isWhite, initialSpot):
        pieceType = Pieces.wPawn if(isWhite) else Pieces.bPawn
        nType = pieceTypeToNumConv[pieceType]
        super(Pawn, self).__init__(row, col, initialSpot, isWhite, pieceType, nType)

    def getMoves(self, board):
        #TODO- implement this
        moves = []
        return moves

class King(ChessPiece):
    def __init__(self, row, col, isWhite, initialSpot):
        pieceType = Pieces.wKing if(isWhite) else Pieces.bKing
        nType = pieceTypeToNumConv[pieceType]
        super(King, self).__init__(row, col, initialSpot, isWhite, pieceType, nType)

    def getMoves(self, board):
        #TODO- implement this
        moves = []
        return moves

class Queen(ChessPiece):
    def __init__(self, row, col, isWhite, initialSpot):
        pieceType = Pieces.wQueen if(isWhite) else Pieces.bQueen
        nType = pieceTypeToNumConv[pieceType]
        super(Queen, self).__init__(row, col, initialSpot, isWhite, pieceType, nType)

    def getMoves(self, board):
        #TODO- implement this
        moves = []
        return moves

class Rook(ChessPiece):
    def __init__(self, row, col, isWhite, initialSpot):
        pieceType = Pieces.wRook if(isWhite) else Pieces.bRook
        nType = pieceTypeToNumConv[pieceType]
        super(Rook, self).__init__(row, col, initialSpot, isWhite, pieceType, nType)

    def getMoves(self, board):
        #TODO- implement this
        moves = []
        return moves

class Knight(ChessPiece):
    def __init__(self, row, col, isWhite, initialSpot):
        pieceType = Pieces.wKnight if(isWhite) else Pieces.bKnight
        nType = pieceTypeToNumConv[pieceType]
        super(Knight, self).__init__(row, col, initialSpot, isWhite, pieceType, nType)

    def getMoves(self, board):
        #TODO- implement this
        moves = []
        return moves

class Bishop(ChessPiece):
    def __init__(self, row, col, isWhite, initialSpot):
        pieceType = Pieces.wBishop if(isWhite) else Pieces.bBishop
        nType = pieceTypeToNumConv[pieceType]
        super(Bishop, self).__init__(row, col, initialSpot, isWhite, pieceType, nType)

    def getMoves(self, board):
        #TODO- implement this
        moves = []
        return moves
