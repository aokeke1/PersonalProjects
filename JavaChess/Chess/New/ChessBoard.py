import time,copy,random
import Pieces

class Board(object):
    def __init__(self):
        self.remainingWhitePieces = []
        self.remainingBlackPieces = []
        self.history = []
        self.layout = {}
        self.letters = "ABCDEFGH"
        self.numbers = "12345678"
    
        for i in xrange(8):
            #Make Black Pawns
            newPawn = Pieces.Pawn(self.letters[i]+"7", "Black", self)
            self.remainingBlackPieces.append(newPawn)
            self.layout[newPawn.getPosition()] = newPawn
        
        for i in xrange(8):
            #Make White Pawns
            newPawn = Pieces.Pawn(self.letters[i]+"2", "White", self)
            self.remainingWhitePieces.append(newPawn)
            self.layout[newPawn.getPosition()] = newPawn
            
        #Make Bishop, Knight, and Rook
        bishopPositions = ["C1","C8","F1","F8"]
        rookPositions = ['A1','A8','H1','H8']
        knightPositions = ['B1','B8','G1','G8']
        
        for i in xrange(4):
            if i%2==0:
                color="WHITE"
            else:
                color="BLACK"
            newBishop = Pieces.Bishop(bishopPositions[i],color, self)
            self.layout[bishopPositions[i]] = newBishop
            
            newRook = Pieces.Rook(rookPositions[i],color, self)
            self.layout[rookPositions[i]] = newRook

            newKnight = Pieces.Knight(knightPositions[i],color, self)
            self.layout[knightPositions[i]] = newKnight            
            
            if i%2==0:
                self.remainingWhitePieces.append(newBishop)
                self.remainingWhitePieces.append(newRook)
                self.remainingWhitePieces.append(newKnight)
            else:
                self.remainingBlackPieces.append(newBishop)
                self.remainingBlackPieces.append(newRook)
                self.remainingBlackPieces.append(newKnight)
            
        
        #Make Queens and Kings
        queenPositions = ["D1","D8"]
        kingPositions = ['E1','E8']
 
        for i in xrange(2):
            if i%2==0:
                color="WHITE"
            else:
                color="BLACK"
            newQueen = Pieces.Queen(queenPositions[i],color, self)
            self.layout[queenPositions[i]] = newQueen
            
            newKing = Pieces.King(kingPositions[i],color, self)
            self.layout[kingPositions[i]] = newKing     
            
            if i%2==0:
                self.remainingWhitePieces.append(newQueen)
                self.remainingWhitePieces.append(newKing)
            else:
                self.remainingBlackPieces.append(newQueen)
                self.remainingBlackPieces.append(newKing)
        
        #Fill remaining squars with 0
        for letter in self.letters:
            for number in self.numbers:
                if letter+number not in self.layout.keys():
                    self.layout[letter+number] = 0

    
    def __eq__(self, val):
        if type(val)==Board:
            return self.layout==val.getLayout()
        return False
    
    def __ne__(self,val):
        return not(self.__eq__(val))
        
    def loadBoard(self, gameDoc):
        pass
        
    def __str__(self):
        return str(self.layout)
    
    def resetBoard(self):
        self.__init__()

    def getPieceAt(self, position):
        """
        Given a position, returns the piece at that position
        """
        position = position.upper()
        assert len(position) == 2
        assert (position[0] in self.letters) and (position[1] in self.numbers)
        return self.layout[position]
        
    def getWhitePieces(self):
        return self.remainingWhitePieces
        
    def getBlackPieces(self):
        return self.remainingBlackPieces
        
    def getAllRemainingPieces(self):
        return self.remainingWhitePieces + self.remainingBlackPieces
        
    def getLayout(self):
        return self.layout
        
    def saveGame(self):
        pass