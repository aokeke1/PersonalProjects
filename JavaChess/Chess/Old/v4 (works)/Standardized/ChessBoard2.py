import Pieces
import time,copy,random


class Row:
    
    def __init__(self, pos):
        self.position = pos
        self.row = ['x','x','x','x','x','x','x','x']
        self.possiblePieces = ["King","Queen","Bishop","Knight","Rook","Pawn"]

    def setRowPos(self, pos, piece): 
        if pos in range(0,8) and (piece in self.possiblePieces):
            self.row[pos] = piece
        elif pos in range(0,8):
            self.row[pos] = 'x'
        else:
            print "Error: this is not a vald move"

    def getRowPos(self, pos):
        if pos in range(0,8):
            return self.row[pos]

    def __str__(self):
        s = ''
        for i in self.row:
            if i == "x":
                s+=i
                s+=" "
            else:
                s += i.getSymbol()
                s += " "
        return s[:-1]


    
class Column:
    
    def __init__(self, pos):
        self.position = pos
        self.col = ['x','x','x','x','x','x','x','x']
        self.possiblePieces = ["King","Queen","Bishop","Knight","Rook","Pawn"]

    def setColPos(self, pos, piece):
        if pos in range(0,8) and (piece in self.possiblePieces):
            self.col[pos] = piece.getSymbol()
        elif pos in range(0,8):
            self.col[pos] = 'x'
        else:
            print "Error: this is not a vald move"

    def getColPos(self, pos):
        if pos in range(0,8):
            return self.col[pos]

    def __str__(self):
        s = ''
        for i in self.col:
            if i == "x":
                s+=i
                s+="\n"
            else:
                s += i.getSymbol()
                s += "\n"
        return s[:-1]




class Board:
    def __init__(self):
        self.possible = "ABCDEFGH"
        self.rows = []
        self.cols = []
        self.pieces = []
        self.ended = False
