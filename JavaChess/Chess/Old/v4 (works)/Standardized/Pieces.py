import time,copy,random

class Piece(object):
    def __init__(self, position, color, board):
    #makes a piece in a given position (string) with a given color (string white or black)
    #on a board (board)
        position.upper()
        if len(position)==2 and (position[0] in "ABCDEFGH" and position[1] in "12345678") and\
           (color == "White" or color == "Black"):
            self.position = position
            self.color = color
            self.name = self.getName()
            self.letters = "ABCDEFGH"
            self.board = board
            self.hasMoved = False
            self.validMoves = []
            self.lastPosition = ""
        else:
            print "This is not a valid position."
    def getPosition(self):
        return self.position
    def setPosition(self, position):
        if type(position)== tuple and position[0] in range(8) and position[1] in range(8):
            r = 8-position[0]
            i = self.letters[position[1]]
            newposition = i+str(r)
            if self.name == "Pawn":
                self.lastPosition = self.position
            self.position = newposition
            self.hasMoved = True
            
        else:
            self.position = "X"
            self.validMoves = []
            
    def getColor(self):
        return self.color
    def getName(self):
        return ""
    def __eq__(self, val):
        if type(val) == str:
            if self.getName() == val or val == "Piece":
                return True
        elif str(self) == str(val):
            return True
        return False
    def __ne__(self, val):
        return not(self.__eq__(val))
    def updateValidMoves(self):
        self.validMoves=[]
    def getValidMoves(self):
        return self.validMoves
    def isValidMove(self, position):
        if position in self.validMoves:
            return True
##    def Move(self, position):
##        if self.isValid(position)
##            self.setPosition(self, position)
    def getSymbol(self):
        return ""
    def getMoveStatus(self):
        return self.hasMoved
    def willBeCheck(self, end):
        start = self.position
        board2 = copy.deepcopy(self.board)
        for p in board2.getAllRemainingPieces():
            if p == "King" and p.getColor() == self.color:
                king2 = p
                break
        if king2.getColor() == "Black":
            board2.blackMove2(start, end)
        elif king2.getColor() == "White":
            board2.whiteMove2(start, end)
        return king2.inCheck() 
    def __str__(self):
        return "{"+self.color+" "+self.name+" at "+self.position+"}"
    
class King(Piece):
    def getName(self):
        return "King"
    def getSymbol(self):
        if self.color == "White":
            return "K"
        if self.color == "Black":
            return "k"
    def updateValidMoves(self):
        self.validMoves=[]
        pos = squareToCoord(self.position)
        pos1 = (pos[0]+1,pos[1]+1)
        pos2 = (pos[0]+1,pos[1])
        pos3 = (pos[0]+1,pos[1]-1)
        pos4 = (pos[0],pos[1]+1)
        pos5 = (pos[0],pos[1]-1)
        pos6 = (pos[0]-1,pos[1]+1)
        pos7 = (pos[0]-1,pos[1])
        pos8 = (pos[0]-1,pos[1]-1)
        possible = [pos1,pos2,pos3,pos4,pos5,pos6,pos7,pos8]
        possible2 = copy.deepcopy(possible)
        for p in possible2:
##            print p
            # makes sure the move is on the board 
            if p[0]<0 or p[0]>=8 or p[1]<0 or p[1]>=8:
##                print p, "removed. off board"
                possible.remove(p)
        possible2 = copy.deepcopy(possible)
        for p in possible2:
##            print coordToSquare(p)
            piece = self.board.getPieceAt(coordToSquare(p))
            if piece =="Piece":
                if piece.getColor() == self.color:
##                    print coordToSquare(p), "removed. friendly piece in way"
                    possible.remove(p)
                #For future use creating a strategy
                elif piece.getColor() != self.color:
                    continue
            else:
                continue
        for p in possible:
            self.validMoves.append(coordToSquare(p))
        #Make sure the move won't put me in check
        validMoves2 = copy.deepcopy(self.validMoves)
        for place in self.validMoves:
