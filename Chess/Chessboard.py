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
        self.padded_board = np.vstack((np.inf*np.ones((1,8),int),self.padded_board))
        self.padded_board = np.vstack((self.padded_board,np.inf*np.ones((1,8),int)))
        self.padded_board = np.vstack((self.padded_board,np.inf*np.ones((1,8),int)))
        self.padded_board = np.hstack((np.inf*np.ones((12,1),int),self.padded_board))
        self.padded_board = np.hstack((np.inf*np.ones((12,1),int),self.padded_board))
        self.padded_board = np.hstack((self.padded_board,np.inf*np.ones((12,1),int)))
        self.padded_board = np.hstack((self.padded_board,np.inf*np.ones((12,1),int)))
        

    def get_black_moves(self):
        """
        returns a dictionary of moves that black can make not filtering moves that 
        put black in check.
        Format is 'moves' is mapped to a set of moves and 'threatened_squares'
        is mapped to a set of threatened positions.
        """
        if self.black_moves_unvalidated is None:
            self.black_moves_unvalidated = {'moves':set(),'threatened_squares':set()}
            possible_starts = np.argwhere(np.sign(self.gameboard)==Ref.Black)
            for start in possible_starts:
                moves,threatened = self.get_moves_from_start(tuple(start))
                self.black_moves_unvalidated['threatened_squares'].update(threatened)
                self.black_moves_unvalidated['moves'].update(moves)
        return self.black_moves_unvalidated
    def get_white_moves(self):
        """
        returns a dictionary of moves that black can make not filtering moves that 
        put white in check.
        Format is 'moves' is mapped to a set of moves and 'threatened_squares'
        is mapped to a set of threatened positions.
        """
        if self.white_moves_unvalidated is None:
            self.white_moves_unvalidated = {'moves':set(),'threatened_squares':set()}
            possible_starts = np.argwhere(np.sign(self.gameboard)==Ref.White)
            for start in possible_starts:
                moves,threatened = self.get_moves_from_start(tuple(start))
                self.white_moves_unvalidated['threatened_squares'].update(threatened)
                self.white_moves_unvalidated['moves'].update(moves)
        return self.white_moves_unvalidated
        
    def get_moves_from_start(self,start):
        moves = set()
        extra_moves = set()
        threatened = set()
        piece = self.gameboard[start]
        if piece==0:
            return moves,threatened
        player = np.sign(piece)

        move_array = np.zeros((12,12),int) #with padding
        
        
        if abs(piece) == Ref.KingID:
#            print ("Getting king moves")
            pad_start = start[0]+2,start[1]+2
            tmoves = np.array([[ 1,  1],
                               [ 1, -1],
                               [-1,  1],
                               [-1, -1],
                               [ 1,  0],
                               [-1,  0],
                               [ 0,  1],
                               [ 0, -1]])
            tmoves = (tmoves+pad_start).T
            move_array[tmoves[0],tmoves[1]] = 1
            move_array = (np.sign(self.padded_board)!=np.sign(self.padded_board[pad_start]))&move_array
            #Castling
            #Don't need to update threatened because involved squares need to be empty for castling
            if np.sign(piece)==Ref.White:
                castle_rights = self.WC
                castle_row = 9
            elif np.sign(piece)==Ref.Black:
                castle_rights = self.BC
                castle_row = 2
            if castle_rights&2 and np.all(self.padded_board[castle_row,(6,5,4,3,2)] == [player*Ref.KingID,0,0,0,player*Ref.RookID]):
                #Castle Left
                extra_moves.add((start,(castle_row-2,2),"CQ"))
            if castle_rights&1 and np.all(self.padded_board[castle_row,(6,7,8,9)] == [player*Ref.KingID,0,0,player*Ref.RookID]):
                #Castle Right
                extra_moves.add((start,(castle_row-2,6),"CK"))
                
            
        elif (abs(piece)==Ref.QueenID)or(abs(piece)==Ref.RookID)or(abs(piece)==Ref.BishopID):