##        self.record = []
##        self.undone = []
        for i in range(8):
            self.rows.append(Row(i))
            self.cols.append(Column(i))
        self.remainingWhitePieces = []
        self.remainingBlackPieces = []
        for i in range(8):
            #Black Pawns
            newPawn = Pieces.Pawn(str(self.possible[i])+"7", "Black", self)
            self.rows[1].setRowPos(i,newPawn)
            self.cols[i].setColPos(1,newPawn)
            self.pieces.append(newPawn)
            self.remainingBlackPieces.append(newPawn)
        for i in range(8):
            #White Pawns
            newPawn = Pieces.Pawn(str(self.possible[i])+"2", "White", self)
            self.rows[6].setRowPos(i,newPawn)
            self.cols[i].setColPos(6,newPawn)
            self.pieces.append(newPawn)
            self.remainingWhitePieces.append(newPawn)
        #Rooks
        newRook = Pieces.Rook("A8","Black", self)
        self.rows[0].setRowPos(0,newRook)
        self.cols[0].setColPos(0,newRook)
        self.pieces.append(newRook)
        self.remainingBlackPieces.append(newRook)
        newRook = Pieces.Rook("H8","Black", self)
        self.rows[0].setRowPos(7,newRook)
        self.cols[7].setColPos(0,newRook)
        self.pieces.append(newRook)
        self.remainingBlackPieces.append(newRook)
        newRook = Pieces.Rook("A1","White", self)
        self.rows[7].setRowPos(0,newRook)
        self.cols[0].setColPos(7,newRook)
        self.pieces.append(newRook)
        self.remainingWhitePieces.append(newRook)
        newRook = Pieces.Rook("H1","White", self)
        self.rows[7].setRowPos(7,newRook)
        self.cols[7].setColPos(7,newRook)
        self.pieces.append(newRook)
        self.remainingWhitePieces.append(newRook)
        #Knights
        newKnight = Pieces.Knight("B8","Black", self)
        self.rows[0].setRowPos(1,newKnight)
        self.cols[1].setColPos(0,newKnight)
        self.pieces.append(newKnight)
        self.remainingBlackPieces.append(newKnight)
        newKnight = Pieces.Knight("G8","Black", self)
        self.rows[0].setRowPos(6,newKnight)
        self.cols[6].setColPos(0,newKnight)
        self.pieces.append(newKnight)
        self.remainingBlackPieces.append(newKnight)
        newKnight = Pieces.Knight("B1","White", self)
        self.rows[7].setRowPos(1,newKnight)
        self.cols[1].setColPos(7,newKnight)
        self.pieces.append(newKnight)
        self.remainingWhitePieces.append(newKnight)
        newKnight = Pieces.Knight("G1","White", self)
        self.rows[7].setRowPos(6,newKnight)
        self.cols[6].setColPos(7,newKnight)
        self.pieces.append(newKnight)
        self.remainingWhitePieces.append(newKnight)
        #Bishops
        newBishop = Pieces.Bishop("C8","Black", self)
        self.rows[0].setRowPos(2,newBishop)
        self.cols[2].setColPos(0,newBishop)
        self.pieces.append(newBishop)
        self.remainingBlackPieces.append(newBishop)
        newBishop = Pieces.Bishop("F8","Black", self)
        self.rows[0].setRowPos(5,newBishop)
        self.cols[5].setColPos(0,newBishop)
        self.pieces.append(newBishop)
        self.remainingBlackPieces.append(newBishop)
        newBishop = Pieces.Bishop("C1","White", self)
        self.rows[7].setRowPos(2,newBishop)
        self.cols[2].setColPos(7,newBishop)
        self.pieces.append(newBishop)
        self.remainingWhitePieces.append(newBishop)
        newBishop = Pieces.Bishop("F1","White", self)
        self.rows[7].setRowPos(5,newBishop)
        self.cols[5].setColPos(7,newBishop)
        self.pieces.append(newBishop)
        self.remainingWhitePieces.append(newBishop)
        #Queens
        newQueen = Pieces.Queen("D8","Black", self)
        self.rows[0].setRowPos(3,newQueen)
        self.cols[3].setColPos(0,newQueen)
        self.pieces.append(newQueen)
        self.remainingBlackPieces.append(newQueen)
        newQueen = Pieces.Queen("D1","White", self)
        self.rows[7].setRowPos(3,newQueen)
        self.cols[3].setColPos(7,newQueen)
        self.pieces.append(newQueen)
        self.remainingWhitePieces.append(newQueen)
        #Kings
        newKing = Pieces.King("E8","Black", self)
        self.rows[0].setRowPos(4,newKing)
        self.cols[4].setColPos(0,newKing)
        self.pieces.append(newKing)
        self.blackKing = newKing
        self.remainingBlackPieces.append(newKing)
        newKing = Pieces.King("E1","White", self)
        self.rows[7].setRowPos(4,newKing)
        self.cols[4].setColPos(7,newKing)
        self.pieces.append(newKing)
        self.whiteKing = newKing
        self.remainingWhitePieces.append(newKing)
        #Find the valid moves for each piece