##            print place
            if self.willBeCheck(place):
##                print place, "removed. will be check"
                validMoves2.remove(place)
        self.validMoves = copy.deepcopy(validMoves2)
        if not(self.inCheck()):
            if self.color == "White":
                if self.canQueenSideCastle():
                    self.validMoves.append("C1")
                if self.canKingSideCastle():
                    self.validMoves.append("G1")
            if self.color == "Black":
                if self.canQueenSideCastle():
                    self.validMoves.append("C8")
                if self.canKingSideCastle():
                    self.validMoves.append("G8")
    def inCheck(self):
        if self.color == "White":
            threats = self.board.checkRemainingBlackPieces()
        if self.color == "Black":
            threats = self.board.checkRemainingWhitePieces()
        for piece in threats:
            piece.updateValidMoves2()
            if self.position in piece.getValidMoves():
##                print "Check!"
##                print piece
                return True
        return False
    def updateValidMoves2(self):
        self.validMoves=[]
        pos = squareToCoord(self.position)
        pos1 = (pos[0]+1,pos[1]+1)
        pos2 = (pos[0]+1,pos[1])
        pos3 = (pos[0]+1,pos[1]-1)
        pos4 = (pos[0],pos[1]+1)
        pos5 = (pos[0],pos[1]-1)
        pos6 = (pos[0]-1,pos[1]+1)
        pos7 = (pos[0]-1,pos[1])
        pos8 = (pos[0]-1,pos[1]-1)
        possible = [pos1,pos2,pos3,pos4,pos5,pos6,pos7,pos8]
        possible2 = copy.deepcopy(possible)
        for p in possible:
##            print p
            # makes sure the move is on the board 
            if p[0]<0 or p[0]>=8 or p[1]<0 or p[1]>=8:
##                print p, "removed. off board2"
                possible2.remove(p)
        possible = copy.deepcopy(possible2)
        for p in possible:
##            print coordToSquare(p)
            piece = self.board.getPieceAt(coordToSquare(p))
            if piece =="Piece":
                if piece.getColor() == self.color:
##                    print coordToSquare(p), "removed. friendly piece in way2"
                    possible2.remove(p)
                #For future use creating a strategy
                elif piece.getColor() != self.color:
                    continue
            else:
                continue
        possible = copy.deepcopy(possible2)
        for p in possible:
            self.validMoves.append(coordToSquare(p))
        if self.color == "White":
            if self.canQueenSideCastle():
                self.validMoves.append("C1")
            if self.canKingSideCastle():
                self.validMoves.append("G1")
        if self.color == "Black":
            if self.canQueenSideCastle():
                self.validMoves.append("C8")
            if self.canKingSideCastle():
                self.validMoves.append("G8")
    def canQueenSideCastle(self):
##        if self.inCheck():
##            return False
        if self.hasMoved:
            return False
        if self.color == "White":
            rook = self.board.getPieceAt("A1")
            if rook != "Rook":
                return False
            if rook.getMoveStatus() or rook.getColor()!=self.color:
                return False
            threats = self.board.checkRemainingBlackPieces()
            positionsToCheck = ["D1","C1"]
            blocked = "B1"
        if self.color == "Black":
            rook = self.board.getPieceAt("A8")
            if rook != "Rook":
                return False
            if rook.getMoveStatus() or rook.getColor()!=self.color:
                return False
            threats = self.board.checkRemainingBlackPieces()
            positionsToCheck = ["D8","C8"]
            blocked = "B8"
        if self.board.getPieceAt(blocked) == "Piece":
            return False
        for spot in positionsToCheck:
            if self.board.getPieceAt(spot) == "Piece":
                return False
        for piece in threats:
            piece.updateValidMoves2()
            for spot in positionsToCheck:
                if spot in piece.getValidMoves():
                    return False
        return True
    def canKingSideCastle(self):
