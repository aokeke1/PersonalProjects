# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 11:08:21 2017

@author: aokeke
"""
import numpy as np
import References as Ref
import time
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
                           
            self.EP = EP #tuple that says what square can be taken by en passant
            self.WC = WC #white castle rights as a binary second bit is left first bit is right
            self.BC = BC #black castle rights as a binary second bit is left first bit is right
        elif type(gameboard)==str:
            #Make gameboard from FEN
            fields = gameboard.split(" ")
            #Castling Rights
            self.BC = 0
            self.WC = 0
            self.EP = None
#            print (fields[2])
            if "K" in fields[2]:
                self.WC |= 1
            if "k" in fields[2]:
                self.BC |= 1
            if "Q" in fields[2]:
                self.WC |= 2
            if "q" in fields[2]:
                self.BC |= 2
            #En Passant Rights
            if fields[3]!="-":
                cols = "abcdefgh"
                rows = "87654321"
                self.EP = (rows.find(fields[3][1]),cols.find(fields[3][0]))
            self.gameboard = np.zeros((8,8),dtype=int)
            currPos = (0,0)
            for char in fields[0]:
#                print (char)
#                print (currPos)
                if char=="/":
                    currPos = (currPos[0]+1,0)
                elif str.isnumeric(char):
                    currPos = (currPos[0],currPos[1]+int(char))
                else:
                    if str.isupper(char):
                        player = Ref.White
                    else:
                        player = Ref.Black
                    pieceType = char.lower()
                    if pieceType=="k":
                        piece = 6
                    elif pieceType=="q":
                        piece = 5
                    elif pieceType=="r":
                        piece = 4
                    elif pieceType=="b":
                        piece = 3
                    elif pieceType=="n":
                        piece = 2
                    elif pieceType=="p":
                        piece = 1
                    self.gameboard[currPos] = player*piece
                    currPos = (currPos[0],currPos[1]+1)
            
            
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
                if obj_coord[0]<=9 and obj_coord[1]<=9 and np.sign(self.padded_board[obj_coord])!=np.sign(self.padded_board[pad_start]):
                    move_array[obj_coord] = 1
                #decreasing direction
                relIndOfFirstObj = curr_pos - np.argwhere(self.padded_board.diagonal(offset=diag_offset)[:curr_pos]!=0)[-1][0]
                move_array[range(pad_start[0]-relIndOfFirstObj+1,pad_start[0]),\
                           range(pad_start[1]-relIndOfFirstObj+1,pad_start[1])] = 1
                obj_coord = (pad_start[0]-relIndOfFirstObj,pad_start[1]-relIndOfFirstObj)
                if obj_coord[0]>=2 and obj_coord[1]>=2 and np.sign(self.padded_board[obj_coord])!=np.sign(self.padded_board[pad_start]):
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
                if obj_coord[0]<=9 and obj_coord[1]<=9 and np.sign(flip_padded_board[obj_coord])!=np.sign(flip_padded_board[pad_start]):
                    move_array[obj_coord] = 1
                #decreasing direction
                relIndOfFirstObj = curr_pos - np.argwhere(flip_padded_board.diagonal(offset=diag_offset)[:curr_pos]!=0)[-1][0]
                move_array[range(pad_start[0]-relIndOfFirstObj+1,pad_start[0]),\
                           range(pad_start[1]-relIndOfFirstObj+1,pad_start[1])] = 1
                obj_coord = (pad_start[0]-relIndOfFirstObj,pad_start[1]-relIndOfFirstObj)
                if obj_coord[0]>=2 and obj_coord[1]>=2 and np.sign(flip_padded_board[obj_coord])!=np.sign(flip_padded_board[pad_start]):
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
                    
                else:
                    move_array[new_row+2,start[1]+1] = 1
                
            #Capture Right
            if start[1]<7 and np.sign(self.gameboard[new_row,start[1]+1])==-player:
                if new_row==0 or new_row==7:
                    extra_moves.add((start,(new_row,start[1]+1),"PQ"))
                    extra_moves.add((start,(new_row,start[1]+1),"PR"))
                    extra_moves.add((start,(new_row,start[1]+1),"PB"))
                    extra_moves.add((start,(new_row,start[1]+1),"PN"))
                else:
                    move_array[new_row+2,start[1]+3] = 1
            threatened.add((new_row,start[1]-1))
            threatened.add((new_row,start[1]+1))    
            #Double Move Forward
            if ((start[0]==1 and player==Ref.Black) or (start[0]==6 and player==Ref.White)) and self.gameboard[new_row2,start[1]]==0 and self.gameboard[new_row,start[1]]==0:
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
                flag = move[2]
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
#            print ("move:",move)
            if player==Ref.White:
                op_moves = self.get_black_moves()
            elif player==Ref.Black:
                op_moves = self.get_white_moves()
            if move[2]=="CK":
                squares = set([(move[0][0],4),(move[0][0],5),(move[0][0],6)]) #,(move[0][0],7)
            elif move[2]=="CQ":
                squares = set([(move[0][0],2),(move[0][0],3),(move[0][0],4)]) #(move[0][0],0),(move[0][0],1),
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
        board[np.where(self.gameboard==0)] = "."
        return str(board)
    def __repr__(self):
        return "\n"+self.__str__()+"\n"
        
def perft(depth,player=Ref.White,game=Chessboard(),should_print=True):
    perft_dict = {}
    def inner_perft(depth,player,game):
#        print (game,player)
        if depth == 0:
            return 1,1
        elif (game,depth) in perft_dict:
            return perft_dict[(game,depth)]
        numBoards = 0
        numNodes = 1
        moves = game.get_valid_moves(player)
        if len(moves)==0:
            return 0,1
        for move in moves:
            tGame,_ = game.make_move(player,move)
            v1,v2 = inner_perft(depth-1,-player,tGame)
            numBoards += v1
            numNodes += v2   
        perft_dict[(game,depth)] = numBoards,numNodes
        return perft_dict[(game,depth)]
    start = time.time()
    numBoards,numNodes = inner_perft(depth,player,game)
    end = time.time()
    if should_print:
        print (numBoards,"boards at depth",depth)
        print (numNodes,"nodes seen")
        print (numNodes/(end-start),"nodes per second")
        print (numBoards/(end-start),"boards per second")
        print ("This took",(end-start)//60,"min",(end-start)%60,"sec")
    return numBoards,numNodes

def divide(depth,player=Ref.White,game=Chessboard(),should_print=True):
    start = time.time()
    numBoards = 0
    numNodes = 1
    moves = game.get_valid_moves(player)
    cols = "abcdefgh"
    rows = "87654321"
#    print (moves)
    i=0
    for move in moves:
        
        tGame,_ = game.make_move(player,move)
        v1,v2 = perft(depth-1,-player,tGame,should_print=False)
        tMoveName = cols[move[0][1]] + rows[move[0][0]] + cols[move[1][1]] + rows[move[1][0]]
        if len(move)==3:
            tMoveName += move[2][1]
        print (tMoveName,":",v1)
        if i==0:
            i+=1
        numBoards += v1
        numNodes += v2
        
    end = time.time()
    if should_print:
        print (numBoards,"boards at depth",depth)
        print (numNodes,"nodes seen")
        print (numNodes/(end-start),"nodes per second")
        print ("This took",(end-start)//60,"min",(end-start)%60,"sec")
    return numBoards,numNodes
def test():
    inputStr = "1k6/1b6/8/8/7R/8/8/4K2R b K - 0 1; perft 5 = 1063513"
    test_single(inputStr)
    inputStr = "3k4/3p4/8/K1P4r/8/8/8/8 b - - 0 1; perft 6 = 1134888"
    test_single(inputStr)
    inputStr = "8/8/4k3/8/2p5/8/B2P2K1/8 w - - 0 1; perft 6 = 1015133"
    test_single(inputStr)
    inputStr = "8/8/1k6/2b5/2pP4/8/5K2/8 b - d3 0 1; perft 6 = 1440467"
    test_single(inputStr)
    inputStr = "5k2/8/8/8/8/8/8/4K2R w K - 0 1; perft 6 = 661072"
    test_single(inputStr)
    inputStr = "3k4/8/8/8/8/8/8/R3K3 w Q - 0 1; perft 6 = 803711"
    test_single(inputStr)
    inputStr = "4k3/1P6/8/8/8/8/K7/8 w - - 0 1; perft 6 = 217342"
    test_single(inputStr)
    inputStr = "8/P1k5/K7/8/8/8/8/8 w - - 0 1; perft 6 = 92683"
    test_single(inputStr)
    inputStr = "8/k1P5/8/1K6/8/8/8/8 w - - 0 1; perft 7 = 567584"
    test_single(inputStr)
    inputStr = "K1k5/8/P7/8/8/8/8/8 w - - 0 1; perft 6 = 2217"
    test_single(inputStr)
    inputStr = "8/8/2k5/5q2/5n2/8/5K2/8 b - - 0 1; perft 4 = 23527"
    test_single(inputStr)
    
def test_single(inputStr):
    fields = inputStr.split(";")
    fen = fields[0]
    player = 1
    if fen.split(" ")[1]!="w":
        player = -player
    fields2 = fields[1].split(" ")
    expectedNumMoves = int(fields2[4])
    depth = int(fields2[2])
    
    b = Chessboard(fen)
    print (fen)
    print (b)
    numBoards,numNodes = perft(depth,player,b,True)
    if numBoards!=expectedNumMoves:
        print ("Failed")
        print ("Expected:",expectedNumMoves,"Got:",numBoards)
        numBoards,numNodes = divide(depth,player,b)
    else:
        print ("Passed")
    print ("---------------------------",flush=True)
    
if __name__=="__main__":

    pass
#    perft(2)
#    perft2(3)
#    b = Chessboard()
#    b,_ = b.make_move(1,((6,4),(5,4)))
#    b,_ = b.make_move(-1,((1,4),(3,4)))
#    print (b)
#    print(perft(2,1,b))
    
#    numBoards,numNodes = perft(2)
#    numBoards,numNodes = divide(3)
#    print ("--------------------------")
#    b = Chessboard()
#    b,_ = b.make_move(1,((7,6),(5,5)))
#    b,_ = b.make_move(-1,((1,1),(2,1)))
#    print (b)
#    divide(1,1,b)
#    fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"
#    b = Chessboard(fen)
#    print (b)
#    print (b.EP)
#    print (b.WC)
#    print (b.BC)
    test()
#    b = Chessboard("1k6/1b6/8/8/7R/8/8/4K2R b K - 0 1")
#    b,_ = b.make_move(-1,((1,1),(2,0)))
#    print (b)
#    divide(4,1,b)
#    b,_ = b.make_move(1,((4,7),(3,7)))
#    print (b)
#    divide(3,-1,b)
#    b,_ = b.make_move(-1,((2,0),(1,1)))
#    print (b)
#    divide(2,1,b)
#import timeit
#%timeit b = Chessboard();b.get_black_moves;
#%timeit b = Chessboard();b.get_black_moves2;
