# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 22:47:02 2017

@author: jasmine
@author: arinz
"""
import numpy as np
import matplotlib.pyplot as plt
import time
import pickle as pkl
import operator
import cProfile

R_GENERAL= 1
R_ADVISOR = 2
R_BISHOP = 3
R_KNIGHT = 4
R_ROOK = 5
R_CANNON = 6
R_PAWN = 7
B_GENERAL= -1
B_ADVISOR = -2
B_BISHOP = -3
B_KNIGHT = -4
B_ROOK = -5
B_CANNON = -6
B_PAWN = -7
EMPTY = 0

class Xiangqi:
    def __init__(self,gameBoard=None):

        if gameBoard is None:
            self.gameBoard = np.zeros((10, 9), dtype = int)
            self.gameBoard[0, 0] = B_ROOK
            self.gameBoard[0, 1] = B_KNIGHT
            self.gameBoard[0, 2] = B_BISHOP
            self.gameBoard[0, 3] = B_ADVISOR
            self.gameBoard[0, 4] = B_GENERAL
            self.gameBoard[9, 0] = R_ROOK
            self.gameBoard[9, 1] = R_KNIGHT
            self.gameBoard[9, 2] = R_BISHOP
            self.gameBoard[9, 3] = R_ADVISOR
            self.gameBoard[9, 4] = R_GENERAL
            for i in range(2, 6):
                self.gameBoard[0, 3 + i] = -i
                self.gameBoard[9, 3 + i] = i
            
            self.gameBoard[2, 1] = B_CANNON
            self.gameBoard[2, 7] = B_CANNON
            self.gameBoard[7, 1] = R_CANNON
            self.gameBoard[7, 7] = R_CANNON
            
            for j in range(5):
                self.gameBoard[3, 2*j] = B_PAWN
                self.gameBoard[6, 2*j] = R_PAWN
        else:
            self.gameBoard = gameBoard
            
    def __hash__(self):
        return hash(self.gameBoard.tostring())

    def __eq__(self,other):
        if type(other)!=type(self):
            return False
        return np.all(self.gameBoard==other.gameBoard)
    def __neq__(self,other):
        return not(self.__eq__(other))
    
    def __str__(self):
        output = ""
        
        for i in range(10):
            for j in range(9):
                toAdd = str(int(self.gameBoard[i,j]))
                if len(toAdd)==1:
                    toAdd = " " + toAdd
                toAdd += " "
                output += toAdd
            output += "\n"
        return output
        
    def get_new_locations(self,gameBoard, coordinate):
        x = coordinate[0]
        y = coordinate[1]
        moves = []
        if gameBoard[x, y] ==  EMPTY:
            pass
        
        elif gameBoard[x, y] == R_PAWN: # red pawn
            if x -1 >= 0 and gameBoard[x -1, y] <= 0:
                moves.append((x-1, y))
            if x <= 4:
                if y-1 >=0 and gameBoard[x, y-1] <=0:
                    moves.append((x, y-1))
                if y+1 <= 8 and gameBoard[x , y+1] <= 0:
                    moves.append((x, y+1))
    
        elif gameBoard[x, y] == B_PAWN: # black pawn
            if x+1 <= 9 and gameBoard[x + 1, y] >=0:
                moves.append((x +1, y))
            if x >= 5:
                if y + 1 <= 8 and gameBoard[x, y +1] >= 0:
                    moves.append((x, y+1))
                if y -1 >= 0 and gameBoard[x, y- 1] >=0:
                    moves.append((x, y-1))
                
        elif gameBoard[x, y] == R_GENERAL:
            # generals cannot face each other
            bg_pos = np.argwhere(gameBoard == B_GENERAL)[0]
            if bg_pos[1]== y:
                sr = bg_pos[0] + 1
                er = x
                middle = gameBoard[sr: er, y]
                n_zero_pos = np.argwhere(middle != 0)
                if len(n_zero_pos) == 0:
                    moves.append(tuple(bg_pos))
            if x-1 >= 7 and gameBoard[x - 1, y] <= 0:
                moves.append((x-1, y))
            if x+1 <= 9 and gameBoard[x + 1, y] <= 0:
                moves.append((x+1, y))
            if y - 1 >= 3 and gameBoard[x, y - 1] <= 0:
                moves.append((x, y-1))
            if y + 1 <= 5 and gameBoard[x, y + 1] <= 0:
                moves.append((x, y + 1))
        
        elif gameBoard[x, y] == B_GENERAL:
    
            rg_pos = np.argwhere(gameBoard == R_GENERAL)[0]
            if rg_pos[1]== y:
                sr = x + 1
                er = rg_pos[0]
                middle = gameBoard[sr: er, y]
                n_zero_pos = np.argwhere(middle != 0)
                if len(n_zero_pos) == 0:
                    moves.append(tuple(rg_pos))
                    
            if gameBoard[x - 1, y] >= 0 and x-1 >= 0:
                moves.append((x-1, y))
            if gameBoard[x + 1, y] >= 0 and x+1 <= 2:
                moves.append((x+1, y))
            if gameBoard[x, y - 1] >= 0 and y - 1 >= 3:
                moves.append((x, y-1))
            if gameBoard[x, y + 1] >= 0 and y + 1 <= 5:
                moves.append((x, y + 1))
        
        elif gameBoard[x, y] == R_ADVISOR:
            if x == 9 or x == 7:
                if gameBoard[8, 4] <= 0:
                    moves.append((8, 4))
            elif x == 8:
                if gameBoard[7, 3] <= 0:
                    moves.append((7,3))
                if gameBoard[7, 5] <= 0:
                    moves.append((7, 5))
                if gameBoard[9, 3] <= 0:
                    moves.append((9, 3))
                if gameBoard[9, 5] <= 0:
                    moves.append((9, 5))
                    
        elif gameBoard[x, y] == B_ADVISOR:
            if x == 0 or x == 2:
                if gameBoard[1, 4] >= 0:
                    moves.append((1, 4))
            elif x == 1:
                if gameBoard[0, 3] >= 0:
                    moves.append((0,3))
                if gameBoard[0, 5] >= 0:
                    moves.append((0, 5))
                if gameBoard[2, 3] >= 0:
                    moves.append((2, 3))
                if gameBoard[2, 5] >= 0:
                    moves.append((2, 5))
        
        elif gameBoard[x, y] == R_BISHOP:
            if x- 1 > 5 and y-1 > 0 and gameBoard[x -1, y-1] == 0 and gameBoard[x -2, y -2] <= 0:
                moves.append((x-2, y-2))
            if x -1 > 5 and y+1 < 8 and gameBoard[x-1, y+1] == 0 and gameBoard[x-2, y + 2] <=0:
                moves.append((x-2, y+2))
            if x +1 < 9 and y-1 > 0 and gameBoard[x+1, y-1] == 0 and gameBoard[x+2, y - 2] <=0:
                moves.append((x+2, y-2))
            if x +1 < 9 and y+1 < 8 and gameBoard[x+1, y+1] == 0 and gameBoard[x+2, y + 2] <=0:
                moves.append((x+2, y+2))
        
        elif gameBoard[x, y] == B_BISHOP:
            if x- 1 > 0 and y-1 > 0 and gameBoard[x -1, y-1] == 0 and gameBoard[x -2, y -2] >= 0:
                moves.append((x-2, y-2))
            if x -1 > 0 and y+1 < 8 and gameBoard[x-1, y+1] == 0 and gameBoard[x-2, y + 2] >=0:
                moves.append((x-2, y+2))
            if x +1 < 4 and y-1 > 0 and gameBoard[x+1, y-1] == 0 and gameBoard[x+2, y - 2] >=0:
                moves.append((x+2, y-2))
            if x +1 < 4 and y+1 < 8 and gameBoard[x+1, y+1] == 0 and gameBoard[x+2, y + 2] >=0:
                moves.append((x+2, y+2))
                
        elif abs(gameBoard[x, y]) == R_KNIGHT:
            if y > 1 and gameBoard[x, y -1] == 0:
                if x + 1 <= 9 and gameBoard[x + 1, y -2]*gameBoard[x, y] <= 0:
                    moves.append((x+1, y- 2))
                if x - 1 >= 0 and gameBoard[x - 1, y -2]*gameBoard[x, y] <= 0:
                    moves.append((x-1, y -2))
            if y < 7 and gameBoard[x, y +1] == 0:
                if x + 1 <= 9 and gameBoard[x + 1, y +2]*gameBoard[x, y] <= 0:
                    moves.append((x+1, y+ 2))
                if x-1 >= 0 and gameBoard[x - 1, y +2]*gameBoard[x, y] <= 0:
                    moves.append((x-1, y +2))
            if x > 1 and gameBoard[x-1, y]== 0:
                if y - 1 >= 0 and gameBoard[x -2, y -1]*gameBoard[x, y] <= 0:
                    moves.append((x-2, y- 1))
                if y + 1 <= 8 and gameBoard[x - 2, y +1]*gameBoard[x, y] <= 0:
                    moves.append((x-2, y + 1))
            if x < 8 and gameBoard[x +1, y] == 0:
                if y - 1 >= 0 and gameBoard[x +2, y -1]*gameBoard[x, y] <= 0:
                    moves.append((x+2, y- 1))
                if y + 1 <= 8 and gameBoard[x +2, y +1]*gameBoard[x, y] <= 0:
                    moves.append((x+2, y + 1))
            
        elif abs(gameBoard[x, y])== R_ROOK:
            i = x + 1
            stop = False
            while i <= 9 and not stop:
                if gameBoard[i, y] == 0:
                    moves.append((i, y))
                    i += 1
                elif gameBoard[i, y]*gameBoard[x, y] > 0:
                    stop = True
                elif gameBoard[i, y]*gameBoard[x, y] < 0:
                    stop = True
                    moves.append((i, y))
            i = x - 1
            stop = False
            while i >= 0 and not stop:
                if gameBoard[i, y] == 0:
                    moves.append((i, y))
                    i -= 1
                elif gameBoard[i, y]*gameBoard[x, y] > 0:
                    stop = True
                elif gameBoard[i, y]*gameBoard[x, y] < 0:
                    stop = True
                    moves.append((i, y))
            i = y + 1
            stop = False
            while i <= 8 and not stop:
                if gameBoard[x, i] == 0:
                    moves.append((x, i))
                    i += 1
                elif gameBoard[x, i]*gameBoard[x, y] > 0:
                    stop = True
                elif gameBoard[x, i]*gameBoard[x, y] < 0:
                    stop = True
                    moves.append((x, i))
            i = y - 1
            stop = False
            while i >= 0 and not stop:
                if gameBoard[x, i] == 0:
                    moves.append((x, i))
                    i -= 1
                elif gameBoard[x, i]*gameBoard[x, y] > 0:
                    stop = True
                elif gameBoard[x, i]*gameBoard[x, y] < 0:
                    stop = True
                    moves.append((x, i))   
            
        elif abs(gameBoard[x, y])== R_CANNON:
            i = x + 1
            stop = False
            pivot_found = False
            while i <= 9 and not stop:
                if gameBoard[i, y] == 0 and not pivot_found:
                    moves.append((i, y))
                    i += 1
                else:
                    if not pivot_found:
                        pivot_found = True
                        i += 1
                    else:
                        if gameBoard[i, y] * gameBoard[x, y] < 0:
                            moves.append((i, y))
                            stop = True
                        elif gameBoard[i, y] * gameBoard[x, y] > 0:
                            stop = True
                        else:
                            i += 1
            i = x - 1
            stop = False
            pivot_found = False
            while i >= 0 and not stop:
                if gameBoard[i, y] == 0 and not pivot_found:
                    moves.append((i, y))
                    i -= 1
                else:
                    if not pivot_found:
                        pivot_found = True
                        i -= 1
                    else:
                        if gameBoard[i, y] * gameBoard[x, y] < 0:
                            moves.append((i, y))
                            stop = True
                        elif gameBoard[i, y] * gameBoard[x, y] > 0:
                            stop = True
                        else:
                            i -= 1
            i = y + 1
            stop = False
            pivot_found = False
            while i <= 8 and not stop:
                if gameBoard[x, i] == 0 and not pivot_found:
                    moves.append((x, i))
                    i += 1
                else:
                    if not pivot_found:
                        pivot_found = True
                        i += 1
                    else:
                        if gameBoard[x, i] * gameBoard[x, y] < 0:
                            moves.append((x, i))
                            stop = True
                        elif gameBoard[i, y] * gameBoard[x, y] > 0:
                            stop = True
                        else:
                            i += 1
            i = y - 1
            stop = False
            pivot_found = False
            while i >= 0 and not stop:
                if gameBoard[x, i] == 0 and not pivot_found:
                    moves.append((x, i))
                    i -= 1
                else:
                    if not pivot_found:
                        pivot_found = True
                        i -= 1
                    else:
                        if gameBoard[x, i] * gameBoard[x, y] < 0:
                            moves.append((x, i))
                            stop = True
                        elif gameBoard[i, y] * gameBoard[x, y] > 0:
                            stop = True
                        else:
                            i-= 1
                
        return moves
    
    def get_possible_red_moves(self,gameBoard):
        red_moves = {}
        red_locs = np.argwhere(gameBoard > 0)
        for loc in red_locs:
            moves = self.get_new_locations(gameBoard, loc)
            if len(moves) > 0:
                red_moves[tuple(loc)] = moves
        return red_moves
            
    
    def get_possible_black_moves(self,gameBoard):
        b_moves = {}
        b_locs = np.argwhere(gameBoard < 0)
        for loc in b_locs:
            moves = self.get_new_locations(gameBoard, loc)
            if len(moves) > 0:
                b_moves[tuple(loc)] = moves
        return b_moves
    
    
    def if_checked_red(self,gameBoard):
        checked = False
        checking_pieces = []
        black_moves = self.get_possible_black_moves(gameBoard)
        rg_pos = tuple(np.argwhere(gameBoard == R_GENERAL)[0])
        for loc in black_moves:
            if rg_pos in black_moves[loc]:
                checked = True
                checking_pieces.append(loc)
        return checked
        
    def if_checked_black(self,gameBoard):
        checked = False
        checking_pieces = []
        red_moves = self.get_possible_red_moves(gameBoard)
        bg_pos = tuple(np.argwhere(gameBoard == B_GENERAL)[0])
        for loc in red_moves:
            if bg_pos in red_moves[loc]:
                checked = True
                checking_pieces.append(loc)
        return checked
    
    def get_valid_red_moves(self):
        """
        the valid moves are the ones where after making the move, checked_red is not True
        """
        valid_moves = {}
        possible_moves = self.get_possible_red_moves(self.gameBoard)
        
        for loc in possible_moves:
            v_moves = set()
            p_moves = possible_moves[loc]
            for newLoc in p_moves:
                potentialBoard = self.gameBoard.copy()
                self.move_to(potentialBoard, loc, newLoc)
                if not self.if_checked_red(potentialBoard):
                    v_moves.add(newLoc)
            if len(v_moves) > 0:
                valid_moves[loc] = v_moves
    
        return valid_moves
    
    def get_valid_black_moves(self):
        valid_moves = {}
        possible_moves = self.get_possible_black_moves(self.gameBoard)
        
        for loc in possible_moves:
            v_moves = set()
            p_moves = possible_moves[loc]
            for newLoc in p_moves:
                potentialBoard = self.gameBoard.copy()
                self.move_to(potentialBoard, loc, newLoc)
                if not self.if_checked_black(potentialBoard):
                    v_moves.add(newLoc)
            if len(v_moves) > 0:
                valid_moves[loc] = v_moves
    
        return valid_moves
    
    def move_to(self,gameBoard, old, new):
        gameBoard[old],gameBoard[new] = EMPTY,gameBoard[old]

    def make_move(self,old,new):
        copyBoard = self.gameBoard.copy()
        self.move_to(copyBoard,old,new)
        return Xiangqi(copyBoard)
    