##        if self.inCheck():
##            return False
        if self.hasMoved:
            return False
        if self.color == "White":
            rook = self.board.getPieceAt("H1")
            if rook != "Rook":
                return False
            if rook.getMoveStatus() or rook.getColor()!=self.color:
                return False
            threats = self.board.checkRemainingBlackPieces()
            positionsToCheck = ["F1","G1"]
        if self.color == "Black":
            rook = self.board.getPieceAt("H8")
            if rook != "Rook":
                return False
            if rook.getMoveStatus() or rook.getColor()!=self.color:
                return False
            threats = self.board.checkRemainingBlackPieces()
            positionsToCheck = ["F8","G8"]
        for spot in positionsToCheck:
            if self.board.getPieceAt(spot) == "Piece":
                return False
        for piece in threats:
            piece.updateValidMoves2()
            for spot in positionsToCheck:
                if spot in piece.getValidMoves():
                    return False
        return True
    
class Queen(Piece):
    def getName(self):
        return "Queen"
    def getSymbol(self):
        if self.color == "White":
            return "Q"
        if self.color == "Black":
            return "q"
    def updateValidMoves(self):
        self.validMoves=[]
        pos = squareToCoord(self.position)
        for i in range(1,8):
            if pos[0]-i<0:
                break
            elif pos[0]-i>=0:
                pos2 = (pos[0]-i,pos[1])
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[0]+i>=8:
                break
            elif pos[0]+i<8:
                pos2 = (pos[0]+i,pos[1])
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[1]-i<0:
                break
            elif pos[1]-i>=0:
                pos2 = (pos[0],pos[1]-i)
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[1]+i>=8:
                break
            elif pos[1]+i<8:
                pos2 = (pos[0],pos[1]+i)
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[0]-i<0 or pos[1]-i<0:
                break
            elif pos[0]-i>=0 and pos[1]-i>=0:
                pos2 = (pos[0]-i,pos[1]-i)
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[0]+i>=8 or pos[1]+i>=8:
                break
            elif pos[0]+i<8 and pos[1]+i<8:
                pos2 = (pos[0]+i,pos[1]+i)
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[0]-i<0 or pos[1]+i>=8:
                break
            elif pos[0]-i>=0 and pos[1]+i<8:
                pos2 = (pos[0]-i,pos[1]+i)
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[0]+i>=8 or pos[1]-i<0:
                break
            elif pos[0]+i<8 and pos[1]-i>=0:
                pos2 = (pos[0]+i,pos[1]-i)
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        #Make sure the move won't put me in check
        validMoves2 = copy.deepcopy(self.validMoves)
        for place in self.validMoves:
            if self.willBeCheck(place):
                validMoves2.remove(place)
        self.validMoves = copy.deepcopy(validMoves2)
    def updateValidMoves2(self):
        self.validMoves=[]
        pos = squareToCoord(self.position)
        for i in range(1,8):
            if pos[0]-i<0:
                break
            elif pos[0]-i>=0:
                pos2 = (pos[0]-i,pos[1])
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[0]+i>=8:
                break
            elif pos[0]+i<8:
                pos2 = (pos[0]+i,pos[1])
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[1]-i<0:
                break
            elif pos[1]-i>=0:
                pos2 = (pos[0],pos[1]-i)
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[1]+i>=8:
                break
            elif pos[1]+i<8:
                pos2 = (pos[0],pos[1]+i)
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[0]-i<0 or pos[1]-i<0:
                break
            elif pos[0]-i>=0 and pos[1]-i>=0:
                pos2 = (pos[0]-i,pos[1]-i)
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[0]+i>=8 or pos[1]+i>=8:
                break
            elif pos[0]+i<8 and pos[1]+i<8:
                pos2 = (pos[0]+i,pos[1]+i)
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[0]-i<0 or pos[1]+i>=8:
                break
            elif pos[0]-i>=0 and pos[1]+i<8:
                pos2 = (pos[0]-i,pos[1]+i)
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[0]+i>=8 or pos[1]-i<0:
                break
            elif pos[0]+i<8 and pos[1]-i>=0:
                pos2 = (pos[0]+i,pos[1]-i)
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        
class Bishop(Piece):
    def getName(self):
        return "Bishop"
    def getSymbol(self):
        if self.color == "White":
            return "B"
        if self.color == "Black":
            return "b"
    def updateValidMoves(self):
        self.validMoves=[]
        pos = squareToCoord(self.position)
        for i in range(1,8):
            if pos[0]-i<0 or pos[1]-i<0:
                break
            elif pos[0]-i>=0 and pos[1]-i>=0:
                pos2 = (pos[0]-i,pos[1]-i)
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[0]+i>=8 or pos[1]+i>=8:
                break
            elif pos[0]+i<8 and pos[1]+i<8:
                pos2 = (pos[0]+i,pos[1]+i)
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[0]-i<0 or pos[1]+i>=8:
                break
            elif pos[0]-i>=0 and pos[1]+i<8:
                pos2 = (pos[0]-i,pos[1]+i)
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[0]+i>=8 or pos[1]-i<0:
                break
            elif pos[0]+i<8 and pos[1]-i>=0:
                pos2 = (pos[0]+i,pos[1]-i)
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        #Make sure the move won't put me in check
        validMoves2 = copy.deepcopy(self.validMoves)
        for place in self.validMoves:
            if self.willBeCheck(place):
                validMoves2.remove(place)
        self.validMoves = copy.deepcopy(validMoves2)
    def updateValidMoves2(self):
        self.validMoves=[]
        pos = squareToCoord(self.position)
        for i in range(1,8):
            if pos[0]-i<0 or pos[1]-i<0:
                break
            elif pos[0]-i>=0 and pos[1]-i>=0:
                pos2 = (pos[0]-i,pos[1]-i)
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[0]+i>=8 or pos[1]+i>=8:
                break
            elif pos[0]+i<8 and pos[1]+i<8:
                pos2 = (pos[0]+i,pos[1]+i)
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[0]-i<0 or pos[1]+i>=8:
                break
            elif pos[0]-i>=0 and pos[1]+i<8:
                pos2 = (pos[0]-i,pos[1]+i)
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[0]+i>=8 or pos[1]-i<0:
                break
            elif pos[0]+i<8 and pos[1]-i>=0:
                pos2 = (pos[0]+i,pos[1]-i)
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)

        
class Knight(Piece):
    def getName(self):
        return "Knight"
    def getSymbol(self):
        if self.color == "White":
            return "N"
        if self.color == "Black":
            return "n"
    def updateValidMoves(self):
        self.validMoves=[]
        pos = squareToCoord(self.position)
        pos1 = (pos[0]+2,pos[1]+1)
        pos2 = (pos[0]+2,pos[1]-1)
        pos3 = (pos[0]+1,pos[1]+2)
        pos4 = (pos[0]-1,pos[1]+2)
        pos5 = (pos[0]-2,pos[1]+1)
        pos6 = (pos[0]-2,pos[1]-1)
        pos7 = (pos[0]+1,pos[1]-2)
        pos8 = (pos[0]-1,pos[1]-2)
        possible = [pos1,pos2,pos3,pos4,pos5,pos6,pos7,pos8]
        possible2 = copy.deepcopy(possible)
        for p in possible:
            if p[0]<0 or p[0]>=8 or p[1]<0 or p[1]>=8:
                possible2.remove(p)
        possible = copy.deepcopy(possible2)
        for p in possible:
            piece = self.board.getPieceAt(coordToSquare(p))
            if piece =="Piece":
                if piece.getColor() == self.color:
                    possible2.remove(p)
                #For future use creating a strategy
                elif piece.getColor() != self.color:
                    continue
            else:
                continue
        possible = copy.deepcopy(possible2)
        for p in possible:
            self.validMoves.append(coordToSquare(p))
        #Make sure the move won't put me in check
        validMoves2 = copy.deepcopy(self.validMoves)
        for place in self.validMoves:
            if self.willBeCheck(place):
                validMoves2.remove(place)
        self.validMoves = copy.deepcopy(validMoves2)
    def updateValidMoves2(self):
        self.validMoves=[]
        pos = squareToCoord(self.position)
        pos1 = (pos[0]+2,pos[1]+1)
        pos2 = (pos[0]+2,pos[1]-1)
        pos3 = (pos[0]+1,pos[1]+2)
        pos4 = (pos[0]-1,pos[1]+2)
        pos5 = (pos[0]-2,pos[1]+1)
        pos6 = (pos[0]-2,pos[1]-1)
        pos7 = (pos[0]+1,pos[1]-2)
        pos8 = (pos[0]-1,pos[1]-2)
        possible = [pos1,pos2,pos3,pos4,pos5,pos6,pos7,pos8]
        possible2 = copy.deepcopy(possible)
        for p in possible:
            if p[0]<0 or p[0]>=8 or p[1]<0 or p[1]>=8:
                possible2.remove(p)
        possible = copy.deepcopy(possible2)
        for p in possible:
            piece = self.board.getPieceAt(coordToSquare(p))
            if piece =="Piece":
                if piece.getColor() == self.color:
                    possible2.remove(p)
                #For future use creating a strategy
                elif piece.getColor() != self.color:
                    continue
            else:
                continue
        possible = copy.deepcopy(possible2)
        for p in possible:
            self.validMoves.append(coordToSquare(p))
        