##        self.updateAllPieces()
##        self.recordBoard()
    def __eq__(self, val):
        x = val.getAllRemainingPieces()
        y = self.pieces
        if len(y) != len(x):
            return False
        for i in range(len(x)):
            if str(x[i]) != str(y[i]):
                return False
        return True
    def __ne__(self,val):
        return not(self.__eq__(val))
    def updateAllPieces(self):
        for piece in self.pieces:
            piece.updateValidMoves()
    def updateAllPieces2(self):
        #for testing if move will put me in check
        for piece in self.pieces:
            piece.updateValidMoves2()
    def updateWhitePieces(self):
        #for testing if move will put me in check
        for piece in self.remainingWhitePieces:
            piece.updateValidMoves2()
    def updateBlackPieces(self):
        #for testing if move will put me in check
        for piece in self.remainingBlackPieces:
            piece.updateValidMoves2()
    def whiteMove(self, start, end):
        start=start.upper()
        end=end.upper()
        capture = False
        if len(start)==2 and len(end)==2 and ((start[0] in "ABCDEFGH") and (start[1] in "12345678"))\
           and ((end[0] in "ABCDEFGH") and (end[1] in "12345678")):
            startcoord = (8-int(start[1]),"ABCDEFGH".find(start[0]))
            endcoord = (8-int(end[1]),"ABCDEFGH".find(end[0]))
            piece = self.getPieceAt(start)
            piece2 = self.getPieceAt(end)
            if piece == "Piece":
                piece.updateValidMoves2()
                if piece.getColor() == "White" and piece.isValidMove(end):
                    if not(piece.willBeCheck(end)):
                        if piece == "King" and start == "E1" and (end == "G1" or end == "C1"):
                            if piece.inCheck():
                                print "You cannot castle while in check."
                                return (0,False,False)
                        if piece2 == "Piece":
                            if piece2.getColor() != "White":
                                capture = True
    ##                            self.getAllRemainingPieces()
    ##                            self.checkRemainingBlackPieces()
                                self.pieces.remove(piece2)
                                piece2.setPosition("X")
                                self.remainingBlackPieces.remove(piece2)
    ##                            self.getAllRemainingPieces()
    ##                            self.checkRemainingBlackPieces()
                        elif piece == "Pawn" and piece.getPosition()[0]!= end[0]:
                            capture = True
                            checkcoord = (endcoord[0]+1,endcoord[1])
                            piece21 = self.getPieceAt(coordToSquare(checkcoord))
                            self.pieces.remove(piece21)
                            piece21.setPosition("X")
                            self.remainingBlackPieces.remove(piece21)
                            self.rows[checkcoord[0]].setRowPos(checkcoord[1], "x")
                            self.cols[checkcoord[1]].setColPos(checkcoord[0], "x")
                            

                        self.rows[startcoord[0]].setRowPos(startcoord[1], "x")
                        self.rows[endcoord[0]].setRowPos(endcoord[1], piece)
                        self.cols[startcoord[1]].setColPos(startcoord[0], "x")
                        self.cols[endcoord[1]].setColPos(endcoord[0], piece)
                        piece.setPosition(endcoord)
                        if piece == "King" and start == "E1" and end == "C1":
                            piece2 = self.getPieceAt("A1")
                            startcoord2 = squareToCoord("A1")
                            endcoord2 = squareToCoord("D1")
                            self.rows[startcoord2[0]].setRowPos(startcoord2[1], "x")
                            self.rows[endcoord2[0]].setRowPos(endcoord2[1], piece2)
                            self.cols[startcoord2[1]].setColPos(startcoord2[0], "x")
                            self.cols[endcoord2[1]].setColPos(endcoord2[0], piece2)
                            piece2.setPosition(endcoord2)
                        if piece == "King" and start == "E1" and end == "G1":
                            piece2 = self.getPieceAt("H1")
                            startcoord2 = squareToCoord("H1")
                            endcoord2 = squareToCoord("F1")
                            self.rows[startcoord2[0]].setRowPos(startcoord2[1], "x")
                            self.rows[endcoord2[0]].setRowPos(endcoord2[1], piece2)
                            self.cols[startcoord2[1]].setColPos(startcoord2[0], "x")
                            self.cols[endcoord2[1]].setColPos(endcoord2[0], piece2)
                            piece2.setPosition(endcoord2)

                        if piece == "Pawn" and (endcoord[0] == 0 or endcoord[0] == 7):
                            piece.updateValidMoves()
    ##                    self.updateAllPieces()
    ##                    self.updateAllPieces()
