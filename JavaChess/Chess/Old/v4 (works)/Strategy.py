# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 09:17:35 2016

@author: arinz
"""
import random, copy, ChessBoard, Pieces

def threeMoveRep(history, myBoard):
    """
        Returns true if this board arrangement has been encountered three or
        or more times in the given history
    """
    if history.count(myBoard)>=3:
        return True
    return False

def twoMoveRep(history, myBoard):
    """
        Returns true if this board arrangement has been encountered two or
        or more times in the given history
    """
    if history.count(myBoard)>=2:
        return True
    return False
    
def oneMoveRep(history, myBoard):
    """
        Returns true if this board arrangement has been encountered one or
        or more times in the given history
    """
    if myBoard in history:
        return True
    return False

def checkForMate(color,myBoard,piecesThatCanMove):
    """
        takes in a color, board, and the pieces of the color that can move.
        checks each of the possible moves to see if any of them will result in a
        checkmate. Returns tuple of three values. (False,None,None) if no moves
        can give checkmate. (True,start,end) if a move can give mate. Where start
        is the position of the piece to move and end is the place to move that piece
    """
    for piece in piecesThatCanMove:
        start = piece.getPosition()
        if color.lower()=='white':
            #find the moves
            allMoves = myBoard.checkWhitePossibleMoves(start,shouldPrint=False)[1]
            for end in allMoves:
                #make a copy of the board
                newBoard = copy.deepcopy(myBoard)
                #move the piece
                newBoard.whiteMove(start, end)
                #check if end game
                if newBoard.isEndGame():
                    #if end game return true followed by the move
                    return (True,start,end)
        if color.lower()=='black':
            #find the moves
            allMoves = myBoard.checkBlackPossibleMoves(start,shouldPrint=False)[1]
            for end in allMoves:
                #make a copy of the board
                newBoard = copy.deepcopy(myBoard)
                #move the piece
                newBoard.blackMove(start, end)
                #check if end game
                if newBoard.isEndGame():
                    #if end game return true followed by the move
#                    print "Mate Possible",start,end
                    return (True,start,end)
    return (False,None,None)
    
def pawnUpgrade(piece,board,history,choice):
    """
        Upgrades a pawn based on the choice that was given.
        1 = Knight
        2 = Bishop
        3 = Rook
        4 = Queen
        Then updates the board and history to see if a check or checkmate has
        occurred
    """
    color = piece.getColor()
    choice = int(choice)
    if color.lower() == 'black':
        inCheck = board.whiteInCheck
        hasMoves = board.whiteHasMoves
    elif color.lower()=='white':
        inCheck = board.blackInCheck
        hasMoves = board.blackHasMoves
    #transform pawn
    piece.chooseTrans(choice)
    #Remove the last board update and replace it with the board after you have
    #chosen the upgrade
    try:
        history.pop()
    except IndexError:
        pass
        
    history.append(copy.deepcopy(board))
    if not(hasMoves()):
        if not(inCheck()):
            print "Stalemate!"
            board.winner = "Stalemte!"
            board.endGame()
        elif inCheck():
            print "Checkmate.",color,"wins!"
            board.winner = "Checkmate. "+color+" wins!"
            board.endGame()    
    
def strategy1(color,myBoard,history,count,printStatements=True):
    """
        This is a strategy uses completely random motion. It does not know how
        to upgrade a pawn when the pawn reaches the end. This strategy does not
        search for checkmates.
    """
    assert (color.lower()=='white' or color.lower()=='black')
    if color.lower()=='white':
        #get pieces
        possiblePieces = myBoard.checkRemainingWhitePieces()
        #check which ones can move
        piecesThatCanMove = []
        for piece in possiblePieces:
#            print piece.getPosition()
            if len(myBoard.checkWhitePossibleMoves(piece.getPosition(),shouldPrint=False)[1])>0:
                piecesThatCanMove.append(piece)
        #pick a random piece from among the ones with moves
        piece = random.choice(piecesThatCanMove)
        start = piece.getPosition()
        #pick a random move from among its move set
        possibleMoves = myBoard.checkWhitePossibleMoves(start,shouldPrint=False)[1]
        end = random.choice(possibleMoves)
        #print the decision
        if printStatements:
            print start,"to",end
        #make the move
        a = myBoard.whiteMove(start, end)
        if a[0] == "Good":
            history.append(copy.deepcopy(myBoard))
            if printStatements:
                print ""
                print myBoard
                print ""
            if not(myBoard.isEndGame()):
                if myBoard.blackInCheck():
                    if printStatements:
                        print "Black is in check!\n"
                if a[1] or a[2]:
                    count = 0
                elif not(a[1]) and not(a[2]):
                    count += 1
                    if count >=50:
                        print "50 moves with no pawn movement or captue.\nStalemate!"
                        myBoard.endGame()
        else:
            print "Error!\n"

    elif color.lower()=='black':
        #get pieces
        possiblePieces = myBoard.checkRemainingBlackPieces()
        #check which ones can move
        piecesThatCanMove = []
        for piece in possiblePieces:
#            print piece.getPosition()
            if len(myBoard.checkBlackPossibleMoves(piece.getPosition(),shouldPrint=False)[1])>0:
                piecesThatCanMove.append(piece)
        #pick a random piece from among the ones with moves
        piece = random.choice(piecesThatCanMove)
        start = piece.getPosition()
        #pick a random move from among its move set
        possibleMoves = myBoard.checkBlackPossibleMoves(start,shouldPrint=False)[1]
        end = random.choice(possibleMoves)
        #print the decision
        if printStatements:
            print start,"to",end
        #make the move
        a = myBoard.blackMove(start, end)
        if a[0] == "Good":
            history.append(copy.deepcopy(myBoard))
            if printStatements:
                print ""
                print myBoard
                print ""
            if not(myBoard.isEndGame()):
                if myBoard.whiteInCheck():
                    if printStatements:
                        print "White is in check!\n"
                if a[1] or a[2]:
                    count = 0
                elif not(a[1]) and not(a[2]):
                    count += 1
                    if count >=50:
                        print "50 moves with no pawn movement or captue.\nStalemate!"
                        myBoard.endGame()
        else:
            print "Error!\n"

    return count
    
def strategy2(color,myBoard,history,count,printStatements=True):
    """
        This is a strategy uses completely random motion. When Pawn reaches 
        the end it will turn it into a queen. This strategy does not search for
        checkmates.
    """
    assert (color.lower()=='white' or color.lower()=='black')
    
    #set functions based on color
    if color.lower()=='white':
        getPieces = myBoard.checkRemainingWhitePieces
        checkMove = myBoard.checkWhitePossibleMoves
        movePiece = myBoard.whiteMove
        checkIfInCheck = myBoard.blackInCheck
        opponentColor = "Black"
    elif color.lower()=='black':
        getPieces = myBoard.checkRemainingBlackPieces
        checkMove = myBoard.checkBlackPossibleMoves
        movePiece = myBoard.blackMove
        checkIfInCheck = myBoard.whiteInCheck
        opponentColor = "White"

    #get pieces
    possiblePieces = getPieces()
    #check which ones can move
    piecesThatCanMove = []
    for piece in possiblePieces:
        if len(checkMove(piece.getPosition(),shouldPrint=False)[1])>0:
            piecesThatCanMove.append(piece)
    #pick a random piece from among the ones with moves
    piece = random.choice(piecesThatCanMove)
    start = piece.getPosition()
    #pick a random move from among its move set
    possibleMoves = checkMove(start,shouldPrint=False)[1]
    end = random.choice(possibleMoves)
    #print the decision
    if printStatements:
        print start,"to",end
    #make the move
    a = movePiece(start, end)
    if a[0] == "Good":
        history.append(copy.deepcopy(myBoard))
        if piece=="Pawn" and (piece.getPosition()[1] =='1' or piece.getPosition()[1] =='8'):
            pawnUpgrade(piece,myBoard,history,4)
        if printStatements:
            print ""
            print myBoard
            print ""
        if not(myBoard.isEndGame()):
            if checkIfInCheck():
                if printStatements:
                    print opponentColor,"is in check!\n"
            if a[1] or a[2]:
                count = 0
            elif not(a[1]) and not(a[2]):
                count += 1
                if count >=50:
                    print "50 moves with no pawn movement or captue.\nStalemate!"
                    myBoard.endGame()
    else:
        print "Error! Could not move piece!\n"

    return count

def strategy3(color,myBoard,history,count,printStatements=True):
    """
        This is a strategy uses completely random motion, but if it can checkmate,
        it will. When Pawn reaches the end it will turn it into a queen.
    """
    assert (color.lower()=='white' or color.lower()=='black')
    
    #set functions based on color
    if color.lower()=='white':
        getPieces = myBoard.checkRemainingWhitePieces
        checkMove = myBoard.checkWhitePossibleMoves
        movePiece = myBoard.whiteMove
        checkIfInCheck = myBoard.blackInCheck
        opponentColor = "Black"
    elif color.lower()=='black':
        getPieces = myBoard.checkRemainingBlackPieces
        checkMove = myBoard.checkBlackPossibleMoves
        movePiece = myBoard.blackMove
        checkIfInCheck = myBoard.whiteInCheck
        opponentColor = "White"

    #get pieces
    possiblePieces = getPieces()
    #check which ones can move
    piecesThatCanMove = []
    for piece in possiblePieces:
        if len(checkMove(piece.getPosition(),shouldPrint=False)[1])>0:
            piecesThatCanMove.append(piece)
    #check for mate
    mateResults = checkForMate(color,myBoard,piecesThatCanMove)
    
    #if mate possible, do that move
    if mateResults[0]:
        start = mateResults[1]
        end = mateResults[2]
    else:
        #pick a random piece from among the ones with moves
        piece = random.choice(piecesThatCanMove)
        start = piece.getPosition()
        #pick a random move from among its move set
        possibleMoves = checkMove(start,shouldPrint=False)[1]
        end = random.choice(possibleMoves)
    #print the decision
    if printStatements:
        print start,"to",end
    #make the move
    a = movePiece(start, end)
    if a[0] == "Good":
        history.append(copy.deepcopy(myBoard))
        if piece=="Pawn" and (piece.getPosition()[1] =='1' or piece.getPosition()[1] =='8'):
            pawnUpgrade(piece,myBoard,history,4)
        if printStatements:
            print ""
            print myBoard
            print ""
        if not(myBoard.isEndGame()):
            if checkIfInCheck():
                if printStatements:
                    print opponentColor,"is in check!\n"
            if a[1] or a[2]:
                count = 0
            elif not(a[1]) and not(a[2]):
                count += 1
                if count >=50:
                    print "50 moves with no pawn movement or captue.\nStalemate!"
                    myBoard.endGame()
    else:
        print "Error! Could not move piece!\n"

    return count

def scoreChessBoard1(color,board):
    """
    takes a board and the color of the player and determines the score for that
    player. returns the score. 
    Note: this doesn't handle adding points for captures well
    """
    #initialize the score
    score = 0
    #initilize key for scoring
    key = {'King': 15, 'Queen': 10, 'Rook': 7, 'Bishop': 6, 'Knight': 5, 'Pawn': 1}
    #get a list of my pieces
    if color.lower()=='white':
        myPieces = board.checkRemainingWhitePieces()
    if color.lower()=='black':
        myPieces = board.checkRemainingBlackPieces()
        
    for piece in myPieces:
        #get a list of threats and pieces this one can threaten
        threats = piece.getThreats()
        if len(threats)==0:
            #calculate score from what it can take only if no threats
            threatened = piece.getThreatenedPieces()
            for piece2 in threatened:
                score += key[piece2.getName()]
        else:
            #subtract points for it being threatened based on its type
            score -= key[piece.getName()]
    return score
    
def scoreChessBoard2(color,board):
    """
    takes a board and the color of the player and determines the score for that
    player. returns the score. subtract points for each opponent piece on the field
    to promote capturing
    """
    #initialize the score
    score = 0.0
    #initilize key for scoring
    key = {'King': 20.0, 'Queen': 10.0, 'Rook': 7.0, 'Bishop': 6.0, 'Knight': 5.0, 'Pawn': 1.0}
    #get a list of my pieces
    if color.lower()=='white':
        myPieces = board.checkRemainingWhitePieces()
        opponentPieces = board.checkRemainingBlackPieces()
    if color.lower()=='black':
        myPieces = board.checkRemainingBlackPieces()
        opponentPieces = board.checkRemainingWhitePieces()
    #subtract points for each opponent piece on field
    for piece in opponentPieces:
        score -= 1.5*key[piece.getName()]
    for piece in myPieces:
        #get a list of threats and pieces this one can threaten
        threats = piece.getThreats()
        if len(threats)==0:
            #calculate score from what it can take only if no threats
            threatened = piece.getThreatenedPieces()
            for piece2 in threatened:
                score += 1.2*key[piece2.getName()]
        else:
            #subtract points for it being threatened based on its type
            score -= key[piece.getName()]
    return score
    
def strategy4(color,myBoard,history,count,printStatements=True):
    """
        This is a strategy uses scoreChessBoard1 to determine the best move.
        If it can checkmate, it will. When Pawn reaches the end it will turn it
        into a queen.
    """
    assert (color.lower()=='white' or color.lower()=='black')
    
    #set functions based on color
    if color.lower()=='white':
        getPieces = myBoard.checkRemainingWhitePieces
        checkMove = myBoard.checkWhitePossibleMoves
        movePiece = myBoard.whiteMove
        checkIfInCheck = myBoard.blackInCheck
        opponentColor = "Black"
    elif color.lower()=='black':
        getPieces = myBoard.checkRemainingBlackPieces
        checkMove = myBoard.checkBlackPossibleMoves
        movePiece = myBoard.blackMove
        checkIfInCheck = myBoard.whiteInCheck
        opponentColor = "White"

    #get pieces
    possiblePieces = getPieces()
    #check which ones can move
    piecesThatCanMove = []
    for piece in possiblePieces:
        if len(checkMove(piece.getPosition(),shouldPrint=False)[1])>0:
            piecesThatCanMove.append(piece)
    #check for mate
    mateResults = checkForMate(color,myBoard,piecesThatCanMove)
    
    #if mate possible, do that move
    if mateResults[0]:
        start = mateResults[1]
        end = mateResults[2]
    else:
        highScore = 0
        bestStart = None
        bestEnd = None
        #check all pieces and get moves
        for piece in piecesThatCanMove:
            start = piece.getPosition()
            possibleMoves = checkMove(start,shouldPrint=False)[1]
            for end in possibleMoves:
                #make a copy board
                myBoard2 = copy.deepcopy(myBoard)
                #move piece
                if color.lower()=='white':
                    myBoard2.whiteMove(start, end)
                elif color.lower()=='black':
                    myBoard2.blackMove(start, end)
                #check the score for the move
                moveScore = scoreChessBoard1(color,myBoard2)
                #make this the best move if it's score is higher than other moves
                #or if there has bot been a move chosen yet
                if moveScore > highScore or bestStart==None:
                    bestStart = start
                    bestEnd = end
                    highScore = moveScore
        start = bestStart
        end = bestEnd
        piece = myBoard.getPieceAt(start)
#        print "best score found:",highScore

    #print the decision
    if printStatements:
        print start,"to",end
    #make the move
    a = movePiece(start, end)
    if a[0] == "Good":
        history.append(copy.deepcopy(myBoard))
        if piece=="Pawn" and (piece.getPosition()[1] =='1' or piece.getPosition()[1] =='8'):
            pawnUpgrade(piece,myBoard,history,4)
        if printStatements:
            print ""
            print myBoard
            print ""
        if not(myBoard.isEndGame()):
            if checkIfInCheck():
                if printStatements:
                    print opponentColor,"is in check!\n"
            if a[1] or a[2]:
                count = 0
            elif not(a[1]) and not(a[2]):
                count += 1
                if count >=50:
                    print "50 moves with no pawn movement or captue.\nStalemate!"
                    myBoard.endGame()
    else:
        print "Error! Could not move piece!\n"

    return count

def strategy5(color,myBoard,history,count,printStatements=True):
    """
        This is a strategy uses scoreChessBoard2 to determine the best move.
        If it can checkmate, it will. When Pawn reaches the end it will turn it
        into a queen.
    """
    assert (color.lower()=='white' or color.lower()=='black')
    
    #set functions based on color
    if color.lower()=='white':
        getPieces = myBoard.checkRemainingWhitePieces
        checkMove = myBoard.checkWhitePossibleMoves
        movePiece = myBoard.whiteMove
        checkIfInCheck = myBoard.blackInCheck
        opponentColor = "Black"
    elif color.lower()=='black':
        getPieces = myBoard.checkRemainingBlackPieces
        checkMove = myBoard.checkBlackPossibleMoves
        movePiece = myBoard.blackMove
        checkIfInCheck = myBoard.whiteInCheck
        opponentColor = "White"

    #get pieces
    possiblePieces = getPieces()
    #check which ones can move
    piecesThatCanMove = []
    for piece in possiblePieces:
        if len(checkMove(piece.getPosition(),shouldPrint=False)[1])>0:
            piecesThatCanMove.append(piece)
    #check for mate
    mateResults = checkForMate(color,myBoard,piecesThatCanMove)
    
    #if mate possible, do that move
    if mateResults[0]:
        start = mateResults[1]
        end = mateResults[2]
    else:
        highScore = 0
        bestStart = None
        bestEnd = None
        #check all pieces and get moves
        for piece in piecesThatCanMove:
            start = piece.getPosition()
            possibleMoves = checkMove(start,shouldPrint=False)[1]
            for end in possibleMoves:
                #make a copy board
                myBoard2 = copy.deepcopy(myBoard)
                #move piece
                if color.lower()=='white':
                    myBoard2.whiteMove(start, end)
                elif color.lower()=='black':
                    myBoard2.blackMove(start, end)
                #check the score for the move
                moveScore = scoreChessBoard2(color,myBoard2)
                #make this the best move if it's score is higher than other moves
                #or if there has bot been a move chosen yet
                if moveScore > highScore or bestStart==None:
                    bestStart = start
                    bestEnd = end
                    highScore = moveScore
        start = bestStart
        end = bestEnd
        piece = myBoard.getPieceAt(start)
#        print "best score found:",highScore

    #print the decision
    if printStatements:
        print start,"to",end
    #make the move
    a = movePiece(start, end)
    if a[0] == "Good":
        history.append(copy.deepcopy(myBoard))
        if piece=="Pawn" and (piece.getPosition()[1] =='1' or piece.getPosition()[1] =='8'):
            pawnUpgrade(piece,myBoard,history,4)
        if printStatements:
            print ""
            print myBoard
            print ""
        if not(myBoard.isEndGame()):
            if checkIfInCheck():
                if printStatements:
                    print opponentColor,"is in check!\n"
            if a[1] or a[2]:
                count = 0
            elif not(a[1]) and not(a[2]):
                count += 1
                if count >=50:
                    print "50 moves with no pawn movement or captue.\nStalemate!"
                    myBoard.endGame()
    else:
        print "Error! Could not move piece!\n"

    return count
    
def strategy6(color,myBoard,history,count,printStatements=True):
    """
        This is a strategy uses scoreChessBoard2 to determine the best move.
        If it can checkmate, it will. When Pawn reaches the end it will turn it
        into a queen. Pick randomly from moves with same score
    """
    assert (color.lower()=='white' or color.lower()=='black')
    
    #set functions based on color
    if color.lower()=='white':
        getPieces = myBoard.checkRemainingWhitePieces
        checkMove = myBoard.checkWhitePossibleMoves
        movePiece = myBoard.whiteMove
        checkIfInCheck = myBoard.blackInCheck
        opponentColor = "Black"
    elif color.lower()=='black':
        getPieces = myBoard.checkRemainingBlackPieces
        checkMove = myBoard.checkBlackPossibleMoves
        movePiece = myBoard.blackMove
        checkIfInCheck = myBoard.whiteInCheck
        opponentColor = "White"

    #get pieces
    possiblePieces = getPieces()
    #check which ones can move
    piecesThatCanMove = []
    for piece in possiblePieces:
        if len(checkMove(piece.getPosition(),shouldPrint=False)[1])>0:
            piecesThatCanMove.append(piece)
    #check for mate
    mateResults = checkForMate(color,myBoard,piecesThatCanMove)
    
    #if mate possible, do that move
    if mateResults[0]:
        start = mateResults[1]
        end = mateResults[2]
    else:
        highScore = 0
        bestMoves = []
        #check all pieces and get moves
        for piece in piecesThatCanMove:
            start = piece.getPosition()
            possibleMoves = checkMove(start,shouldPrint=False)[1]
            for end in possibleMoves:
                #make a copy board
                myBoard2 = copy.deepcopy(myBoard)
                #move piece
                if color.lower()=='white':
                    myBoard2.whiteMove(start, end)
                elif color.lower()=='black':
                    myBoard2.blackMove(start, end)
                #check the score for the move
                moveScore = scoreChessBoard2(color,myBoard2)
                #make this the best move if it's score is higher than other moves
                #or if there has bot been a move chosen yet
                if moveScore > highScore or len(bestMoves)==0:
                    bestMoves = [(start,end)]
                    highScore = moveScore
                elif moveScore==highScore:
                    bestMoves.append((start,end))
        chosen = random.choice(bestMoves)
        start = chosen[0]
        end = chosen[1]
        piece = myBoard.getPieceAt(start)
#        print "best score found:",highScore

    #print the decision
    if printStatements:
        print start,"to",end
    #make the move
    a = movePiece(start, end)
    if a[0] == "Good":
        history.append(copy.deepcopy(myBoard))
        if piece=="Pawn" and (piece.getPosition()[1] =='1' or piece.getPosition()[1] =='8'):
            pawnUpgrade(piece,myBoard,history,4)
        if printStatements:
            print ""
            print myBoard
            print ""
        if not(myBoard.isEndGame()):
            if checkIfInCheck():
                if printStatements:
                    print opponentColor,"is in check!\n"
            if a[1] or a[2]:
                count = 0
            elif not(a[1]) and not(a[2]):
                count += 1
                if count >=50:
                    print "50 moves with no pawn movement or captue.\nStalemate!"
                    myBoard.endGame()
    else:
        print "Error! Could not move piece!\n"

    return count
    
def scoreChessBoard3(color,board):
    """
    takes a board and the color of the player and determines the score for that
    player. returns the score. subtract points for each opponent piece on the field
    to promote capturing. Huge penalty for moves that would be stalemate.
    If pawn is at an edge, it will change it to a queen.
    """
    #initialize the score
    score = 0.0
    #initilize key for scoring
    key = {'King': 20.0, 'Queen': 10.0, 'Rook': 7.0, 'Bishop': 6.0, 'Knight': 5.0, 'Pawn': 1.0}
    #get a list of my pieces
    if color.lower()=='white':
        myPieces = board.checkRemainingWhitePieces()
        opponentPieces = board.checkRemainingBlackPieces()
        opHasMoves = board.blackHasMoves
    if color.lower()=='black':
        myPieces = board.checkRemainingBlackPieces()
        opponentPieces = board.checkRemainingWhitePieces()
        opHasMoves = board.whiteHasMoves
        
    #penalize stalematemoves severely so as to avoid this move
    if not opHasMoves:
        score -= 9999
    #subtract points for each opponent piece on field
    for piece in opponentPieces:
        score -= 1.5*key[piece.getName()]
    for piece in myPieces:
        #get a list of threats and pieces this one can threaten
        threats = piece.getThreats()
        if len(threats)==0:
            if piece=="Pawn" and (piece.getPosition()[1] =='1' or piece.getPosition()[1] =='8'):
                pawnUpgrade(piece,board,[0],4)
            #calculate score from what it can take only if no threats
            threatened = piece.getThreatenedPieces()
            for piece2 in threatened:
                score += 1.2*key[piece2.getName()]
        else:
            #subtract points for it being threatened based on its type
            score -= key[piece.getName()]
    return score
    
def strategy7(color,myBoard,history,count,printStatements=True):
    """
        This is a strategy uses scoreChessBoard3 to determine the best move and
        avoid stalemate. If it can checkmate, it will. When Pawn reaches the 
        end it will turn it into a queen. Pick randomly from moves with same score
    """
    assert (color.lower()=='white' or color.lower()=='black')
    
    #set functions based on color
    if color.lower()=='white':
        getPieces = myBoard.checkRemainingWhitePieces
        checkMove = myBoard.checkWhitePossibleMoves
        movePiece = myBoard.whiteMove
        checkIfInCheck = myBoard.blackInCheck
        opponentColor = "Black"
    elif color.lower()=='black':
        getPieces = myBoard.checkRemainingBlackPieces
        checkMove = myBoard.checkBlackPossibleMoves
        movePiece = myBoard.blackMove
        checkIfInCheck = myBoard.whiteInCheck
        opponentColor = "White"

    #get pieces
    possiblePieces = getPieces()
    #check which ones can move
    piecesThatCanMove = []
    for piece in possiblePieces:
        if len(checkMove(piece.getPosition(),shouldPrint=False)[1])>0:
            piecesThatCanMove.append(piece)
    #check for mate
    mateResults = checkForMate(color,myBoard,piecesThatCanMove)
    
    #if mate possible, do that move
    if mateResults[0]:
        start = mateResults[1]
        end = mateResults[2]
    else:
        highScore = 0
        bestMoves = []
        #check all pieces and get moves
        for piece in piecesThatCanMove:
            start = piece.getPosition()
            possibleMoves = checkMove(start,shouldPrint=False)[1]
            for end in possibleMoves:
                #make a copy board
                myBoard2 = copy.deepcopy(myBoard)
                #move piece
                if color.lower()=='white':
                    myBoard2.whiteMove(start, end)
                elif color.lower()=='black':
                    myBoard2.blackMove(start, end)
                #check the score for the move
                moveScore = scoreChessBoard3(color,myBoard2)
                #make this the best move if it's score is higher than other moves
                #or if there has bot been a move chosen yet
                if moveScore > highScore or len(bestMoves)==0:
                    bestMoves = [(start,end)]
                    highScore = moveScore
                elif moveScore==highScore:
                    bestMoves.append((start,end))
        chosen = random.choice(bestMoves)
        start = chosen[0]
        end = chosen[1]
        piece = myBoard.getPieceAt(start)
#        print "best score found:",highScore

    #print the decision
    if printStatements:
        print start,"to",end
    #make the move
    a = movePiece(start, end)
    if a[0] == "Good":
        history.append(copy.deepcopy(myBoard))
        if piece=="Pawn" and (piece.getPosition()[1] =='1' or piece.getPosition()[1] =='8'):
            pawnUpgrade(piece,myBoard,history,4)
        if printStatements:
            print ""
            print myBoard
            print ""
        if not(myBoard.isEndGame()):
            if checkIfInCheck():
                if printStatements:
                    print opponentColor,"is in check!\n"
            if a[1] or a[2]:
                count = 0
            elif not(a[1]) and not(a[2]):
                count += 1
                if count >=50:
                    print "50 moves with no pawn movement or captue.\nStalemate!"
                    myBoard.endGame()
    else:
        print "Error! Could not move piece!\n"

    return count
    
def scoreChessBoard4(color,board,tempCount,history):
    """
    takes a board and the color of the player and determines the score for that
    player. returns the score. subtract points for each opponent piece on the field
    to promote capturing. Huge penalty for moves that would be stalemate.
    If pawn is at an edge, it will change it to a queen.
    """
    #initialize the score
    score = 0.0
    #initilize key for scoring
    key = {'King': 20.0, 'Queen': 10.0, 'Rook': 7.0, 'Bishop': 6.0, 'Knight': 5.0, 'Pawn': 1.0}
    #get a list of my pieces
    if color.lower()=='white':
        myPieces = board.checkRemainingWhitePieces()
        opponentPieces = board.checkRemainingBlackPieces()
        opHasMoves = board.blackHasMoves
    if color.lower()=='black':
        myPieces = board.checkRemainingBlackPieces()
        opponentPieces = board.checkRemainingWhitePieces()
        opHasMoves = board.whiteHasMoves
        
    
    #penalize stalematemoves severely so as to avoid this move
    if (not opHasMoves) or tempCount>=50 or threeMoveRep(history, board):
        score -= 9999
    #subtract points for each opponent piece on field
    for piece in opponentPieces:
        score -= 1.5*key[piece.getName()]
    for piece in myPieces:
        #get a list of threats and pieces this one can threaten
        threats = piece.getThreats()
        if len(threats)==0:
            if piece=="Pawn" and (piece.getPosition()[1] =='1' or piece.getPosition()[1] =='8'):
                pawnUpgrade(piece,board,[0],4)
            #calculate score from what it can take only if no threats
            threatened = piece.getThreatenedPieces()
            for piece2 in threatened:
                score += 1.2*key[piece2.getName()]
        else:
            #subtract points for it being threatened based on its type
            score -= key[piece.getName()]
    return score
    
def strategy8(color,myBoard,history,count,printStatements=True):
    """
        This is a strategy uses scoreChessBoard4 to determine the best move and
        avoid stalemate. If it can checkmate, it will. When Pawn reaches the 
        end it will turn it into a queen. Pick randomly from moves with same score
        watches out for 3 move repeat stalemate and 50 move stalemate
    """
    assert (color.lower()=='white' or color.lower()=='black')
    
    #set functions based on color
    if color.lower()=='white':
        getPieces = myBoard.checkRemainingWhitePieces
        checkMove = myBoard.checkWhitePossibleMoves
        movePiece = myBoard.whiteMove
        checkIfInCheck = myBoard.blackInCheck
        opponentColor = "Black"
    elif color.lower()=='black':
        getPieces = myBoard.checkRemainingBlackPieces
        checkMove = myBoard.checkBlackPossibleMoves
        movePiece = myBoard.blackMove
        checkIfInCheck = myBoard.whiteInCheck
        opponentColor = "White"

    #get pieces
    possiblePieces = getPieces()
    #check which ones can move
    piecesThatCanMove = []
    for piece in possiblePieces:
        if len(checkMove(piece.getPosition(),shouldPrint=False)[1])>0:
            piecesThatCanMove.append(piece)
    #check for mate
    mateResults = checkForMate(color,myBoard,piecesThatCanMove)
    
    #if mate possible, do that move
    if mateResults[0]:
        start = mateResults[1]
        end = mateResults[2]
    else:
        highScore = 0
        bestMoves = []
        #check all pieces and get moves
        for piece in piecesThatCanMove:
            start = piece.getPosition()
            possibleMoves = checkMove(start,shouldPrint=False)[1]
            for end in possibleMoves:
                #make a copy board
                myBoard2 = copy.deepcopy(myBoard)
                #move piece
                if color.lower()=='white':
                    tempA = myBoard2.whiteMove(start, end)
                elif color.lower()=='black':
                    tempA = myBoard2.blackMove(start, end)
                if tempA[1] or tempA[2]:
                    tempCount = 0
                else:
                    tempCount = count + 1
                #check the score for the move
                moveScore = scoreChessBoard4(color,myBoard2,tempCount,history)
                #make this the best move if it's score is higher than other moves
                #or if there has bot been a move chosen yet
                if moveScore > highScore or len(bestMoves)==0:
                    bestMoves = [(start,end)]
                    highScore = moveScore
                elif moveScore==highScore:
                    bestMoves.append((start,end))
        chosen = random.choice(bestMoves)
        start = chosen[0]
        end = chosen[1]
        piece = myBoard.getPieceAt(start)
#        print "best score found:",highScore

    #print the decision
    if printStatements:
        print start,"to",end
    #make the move
    a = movePiece(start, end)
    if a[0] == "Good":
        history.append(copy.deepcopy(myBoard))
        if piece=="Pawn" and (piece.getPosition()[1] =='1' or piece.getPosition()[1] =='8'):
            pawnUpgrade(piece,myBoard,history,4)
        if printStatements:
            print ""
            print myBoard
            print ""
        if not(myBoard.isEndGame()):
            if checkIfInCheck():
                if printStatements:
                    print opponentColor,"is in check!\n"
            if a[1] or a[2]:
                count = 0
            elif not(a[1]) and not(a[2]):
                count += 1
                if count >=50:
                    print "50 moves with no pawn movement or captue.\nStalemate!"
                    myBoard.endGame()
    else:
        print "Error! Could not move piece!\n"

    return count
    


def scoreChessBoard5(color,board,tempCount,history):
    """
    takes a board and the color of the player and determines the score for that
    player. returns the score. subtract points for each opponent piece on the field
    to promote capturing. Huge penalty for moves that would be stalemate.
    If pawn is at an edge, it will change it to a queen. Avoids moves that allow
    other person to mate if possible.
    """
    #initialize the score
    score = 0.0
    #initilize key for scoring
    key = {'King': 20.0, 'Queen': 10.0, 'Rook': 7.0, 'Bishop': 6.0, 'Knight': 5.0, 'Pawn': 1.0}
    #get a list of my pieces
    if color.lower()=='white':
        myPieces = board.checkRemainingWhitePieces()
        opponentPieces = board.checkRemainingBlackPieces()
        opHasMoves = board.blackHasMoves
        opponentColor = 'black'
        checkOpMove = board.checkBlackPossibleMoves
    elif color.lower()=='black':
        myPieces = board.checkRemainingBlackPieces()
        opponentPieces = board.checkRemainingWhitePieces()
        opHasMoves = board.whiteHasMoves
        opponentColor = 'white'
        checkOpMove = board.checkWhitePossibleMoves
        
    #penalize severely for moves that allow opponent to mate
    piecesThatCanMove = []
    for piece in opponentPieces:
        if len(checkOpMove(piece.getPosition(),shouldPrint=False)[1])>0:
            piecesThatCanMove.append(piece)
    mateResults = checkForMate(opponentColor,board,piecesThatCanMove)
    if mateResults[0]:
        score -= 99999
    #penalize stalematemoves severely so as to avoid this move
    if (not opHasMoves) or tempCount>=48 or twoMoveRep(history, board):
        score -= 9999
    #subtract points for each opponent piece on field
    for piece in opponentPieces:
        score -= 1.5*key[piece.getName()]
    for piece in myPieces:
        #get a list of threats and pieces this one can threaten
        threats = piece.getThreats()
        if len(threats)==0:
            if piece=="Pawn" and (piece.getPosition()[1] =='1' or piece.getPosition()[1] =='8'):
                pawnUpgrade(piece,board,[0],4)
            #calculate score from what it can take only if no threats
            threatened = piece.getThreatenedPieces()
            for piece2 in threatened:
                score += 1.2*key[piece2.getName()]
        else:
            #subtract points for it being threatened based on its type
            score -= key[piece.getName()]
    return score
    
def strategy9(color,myBoard,history,count,printStatements=True):
    """
        This is a strategy uses scoreChessBoard5 to determine the best move and
        avoid stalemate. If it can checkmate, it will. When Pawn reaches the 
        end it will turn it into a queen. Pick randomly from moves with same score
        watches out for 3 move repeat stalemate and 50 move stalemate. Avoids 
        moves that will allow the opponent to mate if possible.
    """
    assert (color.lower()=='white' or color.lower()=='black')
    
    #set functions based on color
    if color.lower()=='white':
        getPieces = myBoard.checkRemainingWhitePieces
        checkMove = myBoard.checkWhitePossibleMoves
        movePiece = myBoard.whiteMove
        checkIfInCheck = myBoard.blackInCheck
        opponentColor = "Black"
    elif color.lower()=='black':
        getPieces = myBoard.checkRemainingBlackPieces
        checkMove = myBoard.checkBlackPossibleMoves
        movePiece = myBoard.blackMove
        checkIfInCheck = myBoard.whiteInCheck
        opponentColor = "White"

    #get pieces
    possiblePieces = getPieces()
    #check which ones can move
    piecesThatCanMove = []
    for piece in possiblePieces:
        if len(checkMove(piece.getPosition(),shouldPrint=False)[1])>0:
            piecesThatCanMove.append(piece)
    #check for mate
    mateResults = checkForMate(color,myBoard,piecesThatCanMove)
    
    #if mate possible, do that move
    if mateResults[0]:
        start = mateResults[1]
        end = mateResults[2]
    else:
        highScore = 0
        bestMoves = []
        #check all pieces and get moves
        for piece in piecesThatCanMove:
            start = piece.getPosition()
            possibleMoves = checkMove(start,shouldPrint=False)[1]
            for end in possibleMoves:
                #make a copy board
                myBoard2 = copy.deepcopy(myBoard)
                #move piece
                if color.lower()=='white':
                    tempA = myBoard2.whiteMove(start, end)
                elif color.lower()=='black':
                    tempA = myBoard2.blackMove(start, end)
                if tempA[1] or tempA[2]:
                    tempCount = 0
                else:
                    tempCount = count + 1
                #check the score for the move
                moveScore = scoreChessBoard5(color,myBoard2,tempCount,history)
                #make this the best move if it's score is higher than other moves
                #or if there has bot been a move chosen yet
                if moveScore > highScore or len(bestMoves)==0:
                    bestMoves = [(start,end)]
                    highScore = moveScore
                elif moveScore==highScore:
                    bestMoves.append((start,end))
        chosen = random.choice(bestMoves)
        start = chosen[0]
        end = chosen[1]
        piece = myBoard.getPieceAt(start)
#        print "best score found:",highScore

    #print the decision
    if printStatements:
        print start,"to",end
    #make the move
    a = movePiece(start, end)
    if a[0] == "Good":
        history.append(copy.deepcopy(myBoard))
        if piece=="Pawn" and (piece.getPosition()[1] =='1' or piece.getPosition()[1] =='8'):
            pawnUpgrade(piece,myBoard,history,4)
        if printStatements:
            print ""
            print myBoard
            print ""
        if not(myBoard.isEndGame()):
            if checkIfInCheck():
                if printStatements:
                    print opponentColor,"is in check!\n"
            if a[1] or a[2]:
                count = 0
            elif not(a[1]) and not(a[2]):
                count += 1
                if count >=50:
                    print "50 moves with no pawn movement or captue.\nStalemate!"
                    myBoard.endGame()
    else:
        print "Error! Could not move piece!\n"

    return count
def scoreChessBoard6(color,board,tempCount,history):
    """
    takes a board and the color of the player and determines the score for that
    player. returns the score. subtract points for each opponent piece on the field
    to promote capturing. Huge penalty for moves that would be stalemate.
    If pawn is at an edge, it will change it to a queen. Avoids moves that allow
    other person to mate if possible. Points awarded for freeing up movement of
    other pieces. Also King value slightly reduced and points readjusted.
    """
    #initialize the score
    score = 0.0
    #initilize key for scoring
    key = {'King': 13.0, 'Queen': 9.0, 'Rook': 5.0, 'Bishop': 3.2, 'Knight': 2.8, 'Pawn': 1.0}
    #get a list of my pieces
    if color.lower()=='white':
        myPieces = board.checkRemainingWhitePieces()
        opponentPieces = board.checkRemainingBlackPieces()
        opHasMoves = board.blackHasMoves
        opponentColor = 'black'
        checkOpMove = board.checkBlackPossibleMoves
        checkMyMove = board.checkWhitePossibleMoves
    elif color.lower()=='black':
        myPieces = board.checkRemainingBlackPieces()
        opponentPieces = board.checkRemainingWhitePieces()
        opHasMoves = board.whiteHasMoves
        opponentColor = 'white'
        checkOpMove = board.checkWhitePossibleMoves
        checkMyMove = board.checkBlackPossibleMoves
        
    #penalize severely for moves that allow opponent to mate
    piecesThatCanMove = []
    for piece in opponentPieces:
        if len(checkOpMove(piece.getPosition(),shouldPrint=False)[1])>0:
            piecesThatCanMove.append(piece)
    mateResults = checkForMate(opponentColor,board,piecesThatCanMove)
    if mateResults[0]:
        score -= 99999
    #penalize stalematemoves severely so as to avoid this move
    if (not opHasMoves) or tempCount>=48 or twoMoveRep(history, board):
        score -= 9999
    #subtract points for each opponent piece on field
    for piece in opponentPieces:
        score -= 2.5*key[piece.getName()]
    for piece in myPieces:
        #get a list of threats and pieces this one can threaten
        threats = piece.getThreats()
        if len(threats)==0:
            if piece=="Pawn" and (piece.getPosition()[1] =='1' or piece.getPosition()[1] =='8'):
                pawnUpgrade(piece,board,[0],4)
            #calculate score from what it can take only if no threats
            threatened = piece.getThreatenedPieces()
            for piece2 in threatened:
                score += 0.5*key[piece2.getName()]
            #add points for increasing the mobility of other pieces. ignore king mobility
            if not(piece=="King"):
                numPosMoves = len(checkMyMove(piece.getPosition(),shouldPrint=False)[1])
                score += 0.1*key[piece.getName()]*numPosMoves
        else:
            #subtract points for it being threatened based on its type
            score -= key[piece.getName()]
    return score
    
def strategy10(color,myBoard,history,count,printStatements=True):
    """
        This is a strategy uses scoreChessBoard6 to determine the best move and
        avoid stalemate. If it can checkmate, it will. When Pawn reaches the 
        end it will turn it into a queen. Pick randomly from moves with same score
        watches out for 3 move repeat stalemate and 50 move stalemate. Avoids 
        moves that will allow the opponent to mate if possible. Points awarded
        for freeing up movement of other pieces.
    """
    assert (color.lower()=='white' or color.lower()=='black')
    
    #set functions based on color
    if color.lower()=='white':
        getPieces = myBoard.checkRemainingWhitePieces
        checkMove = myBoard.checkWhitePossibleMoves
        movePiece = myBoard.whiteMove
        checkIfInCheck = myBoard.blackInCheck
        opponentColor = "Black"
    elif color.lower()=='black':
        getPieces = myBoard.checkRemainingBlackPieces
        checkMove = myBoard.checkBlackPossibleMoves
        movePiece = myBoard.blackMove
        checkIfInCheck = myBoard.whiteInCheck
        opponentColor = "White"

    #get pieces
    possiblePieces = getPieces()
    #check which ones can move
    piecesThatCanMove = []
    for piece in possiblePieces:
        if len(checkMove(piece.getPosition(),shouldPrint=False)[1])>0:
            piecesThatCanMove.append(piece)
    #check for mate
    mateResults = checkForMate(color,myBoard,piecesThatCanMove)
    
    #if mate possible, do that move
    if mateResults[0]:
        start = mateResults[1]
        end = mateResults[2]
    else:
        highScore = 0
        bestMoves = []
        #check all pieces and get moves
        for piece in piecesThatCanMove:
            start = piece.getPosition()
            possibleMoves = checkMove(start,shouldPrint=False)[1]
            for end in possibleMoves:
                #make a copy board
                myBoard2 = copy.deepcopy(myBoard)
                #move piece
                if color.lower()=='white':
                    tempA = myBoard2.whiteMove(start, end)
                elif color.lower()=='black':
                    tempA = myBoard2.blackMove(start, end)
                if tempA[1] or tempA[2]:
                    tempCount = 0
                else:
                    tempCount = count + 1
                #check the score for the move
                moveScore = scoreChessBoard6(color,myBoard2,tempCount,history)
                #make this the best move if it's score is higher than other moves
                #or if there has bot been a move chosen yet
                if moveScore > highScore or len(bestMoves)==0:
                    bestMoves = [(start,end)]
                    highScore = moveScore
                elif moveScore==highScore:
                    bestMoves.append((start,end))
        chosen = random.choice(bestMoves)
        start = chosen[0]
        end = chosen[1]
        piece = myBoard.getPieceAt(start)
        print "best score found:",highScore

    #print the decision
    if printStatements:
        print start,"to",end
    #make the move
    a = movePiece(start, end)
    if a[0] == "Good":
        history.append(copy.deepcopy(myBoard))
        if piece=="Pawn" and (piece.getPosition()[1] =='1' or piece.getPosition()[1] =='8'):
            pawnUpgrade(piece,myBoard,history,4)
        if printStatements:
            print ""
            print myBoard
            print ""
        if not(myBoard.isEndGame()):
            if checkIfInCheck():
                if printStatements:
                    print opponentColor,"is in check!\n"
            if a[1] or a[2]:
                count = 0
            elif not(a[1]) and not(a[2]):
                count += 1
                if count >=50:
                    print "50 moves with no pawn movement or captue.\nStalemate!"
                    myBoard.endGame()
    else:
        print "Error! Could not move piece!\n"

    return count
    
def scoreChessBoard7(color,board,tempCount,history):
    """
    takes a board and the color of the player and determines the score for that
    player. returns the score. subtract points for each opponent piece on the field
    to promote capturing. Huge penalty for moves that would be stalemate.
    If pawn is at an edge, it will change it to a queen. Avoids moves that allow
    other person to mate if possible. Points awarded for freeing up movement of
    other pieces. Also King value slightly reduced and points readjusted. keeps
    track of protecting pieces
    """
    #initialize the score
    score = 0.0
    #initilize key for scoring
    key = {'King': 13.0, 'Queen': 9.0, 'Rook': 5.0, 'Bishop': 3.2, 'Knight': 2.8, 'Pawn': 1.0}
    #get a list of my pieces
    if color.lower()=='white':
        myPieces = board.checkRemainingWhitePieces()
        opponentPieces = board.checkRemainingBlackPieces()
        opHasMoves = board.blackHasMoves
        opponentColor = 'black'
        checkOpMove = board.checkBlackPossibleMoves
        checkMyMove = board.checkWhitePossibleMoves
    elif color.lower()=='black':
        myPieces = board.checkRemainingBlackPieces()
        opponentPieces = board.checkRemainingWhitePieces()
        opHasMoves = board.whiteHasMoves
        opponentColor = 'white'
        checkOpMove = board.checkWhitePossibleMoves
        checkMyMove = board.checkBlackPossibleMoves
        
    #penalize severely for moves that allow opponent to mate
    piecesThatCanMove = []
    for piece in opponentPieces:
        if len(checkOpMove(piece.getPosition(),shouldPrint=False)[1])>0:
            piecesThatCanMove.append(piece)
    mateResults = checkForMate(opponentColor,board,piecesThatCanMove)
    if mateResults[0]:
        score -= 99999
    #penalize stalematemoves severely so as to avoid this move
    if (not opHasMoves) or tempCount>=48 or oneMoveRep(history, board):
        score -= 9999
    #subtract points for each opponent piece on field
    for piece in opponentPieces:
        score -= 2.5*key[piece.getName()]
    for piece in myPieces:
        protectingPieces = []
        if not(piece=="King"):
            #make a copy of board
            spot = piece.getPosition()
            board2 = copy.deepcopy(board)
            #delete piece in copy
            board2.removePieceAt(spot)
            if color.lower()=='white':
                myPieces2 = board2.checkRemainingWhitePieces()
            elif color.lower()=='black':
                myPieces2 = board2.checkRemainingBlackPieces()
            #check which of my pieces can move to that square
            for p2 in myPieces2:
                if color.lower()=='white':
                    p2Moves = board2.checkWhitePossibleMoves(p2.getPosition(),shouldPrint=False)[1]
                elif color.lower()=='black':
                    p2Moves = board2.checkBlackPossibleMoves(p2.getPosition(),shouldPrint=False)[1]
                if spot in p2Moves:
                    score += 1/key[p2.getName()]
                    protectingPieces.append(p2)
        #compare to number of threats, add points for pieces gaurding and more points for weak gaurds using inverse function
        #if number of gaurds>number of threats, calculate score as if no threats
        #get a list of threats and pieces this one can threaten
        threats = piece.getThreats()
        if len(threats)<len(protectingPieces) or len(threats)==0:
            if piece=="Pawn" and (piece.getPosition()[1] =='1' or piece.getPosition()[1] =='8'):
                pawnUpgrade(piece,board,[0],4)
            #calculate score from what it can take only if no threats
            threatened = piece.getThreatenedPieces()
            for piece2 in threatened:
                score += 0.5*key[piece2.getName()]
            #add points for increasing the mobility of other pieces. ignore king mobility
            if not(piece=="King"):
                numPosMoves = len(checkMyMove(piece.getPosition(),shouldPrint=False)[1])
                score += 0.01*key[piece.getName()]*numPosMoves
        if len(threats)>0:
            #subtract points for it being threatened based on its type
            score -= key[piece.getName()]
    return score
    
def strategy11(color,myBoard,history,count,printStatements=True):
    """
        This is a strategy uses scoreChessBoard7 to determine the best move and
        avoid stalemate. If it can checkmate, it will. When Pawn reaches the 
        end it will turn it into a queen. Pick randomly from moves with same score
        watches out for 3 move repeat stalemate and 50 move stalemate. Avoids 
        moves that will allow the opponent to mate if possible. Points awarded
        for freeing up movement of other pieces. keeps track of protecting pieces
    """
    assert (color.lower()=='white' or color.lower()=='black')
    
    #set functions based on color
    if color.lower()=='white':
        getPieces = myBoard.checkRemainingWhitePieces
        checkMove = myBoard.checkWhitePossibleMoves
        movePiece = myBoard.whiteMove
        checkIfInCheck = myBoard.blackInCheck
        opponentColor = "Black"
    elif color.lower()=='black':
        getPieces = myBoard.checkRemainingBlackPieces
        checkMove = myBoard.checkBlackPossibleMoves
        movePiece = myBoard.blackMove
        checkIfInCheck = myBoard.whiteInCheck
        opponentColor = "White"

    #get pieces
    possiblePieces = getPieces()
    #check which ones can move
    piecesThatCanMove = []
    for piece in possiblePieces:
        if len(checkMove(piece.getPosition(),shouldPrint=False)[1])>0:
            piecesThatCanMove.append(piece)
    #check for mate
    mateResults = checkForMate(color,myBoard,piecesThatCanMove)
    
    #if mate possible, do that move
    if mateResults[0]:
        start = mateResults[1]
        end = mateResults[2]
    else:
        highScore = 0
        bestMoves = []
        #check all pieces and get moves
        for piece in piecesThatCanMove:
            start = piece.getPosition()
            possibleMoves = checkMove(start,shouldPrint=False)[1]
            for end in possibleMoves:
                #make a copy board
                myBoard2 = copy.deepcopy(myBoard)
                #move piece
                if color.lower()=='white':
                    tempA = myBoard2.whiteMove(start, end)
                elif color.lower()=='black':
                    tempA = myBoard2.blackMove(start, end)
                if tempA[1] or tempA[2]:
                    tempCount = 0
                else:
                    tempCount = count + 1
                #check the score for the move
                moveScore = scoreChessBoard7(color,myBoard2,tempCount,history)
                #make this the best move if it's score is higher than other moves
                #or if there has bot been a move chosen yet
                if moveScore > highScore or len(bestMoves)==0:
                    bestMoves = [(start,end)]
                    highScore = moveScore
                elif moveScore==highScore:
                    bestMoves.append((start,end))
        chosen = random.choice(bestMoves)
        start = chosen[0]
        end = chosen[1]
        piece = myBoard.getPieceAt(start)
        print "best score found:",highScore

    #print the decision
    if printStatements:
        print start,"to",end
    #make the move
    a = movePiece(start, end)
    if a[0] == "Good":
        history.append(copy.deepcopy(myBoard))
        if piece=="Pawn" and (piece.getPosition()[1] =='1' or piece.getPosition()[1] =='8'):
            pawnUpgrade(piece,myBoard,history,4)
        if printStatements:
            print ""
            print myBoard
            print ""
        if not(myBoard.isEndGame()):
            if checkIfInCheck():
                if printStatements:
                    print opponentColor,"is in check!\n"
            if a[1] or a[2]:
                count = 0
            elif not(a[1]) and not(a[2]):
                count += 1
                if count >=50:
                    print "50 moves with no pawn movement or captue.\nStalemate!"
                    myBoard.endGame()
    else:
        print "Error! Could not move piece!\n"

    return count    

def scoreChessBoard8(color,board,tempCount,history):
    """
    takes a board and the color of the player and determines the score for that
    player. returns the score. subtract points for each opponent piece on the field
    to promote capturing. Huge penalty for moves that would be stalemate.
    If pawn is at an edge, it will change it to a queen. Avoids moves that allow
    other person to mate if possible. Points awarded for freeing up movement of
    other pieces. Also King value slightly reduced and points readjusted. keeps
    track of protecting pieces
    """
    #initialize the score
    score = 0.0
    #initilize key for scoring
    key = {'King': 13.0, 'Queen': 9.0, 'Rook': 5.0, 'Bishop': 3.2, 'Knight': 2.8, 'Pawn': 1.0}
    #get a list of my pieces
    if color.lower()=='white':
        myPieces = board.checkRemainingWhitePieces()
        opponentPieces = board.checkRemainingBlackPieces()
        opHasMoves = board.blackHasMoves
        opponentColor = 'black'
        checkOpMove = board.checkBlackPossibleMoves
        checkMyMove = board.checkWhitePossibleMoves
    elif color.lower()=='black':
        myPieces = board.checkRemainingBlackPieces()
        opponentPieces = board.checkRemainingWhitePieces()
        opHasMoves = board.whiteHasMoves
        opponentColor = 'white'
        checkOpMove = board.checkWhitePossibleMoves
        checkMyMove = board.checkBlackPossibleMoves
        
    #penalize severely for moves that allow opponent to mate
    piecesThatCanMove = []
    for piece in opponentPieces:
        if len(checkOpMove(piece.getPosition(),shouldPrint=False)[1])>0:
            piecesThatCanMove.append(piece)
    mateResults = checkForMate(opponentColor,board,piecesThatCanMove)
    if mateResults[0]:
        score -= 99999
    #penalize stalematemoves severely so as to avoid this move
    if (not opHasMoves) or tempCount>=48 or oneMoveRep(history, board):
        score -= 9999
    #subtract points for each opponent piece on field
    for piece in opponentPieces:
        score -= 1.7*key[piece.getName()]
    for piece in myPieces:
        protectingPieces = []
        if not(piece=="King"):
            #make a copy of board
            spot = piece.getPosition()
            board2 = copy.deepcopy(board)
            #delete piece in copy
            board2.removePieceAt(spot)
            if color.lower()=='white':
                myPieces2 = board2.checkRemainingWhitePieces()
            elif color.lower()=='black':
                myPieces2 = board2.checkRemainingBlackPieces()
            #check which of my pieces can move to that square
            for p2 in myPieces2:
                if color.lower()=='white':
                    p2Moves = board2.checkWhitePossibleMoves(p2.getPosition(),shouldPrint=False)[1]
                elif color.lower()=='black':
                    p2Moves = board2.checkBlackPossibleMoves(p2.getPosition(),shouldPrint=False)[1]
                if spot in p2Moves:
                    score += 1/key[p2.getName()]
                    protectingPieces.append(p2)
        #compare to number of threats, add points for pieces gaurding and more points for weak gaurds using inverse function
        #if number of gaurds>number of threats, calculate score as if no threats
        #get a list of threats and pieces this one can threaten
        threats = piece.getThreats()
        threatScore = 0
        protectScore = key[piece.getName()]
        for p2 in protectingPieces:
            protectScore += key[p2.getName()]
        for p2 in threats:
            threatScore += key[p2.getName()]
        if (threatScore>=protectScore and len(threats)<=len(protectingPieces)) or len(threats)==0:
            if piece=="Pawn" and (piece.getPosition()[1] =='1' or piece.getPosition()[1] =='8'):
                pawnUpgrade(piece,board,[0],4)
            #calculate score from what it can take only if no threats
            threatened = piece.getThreatenedPieces()
            for piece2 in threatened:
                score += 0.5*key[piece2.getName()]
            #add points for increasing the mobility of other pieces. ignore king mobility
            if not(piece=="King"):
                numPosMoves = len(checkMyMove(piece.getPosition(),shouldPrint=False)[1])
#                score += 0.01*key[piece.getName()]*numPosMoves
                score += 0.01*numPosMoves
        if len(threats)>0:
            #subtract points for it being threatened based on its type
            score -= key[piece.getName()]
    return score

def strategy12(color,myBoard,history,count,printStatements=True):
    """
        This is a strategy uses scoreChessBoard8 to determine the best move and
        avoid stalemate. If it can checkmate, it will. When Pawn reaches the 
        end it will turn it into a queen. Pick randomly from moves with same score
        watches out for 3 move repeat stalemate and 50 move stalemate. Avoids 
        moves that will allow the opponent to mate if possible. Points awarded
        for freeing up movement of other pieces. keeps track of protecting pieces
    """
    assert (color.lower()=='white' or color.lower()=='black')
    
    #set functions based on color
    if color.lower()=='white':
        getPieces = myBoard.checkRemainingWhitePieces
        checkMove = myBoard.checkWhitePossibleMoves
        movePiece = myBoard.whiteMove
        checkIfInCheck = myBoard.blackInCheck
        opponentColor = "Black"
    elif color.lower()=='black':
        getPieces = myBoard.checkRemainingBlackPieces
        checkMove = myBoard.checkBlackPossibleMoves
        movePiece = myBoard.blackMove
        checkIfInCheck = myBoard.whiteInCheck
        opponentColor = "White"

    #get pieces
    possiblePieces = getPieces()
    #check which ones can move
    piecesThatCanMove = []
    for piece in possiblePieces:
        if len(checkMove(piece.getPosition(),shouldPrint=False)[1])>0:
            piecesThatCanMove.append(piece)
    #check for mate
    mateResults = checkForMate(color,myBoard,piecesThatCanMove)
    
    #if mate possible, do that move
    if mateResults[0]:
        start = mateResults[1]
        end = mateResults[2]
    else:
        highScore = 0
        bestMoves = []
        #check all pieces and get moves
        for piece in piecesThatCanMove:
            start = piece.getPosition()
            possibleMoves = checkMove(start,shouldPrint=False)[1]
            for end in possibleMoves:
                #make a copy board
                myBoard2 = copy.deepcopy(myBoard)
                #move piece
                if color.lower()=='white':
                    tempA = myBoard2.whiteMove(start, end)
                elif color.lower()=='black':
                    tempA = myBoard2.blackMove(start, end)
                if tempA[1] or tempA[2]:
                    tempCount = 0
                else:
                    tempCount = count + 1
                #check the score for the move
                moveScore = scoreChessBoard8(color,myBoard2,tempCount,history)
                #make this the best move if it's score is higher than other moves
                #or if there has bot been a move chosen yet
                if moveScore > highScore or len(bestMoves)==0:
                    bestMoves = [(start,end)]
                    highScore = moveScore
                elif moveScore==highScore:
                    bestMoves.append((start,end))
        chosen = random.choice(bestMoves)
        start = chosen[0]
        end = chosen[1]
        piece = myBoard.getPieceAt(start)
        print "best score found:",highScore

    #print the decision
    if printStatements:
        print start,"to",end
    #make the move
    a = movePiece(start, end)
    if a[0] == "Good":
        history.append(copy.deepcopy(myBoard))
        if piece=="Pawn" and (piece.getPosition()[1] =='1' or piece.getPosition()[1] =='8'):
            pawnUpgrade(piece,myBoard,history,4)
        if printStatements:
            print ""
            print myBoard
            print ""
        if not(myBoard.isEndGame()):
            if checkIfInCheck():
                if printStatements:
                    print opponentColor,"is in check!\n"
            if a[1] or a[2]:
                count = 0
            elif not(a[1]) and not(a[2]):
                count += 1
                if count >=50:
                    print "50 moves with no pawn movement or captue.\nStalemate!"
                    myBoard.endGame()
    else:
        print "Error! Could not move piece!\n"

    return count
    
    
def scoreChessBoard9(color,board,tempCount,history):
    """
    takes a board and the color of the player and determines the score for that
    player. returns the score. subtract points for each opponent piece on the field
    to promote capturing. Huge penalty for moves that would be stalemate.
    If pawn is at an edge, it will change it to a queen. Avoids moves that allow
    other person to mate if possible. Points awarded for freeing up movement of
    other pieces. Also King value slightly reduced and points readjusted. keeps
    track of protecting pieces. Points added for own pieces on field
    """
    #initialize the score
    score = 0.0
    #initilize key for scoring
    key = {'King': 13.0, 'Queen': 9.0, 'Rook': 5.0, 'Bishop': 3.2, 'Knight': 2.8, 'Pawn': 1.0}
    #get a list of my pieces
    if color.lower()=='white':
        myPieces = board.checkRemainingWhitePieces()
        opponentPieces = board.checkRemainingBlackPieces()
        opHasMoves = board.blackHasMoves
        opponentColor = 'black'
        checkOpMove = board.checkBlackPossibleMoves
        checkMyMove = board.checkWhitePossibleMoves
    elif color.lower()=='black':
        myPieces = board.checkRemainingBlackPieces()
        opponentPieces = board.checkRemainingWhitePieces()
        opHasMoves = board.whiteHasMoves
        opponentColor = 'white'
        checkOpMove = board.checkWhitePossibleMoves
        checkMyMove = board.checkBlackPossibleMoves
        
    #penalize severely for moves that allow opponent to mate
    piecesThatCanMove = []
    for piece in opponentPieces:
        if len(checkOpMove(piece.getPosition(),shouldPrint=False)[1])>0:
            piecesThatCanMove.append(piece)
    mateResults = checkForMate(opponentColor,board,piecesThatCanMove)
    if mateResults[0]:
        score -= 99999
    #penalize stalematemoves severely so as to avoid this move
    if (not opHasMoves) or tempCount>=48 or oneMoveRep(history, board):
        score -= 9999
    #subtract points for each opponent piece on field
    for piece in opponentPieces:
        score -= 1.7*key[piece.getName()]
    for piece in myPieces:
        score += 1.7*key[piece.getName()]
        protectingPieces = []
        if not(piece=="King"):
            #make a copy of board
            spot = piece.getPosition()
            board2 = copy.deepcopy(board)
            #delete piece in copy
            board2.removePieceAt(spot)
            if color.lower()=='white':
                myPieces2 = board2.checkRemainingWhitePieces()
            elif color.lower()=='black':
                myPieces2 = board2.checkRemainingBlackPieces()
            #check which of my pieces can move to that square
            for p2 in myPieces2:
                if color.lower()=='white':
                    p2Moves = board2.checkWhitePossibleMoves(p2.getPosition(),shouldPrint=False)[1]
                elif color.lower()=='black':
                    p2Moves = board2.checkBlackPossibleMoves(p2.getPosition(),shouldPrint=False)[1]
                if spot in p2Moves:
                    score += 1/key[p2.getName()]
                    protectingPieces.append(p2)
        #compare to number of threats, add points for pieces gaurding and more points for weak gaurds using inverse function
        #if number of gaurds>number of threats, calculate score as if no threats
        #get a list of threats and pieces this one can threaten
        threats = piece.getThreats()
        threatScore = 0
        protectScore = key[piece.getName()]
        for p2 in protectingPieces:
            protectScore += key[p2.getName()]
        for p2 in threats:
            threatScore += key[p2.getName()]
        if (threatScore>=protectScore and len(threats)<=len(protectingPieces)) or len(threats)==0:
            if piece=="Pawn" and (piece.getPosition()[1] =='1' or piece.getPosition()[1] =='8'):
                pawnUpgrade(piece,board,[0],4)
            #calculate score from what it can take only if no threats
            threatened = piece.getThreatenedPieces()
            for piece2 in threatened:
                score += 0.5*key[piece2.getName()]
            #add points for increasing the mobility of other pieces. ignore king mobility
            if not(piece=="King"):
                numPosMoves = len(checkMyMove(piece.getPosition(),shouldPrint=False)[1])
#                score += 0.01*key[piece.getName()]*numPosMoves
                score += 0.01*numPosMoves
        if len(threats)>0:
            #subtract points for it being threatened based on its type
            score -= key[piece.getName()]
    return score

def strategy13(color,myBoard,history,count,printStatements=True):
    """
        This is a strategy uses scoreChessBoard8 to determine the best move and
        avoid stalemate. If it can checkmate, it will. When Pawn reaches the 
        end it will turn it into a queen. Pick randomly from moves with same score
        watches out for 3 move repeat stalemate and 50 move stalemate. Avoids 
        moves that will allow the opponent to mate if possible. Points awarded
        for freeing up movement of other pieces. keeps track of protecting pieces
    """
    assert (color.lower()=='white' or color.lower()=='black')
    
    #set functions based on color
    if color.lower()=='white':
        getPieces = myBoard.checkRemainingWhitePieces
        checkMove = myBoard.checkWhitePossibleMoves
        movePiece = myBoard.whiteMove
        checkIfInCheck = myBoard.blackInCheck
        opponentColor = "Black"
    elif color.lower()=='black':
        getPieces = myBoard.checkRemainingBlackPieces
        checkMove = myBoard.checkBlackPossibleMoves
        movePiece = myBoard.blackMove
        checkIfInCheck = myBoard.whiteInCheck
        opponentColor = "White"

    #get pieces
    possiblePieces = getPieces()
    #check which ones can move
    piecesThatCanMove = []
    for piece in possiblePieces:
        if len(checkMove(piece.getPosition(),shouldPrint=False)[1])>0:
            piecesThatCanMove.append(piece)
    #check for mate
    mateResults = checkForMate(color,myBoard,piecesThatCanMove)
    
    #if mate possible, do that move
    if mateResults[0]:
        start = mateResults[1]
        end = mateResults[2]
    else:
        highScore = 0
        bestMoves = []
        #check all pieces and get moves
        for piece in piecesThatCanMove:
            start = piece.getPosition()
            possibleMoves = checkMove(start,shouldPrint=False)[1]
            for end in possibleMoves:
                #make a copy board
                myBoard2 = copy.deepcopy(myBoard)
                #move piece
                if color.lower()=='white':
                    tempA = myBoard2.whiteMove(start, end)
                elif color.lower()=='black':
                    tempA = myBoard2.blackMove(start, end)
                if tempA[1] or tempA[2]:
                    tempCount = 0
                else:
                    tempCount = count + 1
                #check the score for the move
                moveScore = scoreChessBoard9(color,myBoard2,tempCount,history)
                #make this the best move if it's score is higher than other moves
                #or if there has bot been a move chosen yet
                if moveScore > highScore or len(bestMoves)==0:
                    bestMoves = [(start,end)]
                    highScore = moveScore
                elif moveScore==highScore:
                    bestMoves.append((start,end))
        chosen = random.choice(bestMoves)
        start = chosen[0]
        end = chosen[1]
        piece = myBoard.getPieceAt(start)
        print "best score found:",highScore

    #print the decision
    if printStatements:
        print start,"to",end
    #make the move
    a = movePiece(start, end)
    if a[0] == "Good":
        history.append(copy.deepcopy(myBoard))
        if piece=="Pawn" and (piece.getPosition()[1] =='1' or piece.getPosition()[1] =='8'):
            pawnUpgrade(piece,myBoard,history,4)
        if printStatements:
            print ""
            print myBoard
            print ""
        if not(myBoard.isEndGame()):
            if checkIfInCheck():
                if printStatements:
                    print opponentColor,"is in check!\n"
            if a[1] or a[2]:
                count = 0
            elif not(a[1]) and not(a[2]):
                count += 1
                if count >=50:
                    print "50 moves with no pawn movement or captue.\nStalemate!"
                    myBoard.endGame()
    else:
        print "Error! Could not move piece!\n"

    return count


def scoreChessBoard10(color,board,tempCount,history):
    """
    takes a board and the color of the player and determines the score for that
    player. returns the score. subtract points for each opponent piece on the field
    to promote capturing. Huge penalty for moves that would be stalemate.
    If pawn is at an edge, it will change it to a queen. Avoids moves that allow
    other person to mate if possible. Points awarded for freeing up movement of
    other pieces. Also King value slightly reduced and points readjusted. keeps
    track of protecting pieces. Points added for own pieces on field. Points 
    subtracted for pawns too far from the end.
    """
    #initialize the score
    score = 0.0
    #initilize key for scoring
    key = {'King': 13.0, 'Queen': 9.0, 'Rook': 5.0, 'Bishop': 3.2, 'Knight': 2.8, 'Pawn': 1.0}
    #get a list of my pieces
    if color.lower()=='white':
        myPieces = board.checkRemainingWhitePieces()
        opponentPieces = board.checkRemainingBlackPieces()
        opHasMoves = board.blackHasMoves
        opponentColor = 'black'
        checkOpMove = board.checkBlackPossibleMoves
        checkMyMove = board.checkWhitePossibleMoves
        pawnGoalPos = 8
    elif color.lower()=='black':
        myPieces = board.checkRemainingBlackPieces()
        opponentPieces = board.checkRemainingWhitePieces()
        opHasMoves = board.whiteHasMoves
        opponentColor = 'white'
        checkOpMove = board.checkWhitePossibleMoves
        checkMyMove = board.checkBlackPossibleMoves
        pawnGoalPos = 1
        
    #penalize severely for moves that allow opponent to mate
    piecesThatCanMove = []
    for piece in opponentPieces:
        if len(checkOpMove(piece.getPosition(),shouldPrint=False)[1])>0:
            piecesThatCanMove.append(piece)
    mateResults = checkForMate(opponentColor,board,piecesThatCanMove)
    if mateResults[0]:
        score -= 99999
    #penalize stalematemoves severely so as to avoid this move
    if (not opHasMoves) or tempCount>=48 or oneMoveRep(history, board):
        score -= 9999
    #subtract points for each opponent piece on field
    for piece in opponentPieces:
        score -= 1.7*key[piece.getName()]
    for piece in myPieces:
        score += 1.7*key[piece.getName()]
        #subtract points for pawn being too far from the edge. promotes advancing pawns
        if piece == 'pawn':
            vertSpot = int(piece.getPosition()[1])
            score -= abs(pawnGoalPos-vertSpot)/30
        
        protectingPieces = []
        if not(piece=="King"):
            #make a copy of board
            spot = piece.getPosition()
            board2 = copy.deepcopy(board)
            #delete piece in copy
            board2.removePieceAt(spot)
            if color.lower()=='white':
                myPieces2 = board2.checkRemainingWhitePieces()
            elif color.lower()=='black':
                myPieces2 = board2.checkRemainingBlackPieces()
            #check which of my pieces can move to that square
            for p2 in myPieces2:
                if color.lower()=='white':
                    p2Moves = board2.checkWhitePossibleMoves(p2.getPosition(),shouldPrint=False)[1]
                elif color.lower()=='black':
                    p2Moves = board2.checkBlackPossibleMoves(p2.getPosition(),shouldPrint=False)[1]
                if spot in p2Moves:
                    score += 1/key[p2.getName()]
                    protectingPieces.append(p2)
        #compare to number of threats, add points for pieces gaurding and more points for weak gaurds using inverse function
        #if number of gaurds>number of threats, calculate score as if no threats
        #get a list of threats and pieces this one can threaten
        threats = piece.getThreats()
        threatScore = 0
        protectScore = key[piece.getName()]
        for p2 in protectingPieces:
            protectScore += key[p2.getName()]
        for p2 in threats:
            threatScore += key[p2.getName()]
        if (threatScore>=protectScore and len(threats)<=len(protectingPieces)) or len(threats)==0:
            if piece=="Pawn" and (piece.getPosition()[1] =='1' or piece.getPosition()[1] =='8'):
                pawnUpgrade(piece,board,[0],4)
            #calculate score from what it can take only if no threats
            threatened = piece.getThreatenedPieces()
            for piece2 in threatened:
                if piece2 =="King":
                    score += 0.25*key[piece2.getName()]
                else:
                    score += 0.5*key[piece2.getName()]
            #add points for increasing the mobility of other pieces. ignore king mobility
            if not(piece=="King"):
                numPosMoves = len(checkMyMove(piece.getPosition(),shouldPrint=False)[1])
#                score += 0.01*key[piece.getName()]*numPosMoves
                score += 0.01*numPosMoves
        if len(threats)>0:
            #subtract points for it being threatened based on its type
            score -= key[piece.getName()]
    return score

def strategy14(color,myBoard,history,count,printStatements=True):
    """
        This is a strategy uses scoreChessBoard8 to determine the best move and
        avoid stalemate. If it can checkmate, it will. When Pawn reaches the 
        end it will turn it into a queen. Pick randomly from moves with same score
        watches out for 3 move repeat stalemate and 50 move stalemate. Avoids 
        moves that will allow the opponent to mate if possible. Points awarded
        for freeing up movement of other pieces. keeps track of protecting pieces
    """
    assert (color.lower()=='white' or color.lower()=='black')
    
    #set functions based on color
    if color.lower()=='white':
        getPieces = myBoard.checkRemainingWhitePieces
        checkMove = myBoard.checkWhitePossibleMoves
        movePiece = myBoard.whiteMove
        checkIfInCheck = myBoard.blackInCheck
        opponentColor = "Black"
    elif color.lower()=='black':
        getPieces = myBoard.checkRemainingBlackPieces
        checkMove = myBoard.checkBlackPossibleMoves
        movePiece = myBoard.blackMove
        checkIfInCheck = myBoard.whiteInCheck
        opponentColor = "White"

    #get pieces
    possiblePieces = getPieces()
    #check which ones can move
    piecesThatCanMove = []
    for piece in possiblePieces:
        if len(checkMove(piece.getPosition(),shouldPrint=False)[1])>0:
            piecesThatCanMove.append(piece)
    #check for mate
    mateResults = checkForMate(color,myBoard,piecesThatCanMove)
    
    #if mate possible, do that move
    if mateResults[0]:
        start = mateResults[1]
        end = mateResults[2]
    else:
        highScore = 0
        bestMoves = []
        #check all pieces and get moves
        for piece in piecesThatCanMove:
            start = piece.getPosition()
            possibleMoves = checkMove(start,shouldPrint=False)[1]
            for end in possibleMoves:
                #make a copy board
                myBoard2 = copy.deepcopy(myBoard)
                #move piece
                if color.lower()=='white':
                    tempA = myBoard2.whiteMove(start, end)
                elif color.lower()=='black':
                    tempA = myBoard2.blackMove(start, end)
                if tempA[1] or tempA[2]:
                    tempCount = 0
                else:
                    tempCount = count + 1
                #check the score for the move
                moveScore = scoreChessBoard9(color,myBoard2,tempCount,history)
                #make this the best move if it's score is higher than other moves
                #or if there has bot been a move chosen yet
                if moveScore > highScore or len(bestMoves)==0:
                    bestMoves = [(start,end)]
                    highScore = moveScore
                elif moveScore==highScore:
                    bestMoves.append((start,end))
        chosen = random.choice(bestMoves)
        start = chosen[0]
        end = chosen[1]
        piece = myBoard.getPieceAt(start)
        print "best score found:",highScore

    #print the decision
    if printStatements:
        print start,"to",end
    #make the move
    a = movePiece(start, end)
    if a[0] == "Good":
        history.append(copy.deepcopy(myBoard))
        if piece=="Pawn" and (piece.getPosition()[1] =='1' or piece.getPosition()[1] =='8'):
            pawnUpgrade(piece,myBoard,history,4)
        if printStatements:
            print ""
            print myBoard
            print ""
        if not(myBoard.isEndGame()):
            if checkIfInCheck():
                if printStatements:
                    print opponentColor,"is in check!\n"
            if a[1] or a[2]:
                count = 0
            elif not(a[1]) and not(a[2]):
                count += 1
                if count >=50:
                    print "50 moves with no pawn movement or captue.\nStalemate!"
                    myBoard.endGame()
    else:
        print "Error! Could not move piece!\n"

    return count

strategies = [strategy1,strategy2,strategy3,strategy4,strategy5,strategy6,strategy7,strategy8,strategy9,strategy10,strategy11,strategy12,strategy13,strategy14]
stratNumList = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14']