class Rook(Piece):
    def getName(self):
        return "Rook"
    def getSymbol(self):
        if self.color == "White":
            return "R"
        if self.color == "Black":
            return "r"
    def updateValidMoves(self):
        self.validMoves=[]
        pos = (8-int(self.position[1]),"ABCDEFGH".find(self.position[0]))
        for i in range(1,8):
            if pos[0]-i<0:
                break
            elif pos[0]-i>=0:
                pos2 = (pos[0]-i,pos[1])
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[0]+i>=8:
                break
            elif pos[0]+i<8:
                pos2 = (pos[0]+i,pos[1])
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[1]-i<0:
                break
            elif pos[1]-i>=0:
                pos2 = (pos[0],pos[1]-i)
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[1]+i>=8:
                break
            elif pos[1]+i<8:
                pos2 = (pos[0],pos[1]+i)
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        #Make sure the move won't put me in check
        validMoves2 = copy.deepcopy(self.validMoves)
        for place in self.validMoves:
            if self.willBeCheck(place):
                validMoves2.remove(place)
        self.validMoves = copy.deepcopy(validMoves2)
    def updateValidMoves2(self):
        self.validMoves=[]
        pos = (8-int(self.position[1]),"ABCDEFGH".find(self.position[0]))
        for i in range(1,8):
            if pos[0]-i<0:
                break
            elif pos[0]-i>=0:
                pos2 = (pos[0]-i,pos[1])
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[0]+i>=8:
                break
            elif pos[0]+i<8:
                pos2 = (pos[0]+i,pos[1])
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[1]-i<0:
                break
            elif pos[1]-i>=0:
                pos2 = (pos[0],pos[1]-i)
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        for i in range(1,8):
            if pos[1]+i>=8:
                break
            elif pos[1]+i<8:
                pos2 = (pos[0],pos[1]+i)
                square2 = coordToSquare(pos2)
                piece = self.board.getPieceAt(square2)
                if piece == "Piece":
                    if piece.getColor()==self.getColor():
                        break
                    else:
                        self.validMoves.append(square2)
                        break
                else:
                    self.validMoves.append(square2)
        