##                        self.undone = []
##                        self.recordBoard()
                        if not(self.blackHasMoves()):
                            if not(self.blackInCheck()):
                                print "Stalemate!"
                                self.endGame()
                            elif self.blackInCheck():
                                print "Checkmate. White wins!"
                                self.endGame()
                        return ("Good",piece=="Pawn",capture)
                    else:
                        print "This move will put you in check.a"
                elif not(piece.isValidMove(end)) or piece.getColor() == "Black":
                    print "This is not a valid move!"
            elif piece != "Piece":
                print "This is not a valid move!"
            else:
                print "Something went wrong while trying to move the piece."
        else:
            print "This is not a valid move!"
        return (0,False,False)
            
    def whiteMove2(self, start, end):
        start=start.upper()
        end=end.upper()
        if len(start)==2 and len(end)==2 and ((start[0] in "ABCDEFGH") and (start[1] in "12345678"))\
           and ((end[0] in "ABCDEFGH") and (end[1] in "12345678")):
            startcoord = (8-int(start[1]),"ABCDEFGH".find(start[0]))
            endcoord = (8-int(end[1]),"ABCDEFGH".find(end[0]))
            piece = self.getPieceAt(start)
            piece2 = self.getPieceAt(end)
            if piece == "Piece":
                if piece.getColor() == "White" and piece.isValidMove(end):
##                    if piece == "King" and start == "E1" and (end == "G1" or end == "C1"):
##                        if piece.inCheck():
##                            print "You cannot castle while in check."
##                            return (0,False,False)
                    if piece2 == "Piece":
                        if piece2.getColor() != "White":
##                            self.getAllRemainingPieces()
##                            self.checkRemainingBlackPieces()
                            self.pieces.remove(piece2)
                            piece2.setPosition("X")
                            self.remainingBlackPieces.remove(piece2)
