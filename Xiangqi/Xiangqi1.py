# -*- coding: utf-8 -*-
"""# -*- coding: utf-8 -*-
Created on Wed Jun 14 02:04:24 2017
1: 将
2：仕
3： 象
4：马
5：车
6：炮
7：卒

长将/不吃子  判和
@author: Jasmine
"""
import numpy as np
import time, cProfile


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

red_pieces = {R_GENERAL: 50,
              R_ADVISOR: 2,
              R_BISHOP: 2,
              R_KNIGHT: 4,
              R_ROOK: 9,
              R_CANNON: 4.5,
              R_PAWN: 1}

black_pieces = {B_GENERAL: 50,
              B_ADVISOR: 2,
              B_BISHOP: 2,
              B_KNIGHT: 4,
              B_ROOK: 9,
              B_CANNON: 4.5,
              B_PAWN: 1}

pieces_on_board = {R_GENERAL: 1,
              R_ADVISOR: 2,
              R_BISHOP: 2,
              R_KNIGHT: 2,
              R_ROOK: 2,
              R_CANNON: 2,
              R_PAWN: 5,
              B_GENERAL: 1,
              B_ADVISOR: 2,
              B_BISHOP: 2,
              B_KNIGHT: 2,
              B_ROOK: 2,
              B_CANNON: 2,
              B_PAWN: 5}


gameBoard = np.zeros((10, 9), dtype = int) 
#gameBoard = np.empty((10, 9), dtype = Str)

gameBoard[0, 0] = -5
gameBoard[0, 1] = -4
gameBoard[0, 2] = -3
gameBoard[0, 3] = -2
gameBoard[0, 4] = -1
gameBoard[9, 0] = 5
gameBoard[9, 1] = 4
gameBoard[9, 2] = 3
gameBoard[9, 3] = 2
gameBoard[9, 4] = 1
for i in range(2, 6):
    gameBoard[0, 3 + i] = -i
    gameBoard[9, 3 + i] = i

gameBoard[2, 1] = B_CANNON
gameBoard[2, 7] = B_CANNON
gameBoard[7, 1] = R_CANNON
gameBoard[7, 7] = R_CANNON

for j in range(5):
    gameBoard[3, 2*j] = B_PAWN
    gameBoard[6, 2*j] = R_PAWN

#gameBoard[gameBoard == ''] = '_'

test_b1 = np.array([[0, 0, 0, 0, -1, -2, -3, 0, 0],
                    [0, 0 ,-6, 0, -2, 0, 0, 5, 0],
                    [0, 0 ,7, 0, 0,  0, 0, 0, 0],
                    [0, 0 ,0, 0, 0, 0, 0, 0, 0],
                    [0, 0 ,4, 0, 5, 0, -3, 0, 7],
                    [0, 0 ,0, 0, 0, 0, 0, 0, 0],
                    [0, 0 ,0, 0, 0, 0, 0, 0, 0],
                    [0, 0 ,0, 0, 3, 0, 0, 0, 0],
                    [0, 0 ,0, 0, 2, 0, 0, 0, 0],
                    [0, 0 ,0, 1, 0, 2, 0, 0, 0]])


test_b2 = np.array([[0, 0, 0, -1, 0, -2, -3, 0, 0],
                    [0, 0 ,-6, 0, -2, 0, 0, 5, 0],
                    [0, 0 ,7, 0, 0,  0, 0, 0, 0],
                    [0, 0 ,0, 0, 0, 0, 0, 0, 0],
                    [0, 0 ,4, 0, 5, 0, -3, 0, 7],
                    [0, 0 ,0, 0, 0, 0, 0, 0, 0],
                    [0, 0 ,0, 0, 0, 0, 0, 0, 0],
                    [0, 0 ,-4, 0, 3, 0, 0, 0, 0],
                    [0, 0 ,0, 0, 2, 0, 0, 0, 0],
                    [0, 0 ,-7, 1, 0, 2, 0, 0, 0]])