class Pawn(Piece):
    def getName(self):
        return "Pawn"
    def getSymbol(self):
        if self.color == "White":
            return "P"
        if self.color == "Black":
            return "p"
    def getLastPosition(self):
        return self.lastPosition
    def updateValidMoves(self):
        if self.position[1]=="8" or self.position[1]=="1":
            coord = squareToCoord(self.position)
            square = self.position
            board = self.board
            color = self.color
            x=0
            while not(x in ["1","2","3","4"]):
                x = raw_input("Choose which piece you want:\n1.Knight \n2.Bishop \n3.Rook \n4.Queen \nYour choice:")
            x = int(x)
            if x == 1:
                newPiece = Knight(square, color, board)
            if x == 2:
                newPiece = Bishop(square, color, board)
            if x == 3:
                newPiece = Rook(square, color, board)
            if x == 4:
                newPiece = Queen(square, color, board)
            board.rows[coord[0]].setRowPos(coord[1],newPiece)
            board.cols[coord[1]].setColPos(coord[0],newPiece)
            board.pieces.append(newPiece)
            self.position = "X"
            board.pieces.remove(self)
            if color =="Black":
                board.remainingBlackPieces.append(newPiece)
                board.remainingBlackPieces.remove(self)
            elif color == "White":
                board.remainingWhitePieces.append(newPiece)
                board.remainingWhitePieces.remove(self)
            return
                
        self.validMoves=[]
        #White Pawn Moves
        if self.color == "White":