##                            self.getAllRemainingPieces()
##                            self.checkRemainingBlackPieces()
                    elif piece == "Pawn" and piece.getPosition()[0]!= end[0]:
                        checkcoord = (endcoord[0]+1,endcoord[1])
                        piece21 = self.getPieceAt(coordToSquare(checkcoord))
                        self.pieces.remove(piece21)
                        piece21.setPosition("X")
                        self.remainingBlackPieces.remove(piece21)
                        self.rows[checkcoord[0]].setRowPos(checkcoord[1], "x")
                        self.cols[checkcoord[1]].setColPos(checkcoord[0], "x")                            
                    self.rows[startcoord[0]].setRowPos(startcoord[1], "x")
                    self.rows[endcoord[0]].setRowPos(endcoord[1], piece)
                    self.cols[startcoord[1]].setColPos(startcoord[0], "x")
                    self.cols[endcoord[1]].setColPos(endcoord[0], piece)
                    piece.setPosition(endcoord)
                    if piece == "King" and start == "E1" and end == "C1":
                        piece2 = self.getPieceAt("A1")
                        startcoord2 = squareToCoord("A1")
                        endcoord2 = squareToCoord("D1")
                        self.rows[startcoord2[0]].setRowPos(startcoord2[1], "x")
                        self.rows[endcoord2[0]].setRowPos(endcoord2[1], piece2)
                        self.cols[startcoord2[1]].setColPos(startcoord2[0], "x")
                        self.cols[endcoord2[1]].setColPos(endcoord2[0], piece2)
                        piece2.setPosition(endcoord2)
                    if piece == "King" and start == "E1" and end == "G1":
                        piece2 = self.getPieceAt("H1")
                        startcoord2 = squareToCoord("H1")
                        endcoord2 = squareToCoord("F1")
                        self.rows[startcoord2[0]].setRowPos(startcoord2[1], "x")
                        self.rows[endcoord2[0]].setRowPos(endcoord2[1], piece2)
                        self.cols[startcoord2[1]].setColPos(startcoord2[0], "x")
                        self.cols[endcoord2[1]].setColPos(endcoord2[0], piece2)
                        piece2.setPosition(endcoord2)
                    self.updateBlackPieces()
                elif not(piece.isValidMove(end)) or piece.getColor() == "Black":
                    print "This is not a valid move!"
            elif piece != "Piece":
                print "This is not a valid move!"
            else:
                print "Something went wrong while trying to move the piece."
        else:
            print "This is not a valid move!"
            
    def blackMove(self, start, end):
        start=start.upper()
        end=end.upper()
        capture = False
        if len(start)==2 and len(end)==2 and ((start[0] in "ABCDEFGH") and (start[1] in "12345678"))\
           and ((end[0] in "ABCDEFGH") and (end[1] in "12345678")):
            startcoord = (8-int(start[1]),"ABCDEFGH".find(start[0]))
            endcoord = (8-int(end[1]),"ABCDEFGH".find(end[0]))
            piece = self.getPieceAt(start)
            piece2 = self.getPieceAt(end)
            if piece == "Piece":
                piece.updateValidMoves2()
                if piece.getColor() == "Black" and piece.isValidMove(end):
                    if not(piece.willBeCheck(end)):
                        if piece == "King" and start == "E8" and (end == "G8" or end == "C8"):
                            if piece.inCheck():
                                print "You cannot castle while in check."
                                return (0,False,False)
                        if piece2 == "Piece":
                            if piece2.getColor() != "Black":
                                capture = True
    ##                            self.getAllRemainingPieces()
    ##                            self.checkRemainingWhitePieces()
                                self.pieces.remove(piece2)
                                piece2.setPosition("X")
                                self.remainingWhitePieces.remove(piece2)
    ##                            self.getAllRemainingPieces()
    ##                            self.checkRemainingWhitePieces()
                        elif piece == "Pawn" and piece.getPosition()[0]!= end[0]:
                            capture = True
                            checkcoord = (endcoord[0]-1,endcoord[1])
                            piece21 = self.getPieceAt(coordToSquare(checkcoord))
                            self.pieces.remove(piece21)
                            piece21.setPosition("X")
                            self.remainingBlackPieces.remove(piece21)
                            self.rows[checkcoord[0]].setRowPos(checkcoord[1], "x")
                            self.cols[checkcoord[1]].setColPos(checkcoord[0], "x")
                        self.rows[startcoord[0]].setRowPos(startcoord[1], "x")
                        self.rows[endcoord[0]].setRowPos(endcoord[1], piece)
                        self.cols[startcoord[1]].setColPos(startcoord[0], "x")
                        self.cols[endcoord[1]].setColPos(endcoord[0], piece)
                        piece.setPosition(endcoord)
                        if piece == "King" and start == "E8" and end == "C8":
                            piece2 = self.getPieceAt("A8")
                            startcoord2 = squareToCoord("A8")
                            endcoord2 = squareToCoord("D8")
                            self.rows[startcoord2[0]].setRowPos(startcoord2[1], "x")
                            self.rows[endcoord2[0]].setRowPos(endcoord2[1], piece2)
                            self.cols[startcoord2[1]].setColPos(startcoord2[0], "x")
                            self.cols[endcoord2[1]].setColPos(endcoord2[0], piece2)
                            piece2.setPosition(endcoord2)
                        if piece == "King" and start == "E8" and end == "G8":
                            piece2 = self.getPieceAt("H8")
                            startcoord2 = squareToCoord("H8")
                            endcoord2 = squareToCoord("F8")
                            self.rows[startcoord2[0]].setRowPos(startcoord2[1], "x")
                            self.rows[endcoord2[0]].setRowPos(endcoord2[1], piece2)
                            self.cols[startcoord2[1]].setColPos(startcoord2[0], "x")
                            self.cols[endcoord2[1]].setColPos(endcoord2[0], piece2)
                            piece2.setPosition(endcoord2)
                        if piece == "Pawn" and (endcoord[0] == 0 or endcoord[0] == 7):
                            piece.updateValidMoves()
                        if not(self.whiteHasMoves()):
                            if not(self.whiteInCheck()):
                                print "Stalemate!"
                                self.endGame()
                            elif self.whiteInCheck():
                                print "Checkmate! Black wins!"
                                self.endGame()
    ##                    self.updateAllPieces()
    ##                    self.updateAllPieces()