#            print ("Getting queen/bishop/rook moves")
            if (abs(piece)==Ref.QueenID)or(abs(piece)==Ref.RookID):

                #right ray
                indOfFirstObj = start[1]+3+np.argwhere(self.padded_board[start[0]+2,start[1]+3:]!=0)[0][0] #get the first element
                move_array[start[0]+2,range(start[1]+3,indOfFirstObj)] = 1
                if indOfFirstObj<=9 and np.sign(self.gameboard[start[0],indOfFirstObj-2])!=np.sign(self.gameboard[start]):
                    move_array[start[0]+2,indOfFirstObj] = 1

                #down ray
                indOfFirstObj = start[0]+3+np.argwhere(self.padded_board[start[0]+3:,start[1]+2]!=0)[0][0]
                move_array[range(start[0]+3,indOfFirstObj),start[1]+2] = 1
                if indOfFirstObj<=9 and np.sign(self.gameboard[indOfFirstObj-2,start[1]])!=np.sign(self.gameboard[start]):
                    move_array[indOfFirstObj,start[1]+2] = 1

                #left ray
                indOfFirstObj = np.argwhere(self.padded_board[start[0]+2,:start[1]+2]!=0)[-1][0]
                move_array[start[0]+2,range(indOfFirstObj+1,start[1]+2)] = 1
                if indOfFirstObj>=2 and np.sign(self.gameboard[start[0],indOfFirstObj-2])!=np.sign(self.gameboard[start]):
                    move_array[start[0]+2,indOfFirstObj] = 1

                #up ray
                indOfFirstObj = np.argwhere(self.padded_board[:start[0]+2,start[1]+2]!=0)[-1][0]
                move_array[range(indOfFirstObj+1,start[0]+2),start[1]+2] = 1
                if indOfFirstObj>=2 and np.sign(self.gameboard[indOfFirstObj-2,start[1]])!=np.sign(self.gameboard[start]):
                    move_array[indOfFirstObj,start[1]+2] = 1

            if (abs(piece)==Ref.QueenID)or(abs(piece)==Ref.BishopID):
                #Upper left to lower right diagonal
                diag_offset = start[1]-start[0]
                curr_pos = min(start)+2
                pad_start = start[0]+2,start[1]+2
                #increasing direction
                relIndOfFirstObj = np.argwhere(self.padded_board.diagonal(offset=diag_offset)[curr_pos+1:]!=0)[0][0]
                move_array[range(pad_start[0]+1,pad_start[0]+1+relIndOfFirstObj),\
                           range(pad_start[1]+1,pad_start[1]+1+relIndOfFirstObj)] = 1
                obj_coord = (pad_start[0]+1+relIndOfFirstObj,pad_start[1]+1+relIndOfFirstObj)
                if obj_coord[0]<=9 and obj_coord[1]<=9 and self.padded_board[obj_coord]!=np.sign(self.padded_board[pad_start]):
                    move_array[obj_coord] = 1
                #decreasing direction
                relIndOfFirstObj = curr_pos - np.argwhere(self.padded_board.diagonal(offset=diag_offset)[:curr_pos]!=0)[-1][0]
                move_array[range(pad_start[0]-relIndOfFirstObj+1,pad_start[0]),\
                           range(pad_start[1]-relIndOfFirstObj+1,pad_start[1])] = 1
                obj_coord = (pad_start[0]-relIndOfFirstObj,pad_start[1]-relIndOfFirstObj)
                if obj_coord[0]>=2 and obj_coord[1]>=2 and self.padded_board[obj_coord]!=np.sign(self.padded_board[pad_start]):
                    move_array[obj_coord] = 1
                #Upper right to lower left diagonal
                move_array = np.fliplr(move_array)
                flip_padded_board = np.fliplr(self.padded_board)
                start = start[0],7-start[1]
                #repeat above process
                diag_offset = start[1]-start[0]
                curr_pos = min(start)+2
                pad_start = start[0]+2,start[1]+2
                #increasing direction
                relIndOfFirstObj = np.argwhere(flip_padded_board.diagonal(offset=diag_offset)[curr_pos+1:]!=0)[0][0]
                move_array[range(pad_start[0]+1,pad_start[0]+1+relIndOfFirstObj),\
                           range(pad_start[1]+1,pad_start[1]+1+relIndOfFirstObj)] = 1
                obj_coord = (pad_start[0]+1+relIndOfFirstObj,pad_start[1]+1+relIndOfFirstObj)
                if obj_coord[0]<=9 and obj_coord[1]<=9 and flip_padded_board[obj_coord]!=np.sign(flip_padded_board[pad_start]):
                    move_array[obj_coord] = 1
                #decreasing direction
                relIndOfFirstObj = curr_pos - np.argwhere(flip_padded_board.diagonal(offset=diag_offset)[:curr_pos]!=0)[-1][0]
                move_array[range(pad_start[0]-relIndOfFirstObj+1,pad_start[0]),\
                           range(pad_start[1]-relIndOfFirstObj+1,pad_start[1])] = 1
                obj_coord = (pad_start[0]-relIndOfFirstObj,pad_start[1]-relIndOfFirstObj)
                if obj_coord[0]>=2 and obj_coord[1]>=2 and flip_padded_board[obj_coord]!=np.sign(flip_padded_board[pad_start]):
                    move_array[obj_coord] = 1
                move_array = np.fliplr(move_array)
                start = start[0],7-start[1]

        elif abs(piece) == Ref.KnightID:
#            print ("Getting knight moves")
            pad_start = start[0]+2,start[1]+2
            tmoves = np.array([[ 1,  2],
                               [ 1, -2],
                               [-1,  2],
                               [-1, -2],
                               [ 2,  1],
                               [ 2, -1],
                               [-2,  1],
                               [-2, -1]])
            tmoves = (tmoves+pad_start).T
            move_array[tmoves[0],tmoves[1]] = 1
            move_array = (np.sign(self.padded_board)!=np.sign(self.padded_board[pad_start]))&move_array
        elif abs(piece) == Ref.PawnID:
#            print ("Getting pawn moves")
            
            new_row = start[0]-player
            new_row2 = start[0]-2*player                        
            
            #Single Move Forward
            if self.gameboard[new_row,start[1]]==0:
                if new_row==0 or new_row==7:
                    extra_moves.add((start,(new_row,start[1]),"PQ"))
                    extra_moves.add((start,(new_row,start[1]),"PR"))
                    extra_moves.add((start,(new_row,start[1]),"PB"))
                    extra_moves.add((start,(new_row,start[1]),"PN"))
                else:
                    #don't use move_array for this because this move aren't threats
                    extra_moves.add((start,(new_row,start[1])))
                    
            #Capture Left
            if start[1]>0 and np.sign(self.gameboard[new_row,start[1]-1])==-player:
                if new_row==0 or new_row==7:
                    extra_moves.add((start,(new_row,start[1]-1),"PQ"))
                    extra_moves.add((start,(new_row,start[1]-1),"PR"))
                    extra_moves.add((start,(new_row,start[1]-1),"PB"))
                    extra_moves.add((start,(new_row,start[1]-1),"PN"))
                    threatened.add((new_row,start[1]+1))
                else:
                    move_array[new_row+2,start[1]+1] = 1
                
            #Capture Right
            if start[1]<7 and np.sign(self.gameboard[new_row,start[1]+1])==-player:
                if new_row==0 or new_row==7:
                    extra_moves.add((start,(new_row,start[1]+1),"PQ"))
                    extra_moves.add((start,(new_row,start[1]+1),"PR"))
                    extra_moves.add((start,(new_row,start[1]+1),"PB"))
                    extra_moves.add((start,(new_row,start[1]+1),"PN"))
                    threatened.add((new_row,start[1]+1))
                else:
                    move_array[new_row+2,start[1]+3] = 1
                
            #Double Move Forward
            if ((start[0]==1 and player==Ref.Black) or (start[0]==6 and player==Ref.White)) and self.gameboard[new_row2,start[1]]==0:
                #don't use move_array for this because this move aren't threats
                extra_moves.add((start,(new_row2,start[1])))
                
            #En Passant
            if (self.EP is not None) and ((new_row,start[1]-1)==self.EP or (new_row,start[1]+1)==self.EP):
                extra_moves.add((start,self.EP,"EP"))
                #threatened not needed here because this square will always be empty
            
        
        move_array = move_array[2:10,2:10] #strip padding
        ends = np.argwhere(move_array)
#        for end in ends:
#            e = tuple(end)
#            threatened.add(e)
#            moves.add((start,e))
        threatened.update(set(map(tuple,ends)))
        moves = set(map(self.link_to_start,(start,)*len(ends),ends)) #convert to a set of tuples