##            print self
##            print self.position
            
            coord = squareToCoord(self.position)
            
##            print coord
##            pause = raw_input("pause1")
            coord1 = (coord[0]-1,coord[1])
            coord2 = (coord[0]-1,coord[1]-1)
            coord3 = (coord[0]-1,coord[1]+1)
            #squares to left and right
            coordleft = (coord[0],coord[1]-1)
            coordright = (coord[0],coord[1]+1)
            if coord2[0] in range(8) and coord2[1] in range(8):
                piece2 = self.board.getPieceAt(coordToSquare(coord2))
                piece21 = self.board.getPieceAt(coordToSquare(coordleft))
                if piece2 == "Piece":
                    if piece2.getColor() != self.color:
                        self.validMoves.append(coordToSquare(coord2))
                #en passant
                elif piece21 == "Piece" and self.position[1] == "5":
                    if piece21.getColor() != self.color and piece21.getLastPosition()[1]=="7":
                        self.validMoves.append(coordToSquare(coord2))                        
            if coord3[0] in range(8) and coord3[1] in range(8):
                piece3 = self.board.getPieceAt(coordToSquare(coord3))
                piece31 = self.board.getPieceAt(coordToSquare(coordright))
                if piece3 == "Piece":
                    if piece3.getColor() != self.color:
                        self.validMoves.append(coordToSquare(coord3))
                #en passant
                elif piece31 == "Piece" and self.position[1] == "5":
                    if piece31.getColor() != self.color and piece31.getLastPosition()[1]=="7":
                        self.validMoves.append(coordToSquare(coord3))
            if coord1[0] in range(8) and coord1[1] in range(8):
                piece1 = self.board.getPieceAt(coordToSquare(coord1))
                if piece1 != "Piece":
                    self.validMoves.append(coordToSquare(coord1))
            if not(self.hasMoved):
                coord4 = (coord[0]-2,coord[1])
                piece4 = self.board.getPieceAt(coordToSquare(coord4))
                if piece1 != "Piece" and piece4 != "Piece":
                    self.validMoves.append(coordToSquare(coord4))
        #Black Pawn Moves
        if self.color == "Black":
##            print self
##            print self.position
            
            coord = squareToCoord(self.position)
            