##                        self.undone = []
##                        self.recordBoard()
                        return ("Good",piece=="Pawn",capture)
                    else:
                        print "This move will put you in check.b"
                elif not(piece.isValidMove(end)) or piece.getColor() == "White":
                    print "This is not a valid move!"
            elif piece != "Piece":
                print "This is not a valid move!"
            else:
                print "Something went wrong while trying to move the piece."
        else:
            print "This is not a valid move!"
        return (0,False,False)            

    def blackMove2(self, start, end):
        start=start.upper()
        end=end.upper()
        if len(start)==2 and len(end)==2 and ((start[0] in "ABCDEFGH") and (start[1] in "12345678"))\
           and ((end[0] in "ABCDEFGH") and (end[1] in "12345678")):
            startcoord = (8-int(start[1]),"ABCDEFGH".find(start[0]))
            endcoord = (8-int(end[1]),"ABCDEFGH".find(end[0]))
            piece = self.getPieceAt(start)
            piece2 = self.getPieceAt(end)
            if piece == "Piece":
                if piece.getColor() == "Black" and piece.isValidMove(end):
##                    if piece == "King" and start == "E8" and (end == "G8" or end == "C8"):
##                        if piece.inCheck():
##                            print "You cannot castle while in check."
##                            return (0,False,False)
                    if piece2 == "Piece":
                        if piece2.getColor() != "Black":
##                            self.getAllRemainingPieces()
##                            self.checkRemainingWhitePieces()
                            self.pieces.remove(piece2)
                            piece2.setPosition("X")
                            self.remainingWhitePieces.remove(piece2)
##                            self.getAllRemainingPieces()
##                            self.checkRemainingWhitePieces()
                    elif piece == "Pawn" and piece.getPosition()[0]!= end[0]:
                        checkcoord = (endcoord[0]-1,endcoord[1])
                        piece21 = self.getPieceAt(coordToSquare(checkcoord))
                        self.pieces.remove(piece21)
                        piece21.setPosition("X")
                        self.remainingBlackPieces.remove(piece21)
                        self.rows[checkcoord[0]].setRowPos(checkcoord[1], "x")
                        self.cols[checkcoord[1]].setColPos(checkcoord[0], "x")                            
                    self.rows[startcoord[0]].setRowPos(startcoord[1], "x")
                    self.rows[endcoord[0]].setRowPos(endcoord[1], piece)
                    self.cols[startcoord[1]].setColPos(startcoord[0], "x")
                    self.cols[endcoord[1]].setColPos(endcoord[0], piece)
                    piece.setPosition(endcoord)
                    if piece == "King" and start == "E8" and end == "C8":
                        piece2 = self.getPieceAt("A8")
                        startcoord2 = squareToCoord("A8")
                        endcoord2 = squareToCoord("D8")
                        self.rows[startcoord2[0]].setRowPos(startcoord2[1], "x")
                        self.rows[endcoord2[0]].setRowPos(endcoord2[1], piece2)
                        self.cols[startcoord2[1]].setColPos(startcoord2[0], "x")
                        self.cols[endcoord2[1]].setColPos(endcoord2[0], piece2)
                        piece2.setPosition(endcoord2)
                    if piece == "King" and start == "E8" and end == "G8":
                        piece2 = self.getPieceAt("H8")
                        startcoord2 = squareToCoord("H8")
                        endcoord2 = squareToCoord("F8")
                        self.rows[startcoord2[0]].setRowPos(startcoord2[1], "x")
                        self.rows[endcoord2[0]].setRowPos(endcoord2[1], piece2)
                        self.cols[startcoord2[1]].setColPos(startcoord2[0], "x")
                        self.cols[endcoord2[1]].setColPos(endcoord2[0], piece2)
                        piece2.setPosition(endcoord2)
                    self.updateWhitePieces()
                elif not(piece.isValidMove(end)) or piece.getColor() == "White":
                    print "This is not a valid move!"
            elif piece != "Piece":
                print "This is not a valid move!"
            else:
                print "Something went wrong while trying to move the piece."
        else:
            print "This is not a valid move!"

    def checkWhitePossibleMoves(self, spot):
        spot = spot.upper()
        piece = self.getPieceAt(spot)
        if piece != "Piece":