#        print ("start:",start)
#        print (self.gameboard)
#        print (move_array)
        moves.update(extra_moves)
        return moves,threatened
    
    def link_to_start(self,start,end):
        return (start,tuple(end))
    
    def get_valid_moves(self,player):
        if player == Ref.White:
            if self.white_moves is None:
                self.white_moves = self.validate_moves(player,self.get_white_moves()['moves'])
            return self.white_moves
        elif player == Ref.Black:
            if self.black_moves is None:
                self.black_moves = self.validate_moves(player,self.get_black_moves()['moves'])
            return self.black_moves
        
    def make_move(self,player,move):
        """
        player = 0 allows you to override the check to see if it is a valid move
        
        returns a new chessboard object if a valid move was selected. returns None if the move could not be made
        second value of the return is whether or not a pawn was moved
        """
        
        okToMove = False
        if (player==0):
            #make move without checking if it is valid
            okToMove = True
        else:
            #check if it is a valid move
            moves = self.get_valid_moves(player)
            if (move in moves):
                okToMove = True
        if okToMove:
            newBoard = self.gameboard.copy()
            newBoard[move[0]],newBoard[move[1]] = 0,newBoard[move[0]]
            if len(move)==3:
                flag = move[3]
                if flag=="CK":
                    newBoard[move[0][0],7],newBoard[move[0][0],5] = 0,np.sign(newBoard[move[1]])*Ref.RookID
                elif flag=="CQ":
                    newBoard[move[0][0],0],newBoard[move[0][0],3] = 0,np.sign(newBoard[move[1]])*Ref.RookID
                elif flag=="EP":
                    newBoard[move[0][0],move[1][1]] = 0
                elif flag=="PQ":
                    newBoard[move[1]] = np.sign(newBoard[move[1]])*Ref.QueenID
                elif flag=="PR":
                    newBoard[move[1]] = np.sign(newBoard[move[1]])*Ref.RookID
                elif flag=="PB":
                    newBoard[move[1]] = np.sign(newBoard[move[1]])*Ref.BishopID
                elif flag=="PN":
                    newBoard[move[1]] = np.sign(newBoard[move[1]])*Ref.KnightID
                            
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
#        print ("player_moves:",player_moves)
        for m in player_moves:
            if self.validate_single_move(player,m):
                valid_moves.add(m)
        return valid_moves

    def validate_single_move(self,player,move):
        
        #Can't castle through,out of, or into check
        if len(move)==3 and (move[2]=="CK" or move[2]=="CQ"):
            if player==Ref.White:
                op_moves = self.get_black_moves()
            elif player==Ref.Black:
                op_moves = self.get_white_moves()
            if move[2]=="CK":
                squares = set([(move[0],4),(move[0],5),(move[0],6),(move[0],7)])
            elif move[2]=="CQ":
                squares = set([(move[0],0),(move[0],1),(move[0],2),(move[0],3),(move[0],4)])
            if len(squares.intersection(op_moves['threatened_squares'])):
                return False
            return True
#        print ("move",move)
        tBoard,_ = self.make_move(0,move)
        if player==Ref.White:
            op_moves = tBoard.get_black_moves()
        elif player==Ref.Black:
            op_moves = tBoard.get_white_moves()
#        print (tBoard)
        king_pos = tuple(np.argwhere(tBoard.gameboard==player*Ref.KingID)[0])
        if king_pos in op_moves['threatened_squares']:
            return False
        
        return True
        
    def __eq__(self,other):
        if type(self)!=type(other):
            return False
        return np.all(self.gameboard==other.gameboard) and self.EP==other.EP and self.BC==other.BC and self.WC==other.WC
    def __neq__(self,other):
        return not(self.__eq__(other))
    def __hash__(self):
        return hash(self.gameboard.tostring())
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
        
def perft(depth,player=Ref.White,game=Chessboard()):
    if depth == 0:
        return 1
    
    numBoards = 0
    moves = game.get_valid_moves(player)
    for move in moves:
        tGame,_ = game.make_move(player,move)
        numBoards += perft(depth-1,-player,tGame)
    return numBoards
def perft2(depth,player=Ref.White,game=Chessboard()):
    perft_dict = {}
    def inner_perft(depth,player,game):
        if depth == 0:
            return 1
        elif game in perft_dict:
            return perft_dict[game]
        numBoards = 0
        moves = game.get_valid_moves(player)
        for move in moves:
            tGame,_ = game.make_move(player,move)
            numBoards += inner_perft(depth-1,-player,tGame)
        perft_dict[game] = numBoards
        return numBoards
    return inner_perft(depth,player,game)
def perft3(depth,player=Ref.White,game=Chessboard()):
    if depth == 0:
        return 1,1
    
    numBoards = 0
    numNodes = 1
    moves = game.get_valid_moves(player)
    for move in moves:
        tGame,_ = game.make_move(player,move)
        v1,v2 = perft3(depth-1,-player,tGame)
        numBoards += v1
        numNodes += v2
    return numBoards,numNodes