##            print coord
##            pause = raw_input("pause2")
            coord1 = (coord[0]+1,coord[1])
            coord2 = (coord[0]+1,coord[1]-1)
            coord3 = (coord[0]+1,coord[1]+1)
            #squares to left and right
            coordleft = (coord[0],coord[1]-1)
            coordright = (coord[0],coord[1]+1)
            if coord2[0] in range(8) and coord2[1] in range(8):
                piece2 = self.board.getPieceAt(coordToSquare(coord2))
                piece21 = self.board.getPieceAt(coordToSquare(coordleft))
                if piece2 == "Piece":
                    if piece2.getColor() != self.color:
                        self.validMoves.append(coordToSquare(coord2))
                #en passant
                elif piece21 == "Piece" and self.position[1] == "4":
                    if piece21.getColor() != self.color and piece21.getLastPosition()[1]=="2":
                        self.validMoves.append(coordToSquare(coord2))
            if coord3[0] in range(8) and coord3[1] in range(8):
                piece3 = self.board.getPieceAt(coordToSquare(coord3))
                piece31 = self.board.getPieceAt(coordToSquare(coordright))
                if piece3 == "Piece":
                    if piece3.getColor() != self.color:
                        self.validMoves.append(coordToSquare(coord3))
                #en passant
                elif piece31 == "Piece" and self.position[1] == "4":
                    if piece31.getColor() != self.color and piece31.getLastPosition()[1]=="2":
                        self.validMoves.append(coordToSquare(coord3))
            if coord1[0] in range(8) and coord1[1] in range(8):
                piece1 = self.board.getPieceAt(coordToSquare(coord1))
                if piece1 != "Piece":
                    self.validMoves.append(coordToSquare(coord1))
            if not(self.hasMoved):
                coord4 = (coord[0]+2,coord[1])
                piece4 = self.board.getPieceAt(coordToSquare(coord4))
                if piece1 != "Piece" and piece4 != "Piece":
                    self.validMoves.append(coordToSquare(coord4))
        #Make sure the move won't put me in check
        validMoves2 = copy.deepcopy(self.validMoves)
        for place in self.validMoves:
            if self.willBeCheck(place):
                validMoves2.remove(place)
        self.validMoves = copy.deepcopy(validMoves2)
    def updateValidMoves2(self):
        if self.position[1]=="8" or self.position[1]=="1":
            coord = squareToCoord(self.position)
            square = self.position
            board = self.board
            color = self.color
            x=0
            while not(x in ["1","2","3","4"]):
                x = raw_input("Choose which piece you want:\n1.Knight \n2.Bishop \n3.Rook \n4.Queen \nYour choice:")
            x = int(x)
            if x == 1:
                newPiece = Knight(square, color, board)
            if x == 2:
                newPiece = Bishop(square, color, board)
            if x == 3:
                newPiece = Rook(square, color, board)
            if x == 4:
                newPiece = Queen(square, color, board)
            board.rows[coord[0]].setRowPos(coord[1],newPiece)
            board.cols[coord[1]].setColPos(coord[0],newPiece)
            board.pieces.append(newPiece)
            self.position = "X"
            board.pieces.remove(self)
            if color =="Black":
                board.remainingBlackPieces.append(newPiece)
                board.remainingBlackPieces.remove(self)
            elif color == "White":
                board.remainingWhitePieces.append(newPiece)
                board.remainingWhitePieces.remove(self)
            return
                
        self.validMoves=[]
        #White Pawn Moves
        if self.color == "White":
##            print self
##            print self.position
            
            coord = squareToCoord(self.position)
            