test_b3 = np.array([[0, 0, 0, -1, 0, -2, -3, 0, 0],
                    [0, 0 ,-6, 0, -2, 0, 0, 5, 0],
                    [0, 0 ,7, 0, 0,  0, 0, 0, 0],
                    [0, 0 ,0, 0, 0, 0, 0, 0, 0],
                    [0, 0 ,5, 0, 0, 0, -3, 0, 7],
                    [0, 0 ,0, 0, 0, 0, 0, 0, 0],
                    [0, 0 ,0, 0, 0, 0, 0, 0, 0],
                    [0, 0 ,-4, 0, 0, 0, 0, 0, 0],
                    [0, 0 ,0, 0, 0, 0, 0, 0, 0],
                    [0, -5 ,0, 0, 1, 2, 3, 0, 0]])


test_b4 = np.array([[-5, 6, -3, -2, -1, -2, -3, -4, -5],
       [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
       [ 0, -6,  0,  0,  0,  0,  0, -6,  0],
       [-7,  0, -7,  0, -7,  0, -7,  0, -7],
       [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
       [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
       [ 7,  0,  7,  0,  7,  0,  7,  0,  7],
       [ 0,  0,  0,  0,  0,  0,  0,  6,  0],
       [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
       [ 5,  4,  3,  2,  1,  2,  3,  4,  5]])


test_b5 = np.array([[0,  -5, -3, -2, -1, -2, -3, -4, -5],
       [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
       [ 0, -6,  0,  0,  0,  0,  0, -6,  0],
       [-7,  0, -7,  0, -7,  0, -7,  0, -7],
       [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
       [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
       [ 7,  0,  7,  0,  7,  0,  7,  0,  7],
       [ 0,  0,  0,  0,  0,  0,  0,  6,  0],
       [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
       [ 5,  4,  3,  2,  1,  2,  3,  4,  5]])

#print(test_b4)

def move_to(gameBoard, old, new):
    temp = gameBoard[old[0], old[1]]
    if temp in pieces_on_board:
        pieces_on_board[temp] -= 1
    gameBoard[old[0], old[1]] = EMPTY
    gameBoard[new[0], new[1]] = temp

#        
def get_new_locations(gameBoard, coordinate):
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
#            print(middle)
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
#        print(rg_pos)
        if rg_pos[1]== y:
            sr = x + 1
            er = rg_pos[0]
            middle = gameBoard[sr: er, y]
#            print(middle)
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
#        print("red advisor")
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
#        print("black advisor")
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
#        
        
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
#                        print("capture")
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
#                        print("capture")
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
#                        print("capture")
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
#                        print("capture")
                        moves.append((x, i))
                        stop = True
                    elif gameBoard[i, y] * gameBoard[x, y] > 0:
                        stop = True
                    else:
                        i-= 1
            
    return moves


def get_possible_red_moves(gameBoard):
    red_moves = {}
    red_locs = np.argwhere(gameBoard > 0)
    for loc in red_locs:
        moves = get_new_locations(gameBoard, loc)
        if len(moves) > 0:
            red_moves[tuple(loc)] = moves
    return red_moves
        

def get_possible_black_moves(gameBoard):
    b_moves = {}
    b_locs = np.argwhere(gameBoard < 0)
    for loc in b_locs:
        moves = get_new_locations(gameBoard, loc)
        if len(moves) > 0:
            b_moves[tuple(loc)] = moves
    return b_moves


def if_checked_red(gameBoard):
    checked = False
    checking_pieces = []
    black_moves = get_possible_black_moves(gameBoard)
    rg_pos = tuple(np.argwhere(gameBoard == R_GENERAL)[0])
    for loc in black_moves:
        if rg_pos in black_moves[loc]:
#            print("checked by piece at", loc)
            checked = True
            checking_pieces.append(loc)
    return checked
    
def if_checked_black(gameBoard):
    checked = False
    checking_pieces = []
    red_moves = get_possible_red_moves(gameBoard)
    bg_pos = tuple(np.argwhere(gameBoard == B_GENERAL)[0])
    for loc in red_moves:
        if bg_pos in red_moves[loc]:
#            print("checked by piece at", loc)
            checked = True
            checking_pieces.append(loc)
    return checked

def get_valid_red_moves(gameBoard):
    """
    the valid moves are the ones where after making the move, checked_red is not True
    """
    valid_moves = {}
    possible_moves = get_possible_red_moves(gameBoard)
    
    for loc in possible_moves:
        v_moves = set()
        p_moves = possible_moves[loc]
        for newLoc in p_moves:
            potentialBoard = gameBoard.copy()
            move_to(potentialBoard, loc, newLoc)
            if not if_checked_red(potentialBoard):
                v_moves.add(newLoc)
#            else:
#                print("checked if move", loc, newLoc)
        if len(v_moves) > 0:
            valid_moves[loc] = v_moves

    return valid_moves

def get_valid_black_moves(gameBoard):
    valid_moves = {}
    possible_moves = get_possible_black_moves(gameBoard)
    
    for loc in possible_moves:
        v_moves = set()
        p_moves = possible_moves[loc]
        for newLoc in p_moves:
            potentialBoard = gameBoard.copy()
            move_to(potentialBoard, loc, newLoc)
            if not if_checked_black(potentialBoard):
                v_moves.add(newLoc)
        if len(v_moves) > 0:
            valid_moves[loc] = v_moves

    return valid_moves

def get_red_score(gameBoard):
    score = 0
    for x in range(10):
        for y in range(9):
            piece = gameBoard[x, y]
            if piece in red_pieces:
                score += red_pieces[piece]
    return score

def get_black_score(gameBoard):
    score = 0
    for x in range(10):
        for y in range(9):
            piece = gameBoard[x, y]
            if piece in black_pieces:
                score += black_pieces[piece]
    return score

def get_score0(gameBoard):
#    red_moves = get_valid_red_moves(gameBoard)
#    black_moves = get_valid_black_moves(gameBoard)
#    red_mobility = 0
#    b_mobility = 0
#    for red_loc in red_moves:
#        red_mobility += len(red_moves[red_loc])
#    for black_loc in black_moves:
#        b_mobility += len(black_moves[black_loc])
    #red is the maximizing player
    pieces_diff = get_red_score(gameBoard) - get_black_score(gameBoard)
#    mob_diff = red_mobility - b_mobility
    return pieces_diff

def get_score1(gameBoard):
    red_moves = get_valid_red_moves(gameBoard)
    black_moves = get_valid_black_moves(gameBoard)
    red_mobility = 0
    b_mobility = 0
    for red_loc in red_moves:
        red_mobility += len(red_moves[red_loc])
    for black_loc in black_moves:
        b_mobility += len(black_moves[black_loc])
#    red is the maximizing player
    pieces_diff = get_red_score(gameBoard) - get_black_score(gameBoard)
    mob_diff = red_mobility - b_mobility
    return pieces_diff + mob_diff

    
def get_score(gameBoard):
    score = 0
    for piece in pieces_on_board:
        if piece in red_pieces:
            score += red_pieces[piece] * pieces_on_board[piece]
#            print("added",red_pieces[piece] * pieces_on_board[piece] )
        else:
            score -= black_pieces[piece] * pieces_on_board[piece]
#            print("subtracted", black_pieces[piece] * pieces_on_board[piece])
    return score
    

def red_move(gameBoard):
    moves = get_valid_red_moves(gameBoard)
    best_move = ()
    if len(moves) == 0:
        return best_move
    best_score = - float('inf')
    for loc in moves:
        p_new_locations = moves[loc]
        for new_loc in p_new_locations:
            p_board = gameBoard.copy()
            move_to(p_board, loc, new_loc)
            red_score = get_red_score(p_board)
            black_score = get_black_score(p_board)
            score = red_score - black_score
            if score >= best_score:
                best_move = (loc, new_loc)
                best_score = score
                
    return best_move

    
    
    
#    else:
#        move_to(gameBoard, )

def black_move(gameBoard):
    moves = get_valid_black_moves(gameBoard)
    best_move = ()
    if len(moves) == 0:
        return best_move
    best_score = - float('inf')
    for loc in moves:
        p_new_locations = moves[loc]
        for new_loc in p_new_locations:
            p_board = gameBoard.copy()
            move_to(p_board, loc, new_loc)
            red_score = get_red_score(p_board)
            black_score = get_black_score(p_board)
            score = black_score - red_score
            if score > best_score:
                best_move = (loc, new_loc)
                best_score = score
                
    return best_move
#while not gameEnd:
#    print(gameBoard)


def red_move_minimax(gameBoard):
    moves = get_valid_red_moves(gameBoard)
    if len(moves) == 0:
        return ()
    best_move = ()
    best_score = - float('inf')
    for loc in moves:
        p_new_locs = moves[loc] #potential new locations
        for new_loc in p_new_locs:
            p_board = gameBoard.copy()
            move_to(p_board, loc, new_loc)
#            if loc == (7,1) and new_loc == (0,1):
#                    print(p_board)
            best_reply = black_move(p_board)
            if best_reply == ():
                # red wins if this move is made
                return (loc, new_loc)
            else:
                
                move_to(p_board, best_reply[0], best_reply[1])
                redS = get_red_score(p_board)
                blackS = get_black_score(p_board)
                score = redS - blackS
                print("if red move", loc, new_loc)
                print("then black move", best_reply)
                print("score is", score)
                if score > best_score:
                    best_score = score
                    best_move = (loc, new_loc)
    return best_move
    
def black_move_minimax(gameBoard):
    moves = get_valid_black_moves(gameBoard)
    if len(moves) == 0:
        return ()
    best_move = ()
    best_score = - float('inf')
    for loc in moves:
        p_new_locs = moves[loc]
        for new_loc in p_new_locs:
            p_board = gameBoard.copy()
            move_to(p_board, loc, new_loc)
            best_reply = red_move(p_board)
            if best_reply == ():
                # black wins if this move is made
                return (loc, new_loc)
            else:
                move_to(p_board, best_reply[0], best_reply[1])
                redS = get_red_score(p_board)
                blackS = get_black_score(p_board)
                score = blackS - redS
                if score >= best_score:
                    best_score = score
                    best_move = (loc, new_loc)
    return best_move
    
    
    

valid_moves_black = {}
valid_moves_red = {}
def minimax(gameBoard, depth, player):
    if depth == 0:
        return (), get_score(gameBoard)
    elif player == 'red':
        
        if len(valid_moves_red) == 0 or gameBoard.tostring() not in valid_moves_red:
            moves =  get_valid_red_moves(gameBoard)
            valid_moves_red[gameBoard.tostring()] = moves
        else:
            moves = valid_moves_red[gameBoard.tostring()]
            print("took from dictionary")
        best_move = ()
        best_score = - float('inf')
        if len(moves) == 0:
            return best_move, best_score
        else:
#            board = gameBoard.copy()
            for loc in moves:
                p_new_locs = moves[loc]
                for new_loc in p_new_locs:
                    p_board = gameBoard.copy()
                    move_to(p_board, loc, new_loc)
                    best_reply, score = minimax(p_board, depth -1, 'black')
                    if score > best_score:
#                        print("if red move", loc, new_loc, 'black move', best_reply)
                        best_score = score
                        best_move = (loc, new_loc)
            return best_move, best_score            
    elif player == 'black':
        if len(valid_moves_black) == 0 or gameBoard.tostring() not in valid_moves_black:
            moves = get_valid_black_moves(gameBoard)
            valid_moves_black[gameBoard.tostring()] = moves
        else:
             moves = valid_moves_black[gameBoard.tostring()]
#             print("took from dictionary")
        best_move = ()
        best_score = float('inf')
        if len(moves)== 0:
            return best_move, best_score
        else:
            for loc in moves:
                p_new_locs = moves[loc]
                for new_loc in p_new_locs:
                    p_board = gameBoard.copy()
                    move_to(p_board, loc, new_loc)
                    best_reply, score = minimax(p_board, depth -1, 'red')
                    if score < best_score:
#                        print("if black move", loc, new_loc, 'red move', best_reply)
                        best_score = score
                        best_move = (loc, new_loc)
            return best_move, best_score
            
            
def minimax_old(gameBoard, depth, player):
    if depth == 0:
        return (), get_score(gameBoard)
    elif player == 'red':
#        if gameBoard.tostring() in valid_moves_red:
#            moves = valid_moves_red[gameBoard.tostring()]
#        else:
        moves =  get_valid_red_moves(gameBoard)
#            valid_moves_red[gameBoard.tostring()] = moves
        best_move = ()
        best_score = - float('inf')
        if len(moves) == 0:
            return best_move, best_score
        else:
#            board = gameBoard.copy()
            for loc in moves:
                p_new_locs = moves[loc]
                for new_loc in p_new_locs:
                    p_board = gameBoard.copy()
                    move_to(p_board, loc, new_loc)
                    best_reply, score = minimax_old(p_board, depth -1, 'black')
                    if score > best_score:
#                        print("if red move", loc, new_loc, 'black move', best_reply)
                        best_score = score
                        best_move = (loc, new_loc)
#                        board = p_board.copy()
#            print(board)
            return best_move, best_score
    elif player == 'black':
#        if gameBoard.tostring() in valid_moves_black:
#            moves = valid_moves_black[gameBoard.tostring()]
#        else:
        moves = get_valid_black_moves(gameBoard)
#            valid_moves_black[gameBoard.tostring()] = moves
        best_move = ()
        best_score = float('inf')
        if len(moves)== 0:
            return best_move, best_score
        else:
            for loc in moves:
                p_new_locs = moves[loc]
                for new_loc in p_new_locs:
                    
                    p_board = gameBoard.copy()
                    move_to(p_board, loc, new_loc)
                    best_reply, score = minimax_old(p_board, depth -1, 'red')
                    if score < best_score:
#                        print("if black move", loc, new_loc, 'red move', best_reply)
                        best_score = score
                        best_move = (loc, new_loc)
            return best_move, best_score

def alpha_beta(gameBoard, depth, player, alpha, beta):
    if depth == 0:
        return (), get_score1(gameBoard)
    elif player == 'red':
        moves = get_valid_red_moves(gameBoard)
        if moves == ():
            return (), -float('inf')
        else:
            b_move = ()
            for loc in moves:
                p_new_locs = moves[loc]
                for new_loc in p_new_locs:
                    p_board = gameBoard.copy()
                    move_to(p_board, loc, new_loc)
                    move, score = alpha_beta(p_board, depth -1, 'black', alpha, beta)
                    if score >= beta:
                        return (loc, new_loc), beta
                    if score > alpha:
                        alpha = score
                        b_move = (loc, new_loc)
            return b_move, alpha
    elif player == 'black':
        moves = get_valid_black_moves(gameBoard)
        if moves == ():
            return (), float('inf')
        else:
            b_move = ()
            for loc in moves:
                p_new_locs = moves[loc]
                for new_loc in p_new_locs:
                    p_board = gameBoard.copy()
                    move_to(p_board, loc, new_loc)
                    move, score = alpha_beta(p_board, depth -1, 'red', alpha, beta)
                    if score <= alpha:
                        return (loc, new_loc), alpha
                    if score < beta:
                        beta = score
                        b_move = (loc, new_loc)
            return b_move, beta
            

if __name__=="__main__":
    startT = time.time()
    #best_red_move, score = alpha_beta(gameBoard, 3, 'red', -float('inf'), float('inf'))
    cProfile.run("best_red_move, score = alpha_beta(gameBoard, 3, 'red', -float('inf'), float('inf'))")
    endT1 = time.time()
    #best_red_move1 = minimax_old(gameBoard, 3, 'red')
    #endT2 = time.time()
    
    print(best_red_move, score)
    print("t1:", endT1 - startT)
    #print("t2:", endT2 - endT1)

###playing game
#gameEnd = False
#num_moves = 0
#while not gameEnd:
#    print(gameBoard)
#    if num_moves % 2 == 0:
#        text = input("red move next, continue?")
#        move, score = minimax_old(gameBoard, 3, 'red')
#        print(score)
#        if move == ():
#            print("red Loss")
#            gameEnd = True
#    else:
#        text = input("black move next, continue?")
##        move, score = minimax(gameBoard, 3, 'black')
#        if text == 'e':
#            move = (0,0)
#        coordinates = text.split(',')
#        if len(coordinates) == 1:
#            move = ()
#        else:
#            
#            start =(int(coordinates[0]), int(coordinates[1]))
#            end = (int(coordinates[2]), int(coordinates[3]))
#            move = (start, end)
#        if move == ():
#            print("black loss")
#            gameEnd = True
#    if text == 'e':
#        print("user exit game")
#        gameEnd = True
#    elif move == ():
#        print("game ended after", num_moves, "moves")
#    else:
#        print(move)
#        move_to(gameBoard, move[0], move[1])
#        num_moves += 1
#

"""
- changed valid moves from list to set. Shaved off 3 seconds.
- added if __name__=="__main__": so code won't be run when called from another file
"""