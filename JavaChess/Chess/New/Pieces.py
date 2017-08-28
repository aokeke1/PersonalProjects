class Piece(object):
    def __init__(self, position, color, board):
        position = position.upper()
        assert  (len(position)==2) and (position[0] in "ABCDEFGH") and  (position[1] in "12345678")
        self.position = position
        color = color.upper()
        assert (color == "WHITE" or color == "BLACK")
        self.color = color
        self.board = board
        self.name = ""
        self.hasMoved = 0
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, val):
        """ Compare position of val to position of self. Return true if the two pieces have the same position. """
        if type(val)== type(self):
            return val.getPosition()==self.getPosition() and self.getName()==val.getName()
        return False
    
    def __ne__(self, val):
        return not(self.__eq__(val))
        
    def getPosition(self):
        return self.position
        
    def setPosition(self, position):
        position = position.upper()
        assert (len(position)==2) and (position[0] in "ABCDEFGH") and  (position[1] in "12345678")
        self.position = position
            
    def getColor(self):
        return self.color
        
    def getName(self):
        return self.name
        
    def getMoves(self):
        return []
    
    def getMoveStatus(self):
        """
        Used to determine if a pawn can double move or
        if a king-rook pair can castle
        """
        return self.hasMoved   



class King(Piece):
    def __init__(self, position, color, board):
        super(King, self).__init__(position, color, board)
        self.name = color[0]+'K'
    
    def inCheck(self):
        pass
    def canQueenSideCastle(self):
        pass
    def canKingSideCastle(self):
        pass
    def getMoves(self):
        pass

class Queen(Piece):
    def __init__(self, position, color, board):
        super(Queen, self).__init__(position, color, board)
        self.name = color[0]+'Q'

    def getMoves(self):
        pass
    
class Rook(Piece):
    def __init__(self, position, color, board):
        super(Rook, self).__init__(position, color, board)
        self.name = color[0]+'R'
        
    def getMoves(self):
        pass

class Bishop(Piece):
    def __init__(self, position, color, board):
        super(Bishop, self).__init__(position, color, board)
        self.name = color[0]+'B'
        
    def getMoves(self):
        pass

class Knight(Piece):
    def __init__(self, position, color, board):
        super(Knight, self).__init__(position, color, board)
        self.name = color[0]+'N'
    
    def getMoves(self):
        pass
    
class Pawn(Piece):
    def __init__(self, position, color, board):
        super(Pawn, self).__init__(position, color, board)
        self.name = color[0]+'P'
        self.lastPosition = position
    
    def getLastPosition(self):
        return self.lastPosition
        
    def getMoves(self):
        pass