def perft4(depth,player=Ref.White,game=Chessboard()):
    perft_dict = {}
    def inner_perft(depth,player,game):
        if depth == 0:
            return 1,1
        elif game in perft_dict:
            return perft_dict[game]
        numBoards = 0
        numNodes = 1
        moves = game.get_valid_moves(player)
        for move in moves:
            tGame,_ = game.make_move(player,move)
            v1,v2 = inner_perft(depth-1,-player,tGame)
            numBoards += v1
            numNodes += v2   
        perft_dict[game] = numBoards,numNodes
        return perft_dict[game]
    return inner_perft(depth,player,game)

if __name__=="__main__":
#    tBoard = np.zeros((12,12),int);
#    tBoard[(3,4,3,3,5,1),(3,3,6,7,5,5)] = 6;
#    tBoard[0:2,:] = 9
#    tBoard[:,0:2] = 9
#    tBoard[:,10:12] = 9
#    tBoard[10:12,:] = 9  
#    start = (3,3)
#    print (tBoard)
#
    #Sliding Pieces
    #Test rook moves
#    b = Chessboard()
#    b.gameboard[(0,0,1),(1,2,0)] = 0
#    b.padded_board[(2,2,3),(3,4,2)] = 0
#    b.gameboard[5,3] = -4
#    b.padded_board[7,5] = -4
#    print (b)
##    print (b.padded_board)
#    moves,threats = b.get_moves_from_start((5,3))
#    print (moves)
#    moves,threats = b.get_moves_from_start((0,0))
#    print (moves)
#    print ("xxxxxxxxxxxxxxxxxxxxx")
#    #Test bishop moves
#    b = Chessboard()
#    b.gameboard[(0,0,1),(1,2,0)] = 0
#    b.padded_board[(2,2,3),(3,4,2)] = 0
#    b.gameboard[(0,5),(0,3)] = -3
#    b.padded_board[(2,7),(2,5)] = -3
#    print (b)
##    print (b.padded_board)
#    moves,threats = b.get_moves_from_start((5,3))
#    print (moves)
#    moves,threats = b.get_moves_from_start((0,0))
#    print (moves)
#    print ("xxxxxxxxxxxxxxxxxxxxx")
#    #Test queen moves
#    b = Chessboard()
#    b.gameboard[(0,0,1),(1,2,0)] = 0
#    b.padded_board[(2,2,3),(3,4,2)] = 0
#    b.gameboard[(0,5),(0,3)] = -5
#    b.padded_board[(2,7),(2,5)] = -5
#    print (b)
##    print (b.padded_board)
#    moves,threats = b.get_moves_from_start((5,3))
#    print (moves)
#    moves,threats = b.get_moves_from_start((0,0))
#    print (moves)
#    print ("xxxxxxxxxxxxxxxxxxxxx")
#    
#    #Move Map Pieces
#    #Test Knight moves
#    b = Chessboard()
#    b.gameboard[(0,0,1),(1,2,0)] = 0
#    b.padded_board[(2,2,3),(3,4,2)] = 0
#    b.gameboard[(0,5),(0,3)] = -2
#    b.padded_board[(2,7),(2,5)] = -2
#    print (b)

#    moves,threats = b.get_moves_from_start((5,3))
#    print (moves)
#    moves,threats = b.get_moves_from_start((0,0))
#    print (moves)
#    print ("xxxxxxxxxxxxxxxxxxxxx")
#    #Test King moves
#    b = Chessboard()
#    b.gameboard[(0,0,0,1),(1,2,3,0)] = 0
#    b.padded_board[(2,2,2,3),(3,4,5,2)] = 0
#    print (b)
#    moves,threats = b.get_moves_from_start((0,4))
#    print ("moves",moves)
#    print("threats",threats)
#    print ("xxxxxxxxxxxxxxxxxxxxx")
#    b = Chessboard()
    pass
#    perft(2)
#    perft2(3)
#    b = Chessboard()
#    b,_ = b.make_move(1,((6,4),(5,4)))
#    b,_ = b.make_move(-1,((1,4),(3,4)))
#    print (b)
#    print(perft(2,1,b))
    import time
    start = time.time()
    numBoards,numNodes = perft4(4)
    
    end = time.time()
    print (numBoards,"boards at specified depth")
    print (numNodes,"nodes seen")
    print (numNodes/(end-start),"nodes per second")

#import timeit
#%timeit b = Chessboard();b.get_black_moves;
#%timeit b = Chessboard();b.get_black_moves2;
