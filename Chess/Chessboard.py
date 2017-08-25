# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 11:08:21 2017

@author: aokeke
"""
import numpy as np
import References as Ref
np.set_printoptions(threshold=np.nan)

class Chessboard:
    def __init__(self,gameboard=None,EP=None,WC=3,BC=3):
        if gameboard is None:
            #Default gameboard
            self.gameboard = np.zeros((8,8),dtype=int)
            
            #White Pieces
            self.gameboard[7,(0,7)]     = Ref.White*Ref.RookID
            self.gameboard[7,(1,6)]     = Ref.White*Ref.KnightID
            self.gameboard[7,(2,5)]     = Ref.White*Ref.BishopID
            self.gameboard[7,3]         = Ref.White*Ref.QueenID
            self.gameboard[7,4]         = Ref.White*Ref.KingID
            self.gameboard[6,range(8)]  = Ref.White*Ref.PawnID
            
            #Black Pieces
            self.gameboard[0,(0,7)]     = Ref.Black*Ref.RookID
            self.gameboard[0,(1,6)]     = Ref.Black*Ref.KnightID
            self.gameboard[0,(2,5)]     = Ref.Black*Ref.BishopID
            self.gameboard[0,3]         = Ref.Black*Ref.QueenID
            self.gameboard[0,4]         = Ref.Black*Ref.KingID
            self.gameboard[1,range(8)]  = Ref.Black*Ref.PawnID
        else:
            self.gameboard = gameboard
        self.EP = EP #tuple that says what square can be taken by en passant
        self.WC = WC #white castle rights as a binary second bit is left first bit is right
        self.BC = BC #black castle rights as a binary second bit is left first bit is right
        
        #May need to reconsider how to implement these
        self.white_moves_unvalidated = None
        self.black_moves_unvalidated = None
        self.white_moves = None
        self.black_moves = None
        
        #padded board
        self.padded_board = np.vstack((np.inf*np.ones((1,8),int),self.gameboard))
        self.padded_board = np.vstack((self.padded_board,np.inf*np.ones((1,8),int)))
        self.padded_board = np.hstack((np.inf*np.ones((10,1),int),self.padded_board))
        self.padded_board = np.hstack((self.padded_board,np.inf*np.ones((10,1),int)))
        

    def get_black_moves(self):
        """
        returns a dictionary of moves that black can make not filtering moves that 
        put black in check.
        Format is 'moves' is mapped to a set of moves and 'threatened_squares'
        is mapped to a set of threatened positions.
        """
        if self.black_moves_unvalidated is not None:
            return self.black_moves_unvalidated
        else:
            raise NotImplementedError
    def get_white_moves(self):
        """
        returns a dictionary of moves that black can make not filtering moves that 
        put white in check.
        Format is 'moves' is mapped to a set of moves and 'threatened_squares'
        is mapped to a set of threatened positions.
        """
        if self.white_moves_unvalidated is not None:
            return self.white_moves_unvalidated
        else:
            raise NotImplementedError

    def get_moves_from_start(self,start):
        moves = set()
        piece = self.gameboard[start]
        if piece==0:
            return moves
        player = np.sign(piece)

        move_array = np.zeros((10,10),int) #with padding
        print ("piece:",piece)
        if abs(piece) == Ref.KingID:
            print ("Getting king moves")
            raise NotImplementedError
        elif (abs(piece)==Ref.QueenID)or(abs(piece)==Ref.RookID)or(abs(piece)==Ref.BishopID):
            print ("Getting queen/bishop/rook moves")
            if (abs(piece)==Ref.QueenID)or(abs(piece)==Ref.RookID):

                #left ray
                indOfFirstObj = start[1]+2+np.argwhere(self.padded_board[start[0]+1,start[1]+2:]!=0)[0][0] #get the first element
                print (indOfFirstObj)
                print (range(start[1]+2,indOfFirstObj))
                move_array[start[0]+1,range(start[1]+2,indOfFirstObj)] = 1
                if np.sign(self.gameboard[start[0],indOfFirstObj-1])!=np.sign(self.gameboard[start]):
                    move_array[start[0]+1,indOfFirstObj] = 1
                print (move_array)
                print ("------left--------")
                #down ray
                indOfFirstObj = start[0]+2+np.argwhere(self.padded_board[start[0]+2:,start[1]+1]!=0)[0][0]
                move_array[range(start[0]+2,indOfFirstObj),start[1]+1] = 1
                print (indOfFirstObj)
                print (range(start[0]+2,indOfFirstObj))
                if np.sign(self.gameboard[indOfFirstObj-1,start[1]])!=np.sign(self.gameboard[start]):
                    move_array[indOfFirstObj,start[1]+1] = 1
                print (move_array)
                print ("-------down-------")
                #right ray
                indOfFirstObj = np.argwhere(self.padded_board[start[0]+1,:start[1]+1]!=0)[-1][0]
                move_array[start[0]+1,range(indOfFirstObj+1,start[1]+1)] = 1
                print (indOfFirstObj)
                print (range(indOfFirstObj+1,start[1]+1))
                if np.sign(self.gameboard[start[0],indOfFirstObj-1])!=np.sign(self.gameboard[start]):
                    move_array[start[0]+1,indOfFirstObj] = 1
                print (move_array)
                print ("------right--------")
                #up ray
                indOfFirstObj = np.argwhere(self.padded_board[:start[0]+1,start[1]+1]!=0)[-1][0]
                move_array[range(indOfFirstObj+1,start[0]+1),start[1]+1] = 1
                print (indOfFirstObj)
                print (range(indOfFirstObj+1,start[0]+1))
                if np.sign(self.gameboard[indOfFirstObj-1,start[1]])!=np.sign(self.gameboard[start]):
                    move_array[indOfFirstObj,start[1]+1] = 1
                print (move_array)
                print ("------up--------")
            if (abs(piece)==Ref.QueenID)or(abs(piece)==Ref.BishopID):
                #diagonal rays
                raise NotImplementedError
        elif abs(piece) == Ref.KnightID:
            print ("Getting knight moves")
            raise NotImplementedError
        elif abs(piece) == Ref.PawnID:
            print ("Getting pawn moves")
            if player == Ref.White:
                raise NotImplementedError
            elif player == Ref.Black:
                raise NotImplementedError
        
        
        move_array = move_array[1:9,1:9] #strip padding
        moves = set(map(tuple,np.argwhere(move_array))) #convert to a set of tuples
        return moves
    
    def get_valid_moves(self,player):
        if player == Ref.White:
            if self.white_moves is not None:
                self.white_moves = self.validate_moves(player,self.get_white_moves())
            return self.white_moves
        elif player == Ref.Black:
            if self.black_moves is None:
                self.black_moves = self.validate_moves(player,self.get_black_moves())
            return self.black_moves
        
    def make_move(self,player,move):
        """
        player = 0 allows you to override the check to see if it is a valid move
        
        returns a new chessboard object if a valid move was selected. returns None if the move could not be made
        second value of the return is whether or not a pawn was moved
        """
        
        #check if it is a valid move
        if (player==0):
            newBoard = self.gameboard.copy()
            newBoard[move[0]],newBoard[move[1]] = 0,newBoard[move[0]]
            #Update these values based on move made
            EP = self.EP
            WC = self.WC
            BC = self.BC
            return Chessboard(newBoard,EP,WC,BC)
        else:
            moves = self.get_valid_moves(player)
            if (move in moves):
                newBoard = self.gameboard.copy()
                newBoard[move[0]],newBoard[move[1]] = 0,newBoard[move[0]]
                #Update these values based on move made
                EP = None
                WC = self.WC
                BC = self.BC
                
                #Update En Passant option
                if abs(self.gameboard[move[0]])==Ref.PawnID:
                    if (move[0][0]==6 and move[1][0]==4):
                        EP = (5,move[0][1])
                    elif (move[0][0]==1 and move[1][0]==3):
                        EP = (2,move[0][1])
                #King moved break castle 
                if self.gameboard[move[0]]==Ref.White*Ref.KingID:
                    WC = 0
                if self.gameboard[move[0]]==Ref.Black*Ref.KingID:
                    BC = 0
                #Left Rooks break castle
                if move[0]==(7,0) or move[1]==(7,0):
                    WC &= 1
                if move[0]==(0,0) or move[1]==(0,0):
                    BC &= 1
                #Right Rooks break castle
                if move[0]==(7,7) or move[1]==(7,7):
                    WC &= 2
                if move[0]==(0,7) or move[1]==(0,7):
                    BC &= 2
                pawnMoved = (abs(self.gameboard[move[0]]) == Ref.PawnID)
                return Chessboard(newBoard,EP,WC,BC),pawnMoved
        return None,False
        
    def validate_moves(self,player,player_moves):
        valid_moves = set()
        for m in player_moves:
            if self.validate_single_move(player,m):
                valid_moves.add(m)
        return valid_moves

    def validate_single_move(self,player,move):
        tBoard,_ = self.make_move(0,move)
        if player==Ref.White:
            op_moves = tBoard.get_black_moves()
        elif player==Ref.Black:
            op_moves = tBoard.get_white_moves()
        king_pos = tuple(np.argwhere(tBoard.gameboard==player*Ref.KingID)[0])
        if king_pos not in op_moves['threatened_squares']:
            return True
        return False
    def __eq__(self,other):
        if type(self)!=type(other):
            return False
        return np.all(self.gameboard==other.gameboard)

    def __neq__(self,other):
        return not(self.__eq__(other))
    
    def __str__(self):
        board = np.empty((8,8),dtype=str)
        #White pieces
        board[np.where(self.gameboard==Ref.White*Ref.KingID)]   = "K"
        board[np.where(self.gameboard==Ref.White*Ref.QueenID)]  = "Q"
        board[np.where(self.gameboard==Ref.White*Ref.RookID)]   = "R"
        board[np.where(self.gameboard==Ref.White*Ref.BishopID)] = "B"
        board[np.where(self.gameboard==Ref.White*Ref.KnightID)] = "N"
        board[np.where(self.gameboard==Ref.White*Ref.PawnID)]   = "P"
        #Black pieces
        board[np.where(self.gameboard==Ref.Black*Ref.KingID)]   = "k"
        board[np.where(self.gameboard==Ref.Black*Ref.QueenID)]  = "q"
        board[np.where(self.gameboard==Ref.Black*Ref.RookID)]   = "r"
        board[np.where(self.gameboard==Ref.Black*Ref.BishopID)] = "b"
        board[np.where(self.gameboard==Ref.Black*Ref.KnightID)] = "n"
        board[np.where(self.gameboard==Ref.Black*Ref.PawnID)]   = "p"
        
        #Empty squares to keep it all in line
        board[np.where(self.gameboard==0)] = " "
        return str(board)
    def __repr__(self):
        return "\n"+self.__str__()+"\n"