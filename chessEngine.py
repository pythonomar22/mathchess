class GameState():
    def __init__(self):
        import numpy as np
        pieceList = ['bR', 'bN', 'bB', 'bR', 'bN', 'bB', 'bK', 'bQ', 'wR', 'wN', 'wB', 'wR', 'wN', 'wB', 'wK', 'wQ', '--']
        pieceArray = np.random.choice(pieceList, 16, replace = False)
        self.board = np.reshape(pieceArray, (4,4))
        self.moveLog = []
        self.moveFunctions = {'R' : self.getRookMoves, 'B' : self.getBishopMoves, 'Q' : self.getQueenMoves,
                            'K' : self.getKingMoves, 'N' : self.getKnightMoves}

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w') or (turn == 'b'):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((2, 1), (-2, -1), (-2, 1), (2, -1), (1, 2), (-1, -2), (-1, 2), (1, -2))
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 4 and 0 <= endCol < 4:
                endPiece = self.board[endRow][endCol]
                if endPiece == '--':
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        kingMoves = ((1, 1), (-1, -1), (0, 1), (1, 0), (1, -1), (-1, 1), (-1, 0), (0, -1))
        for m in kingMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 4 and 0 <= endCol < 4:
                endPiece = self.board[endRow][endCol]
                if endPiece == '--':
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        for d in directions:
            for i in range(1, 4):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 4 and 0 <= endCol < 4:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    else:
                        break
                else:
                    break

    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (1, 0), (0, 1), (0, -1))
        for d in directions:
            for i in range (1, 4):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 4 and 0 <= endCol < 4:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    else:
                        break
                else:
                    break


class Move():

    #keys : value
    ranksToRows = {"1" : 3, "2" : 2, "3": 1, "4" : 0}
    rowsToRanks = {v : k for k, v in ranksToRows.items()}
    filesToCols = {"a" : 0, "b" : 1, "c" : 2, "d" : 3}
    colsToFiles = {v : k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