##            print coord
##            pause = raw_input("pause1")
            coord1 = (coord[0]-1,coord[1])
            coord2 = (coord[0]-1,coord[1]-1)
            coord3 = (coord[0]-1,coord[1]+1)
            #squares to left and right
            coordleft = (coord[0],coord[1]-1)
            coordright = (coord[0],coord[1]+1)
            if coord2[0] in range(8) and coord2[1] in range(8):
                piece2 = self.board.getPieceAt(coordToSquare(coord2))
                piece21 = self.board.getPieceAt(coordToSquare(coordleft))
                if piece2 == "Piece":
                    if piece2.getColor() != self.color:
                        self.validMoves.append(coordToSquare(coord2))
                #en passant
                elif piece21 == "Piece" and self.position[1] == "5":
                    if piece21.getColor() != self.color and piece21.getLastPosition()[1]=="7":
                        self.validMoves.append(coordToSquare(coord2))                        
            if coord3[0] in range(8) and coord3[1] in range(8):
                piece3 = self.board.getPieceAt(coordToSquare(coord3))
                piece31 = self.board.getPieceAt(coordToSquare(coordright))
                if piece3 == "Piece":
                    if piece3.getColor() != self.color:
                        self.validMoves.append(coordToSquare(coord3))
                #en passant
                elif piece31 == "Piece" and self.position[1] == "5":
                    if piece31.getColor() != self.color and piece31.getLastPosition()[1]=="7":
                        self.validMoves.append(coordToSquare(coord3))                                
            if coord1[0] in range(8) and coord1[1] in range(8):
                piece1 = self.board.getPieceAt(coordToSquare(coord1))
                if piece1 != "Piece":
                    self.validMoves.append(coordToSquare(coord1))
            if not(self.hasMoved):
                coord4 = (coord[0]-2,coord[1])
                piece4 = self.board.getPieceAt(coordToSquare(coord4))
                if piece1 != "Piece" and piece4 != "Piece":
                    self.validMoves.append(coordToSquare(coord4))
        #Black Pawn Moves
        if self.color == "Black":
##            print self
##            print self.position
            
            coord = squareToCoord(self.position)
            
##            print coord
##            pause = raw_input("pause2")
            coord1 = (coord[0]+1,coord[1])
            coord2 = (coord[0]+1,coord[1]-1)
            coord3 = (coord[0]+1,coord[1]+1)
            #squares to left and right
            coordleft = (coord[0],coord[1]-1)
            coordright = (coord[0],coord[1]+1)
            if coord2[0] in range(8) and coord2[1] in range(8):
                piece2 = self.board.getPieceAt(coordToSquare(coord2))
                piece21 = self.board.getPieceAt(coordToSquare(coordleft))
                if piece2 == "Piece":
                    if piece2.getColor() != self.color:
                        self.validMoves.append(coordToSquare(coord2))
                #en passant
                elif piece21 == "Piece" and self.position[1] == "4":
                    if piece21.getColor() != self.color and piece21.getLastPosition()[1]=="2":
                        self.validMoves.append(coordToSquare(coord2))
            if coord3[0] in range(8) and coord3[1] in range(8):
                piece3 = self.board.getPieceAt(coordToSquare(coord3))
                piece31 = self.board.getPieceAt(coordToSquare(coordright))
                if piece3 == "Piece":
                    if piece3.getColor() != self.color:
                        self.validMoves.append(coordToSquare(coord3))
                #en passant
                elif piece31 == "Piece" and self.position[1] == "4":
                    if piece31.getColor() != self.color and piece31.getLastPosition()[1]=="2":
                        self.validMoves.append(coordToSquare(coord3))
            if coord1[0] in range(8) and coord1[1] in range(8):
                piece1 = self.board.getPieceAt(coordToSquare(coord1))
                if piece1 != "Piece":
                    self.validMoves.append(coordToSquare(coord1))
            if not(self.hasMoved):
                coord4 = (coord[0]+2,coord[1])
                piece4 = self.board.getPieceAt(coordToSquare(coord4))
                if piece1 != "Piece" and piece4 != "Piece":
                    self.validMoves.append(coordToSquare(coord4))
                        
                
    
def coordToSquare(coord):
    #Converts coordinate to move format with letter
    if coord[0] in range(8) and coord[1] in range(8):
        row = 8-coord[0]
        col = "ABCDEFGH"[coord[1]]
        return col+str(row)
    print coord
    print "This isn't a valid coord"
def squareToCoord(square):
    #Converts move format with letter to coordinate
    if square[0] in "ABCDEFGH" and square[1] in "12345678":
        return (8-int(square[1]),"ABCDEFGH".find(square[0]))
    print square
    print "This isn't a valid square"