##            print "here1"
            print "There is no piece at this position!"
        elif piece.getColor()!= "White":
##            print "here2"
            print "This is not your piece!"
        else:
            print piece
            piece.updateValidMoves()
            print piece.getValidMoves()
    def checkBlackPossibleMoves(self, spot):
        spot = spot.upper()
        piece = self.getPieceAt(spot)        
        if piece != "Piece":
##            print "here1"
            print "There is no piece at this position!"
        elif piece.getColor()!= "Black":
##            print "here2"
            print "This is not your piece!"
        else:
            print piece
            piece.updateValidMoves()
            print piece.getValidMoves()
    def getAllRemainingPieces(self):
##        L = []
##        for p in self.pieces:
##            L.append(str(p))
##        print L
        return self.pieces
    def getPieceAt(self, spot):
        #gets the piece if any at spot given in form A1 to H8
        if len(spot)==2 and ((spot[0] in "ABCDEFGH") and (spot[1] in "12345678")):
            coord = (8-int(spot[1]),"ABCDEFGH".find(spot[0]))
            piece = self.rows[coord[0]].getRowPos(coord[1])
##            print coord
##            print piece
            if piece == "Piece":
##                print piece
                return piece
##            print "No piece found here"
            return None
        print "This is not a valid square. Cannot retrieve piece."
    def checkRemainingWhitePieces(self):
##        L = []
##        for p in self.remainingWhitePieces:
##            L.append(str(p))
##        print L
        return self.remainingWhitePieces
    def checkRemainingBlackPieces(self):
##        L = []
##        for p in self.remainingBlackPieces:
##            L.append(str(p))
##        print L
        return self.remainingBlackPieces

##    def checkMoves(self, pos):
##        pass
##    def recordBoard(self):
##        self.record.append(copy.deepcopy(self))
##    def undo(self):
####        u = self.record
##        if len(self.record)>=1:
##            newBoard = copy.deepcopy(self.record[-1])
##            newBoard.undone.append(copy.deepcopy(self))
##            return newBoard
##        else:
##            print "There are no more moves to undo"
##            return self
##    def redo(self):
##        if len(self.undone)>=1:
##            newBoard = copy.deepcopy(self.undone.pop())
##            newBoard.record.append(copy.deepcopy(self))
##            return newBoard
##        else:
##            "This is the furthest ahead you can go."
##            return self
    def whiteHasMoves(self):
        for piece in self.remainingWhitePieces:
            piece.updateValidMoves()
            if len(piece.getValidMoves()) >= 1:
                return True
        return False      
    def blackHasMoves(self):
        for piece in self.remainingBlackPieces:
            piece.updateValidMoves()
            if len(piece.getValidMoves()) >= 1:
                return True
        return False
    def whiteInCheck(self):
        return self.whiteKing.inCheck()
    def blackInCheck(self):
        return self.blackKing.inCheck()
    def endGame(self):
        self.ended = True
        print "Game Over!"
    def isEndGame(self):
        return self.ended
    def __str__(self):
        s = "    A B C D E F G H\n\n"
        i = 9
        for row in self.rows:
            i -= 1
            s += str(i)
            s += "   "
            s += str(row)
            s += "\n"
        return s[:-1]



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
