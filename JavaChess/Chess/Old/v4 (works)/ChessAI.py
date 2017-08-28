import copy
import ChessBoard, Pieces, Strategy
        
def threeMoveRep(history, myBoard):
    """
        Returns true if this board arrangement has been encountered three or
        or more times in the given history
    """
    if history.count(myBoard)>=3:
        return True
    return False

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




def startGameAI():
    #allows you to designate which players will be AIs and which strategy to use for each AI
    strategies = Strategy.strategies
    AIcolorChoice = raw_input("Which color do you want to be the AI:\n1.Black\n2.White\n3.Neither\n4.Both\nYour choice:")
    while AIcolorChoice not in ['1','2','3','4']:
        AIcolorChoice = raw_input("Which color do you want to be the AI:\n1.Black\n2.White\n3.Neither\n4.Both\nYour choice:")
    if AIcolorChoice=='1':
        AIcolor = "black"
    elif AIcolorChoice=='2':
        AIcolor = "white"
    elif AIcolorChoice=='3':
        AIcolor = "neither"
    elif AIcolorChoice=='4':
        AIcolor = "both"
    if AIcolor.lower()=='white' or AIcolor.lower()=='both':
        whiteStrategyChoice = raw_input("Type the number of the strategy you want to use for White:")
        while whiteStrategyChoice not in Strategy.stratNumList:
            whiteStrategyChoice = raw_input("Type the number of the strategy you want to use for White:")
        whiteStrategy = strategies[int(whiteStrategyChoice)-1]
    if AIcolor.lower()=='black' or AIcolor.lower()=='both':
        blackStrategyChoice = raw_input("Type the number of the strategy you want to use for Black:")
        while blackStrategyChoice not in Strategy.stratNumList:
            blackStrategyChoice = raw_input("Type the number of the strategy you want to use for Black:")
        blackStrategy = strategies[int(blackStrategyChoice)-1]
        
    myBoard = ChessBoard.Board()
    i = -1
    count = 0
    history = []
    redo = []
    print ""
    print myBoard
    print ""
    history.append(copy.deepcopy(myBoard))
    while not(myBoard.isEndGame()):
#        pause = raw_input("pause")
        i += 1
        if i%2==0:
            #set white functions for white turn
            checkPossibleMoves = myBoard.checkWhitePossibleMoves
            pieceMove = myBoard.whiteMove
            opponentInCheck = myBoard.blackInCheck
            opponentColor = "Black"
            print "It is white's turn to move."
        else:
            #set black functions for black turn
            checkPossibleMoves = myBoard.checkBlackPossibleMoves
            pieceMove = myBoard.blackMove
            opponentInCheck = myBoard.whiteInCheck
            opponentColor = "White"
            print "It is black's turn to move."
        #AI moves if AI is available
        if i%2==0 and (AIcolor.lower()=='white' or AIcolor.lower()=='both'):
            count = whiteStrategy('white',myBoard,history,count)
            
        elif i%2==1 and (AIcolor.lower()=='black' or AIcolor.lower()=='both'):
            count = blackStrategy('black',myBoard,history,count)
            
        else:
            x = 0
            while x not in ['1','3','4']:
                x = raw_input("Choose an option:\n1.Make move\n2.Check possible moves for a piece\n3.Undo last move\n4.Redo\nYour choice:")
                print ""
                #check possible moves
                if x == '2':
                    square = raw_input("What is the square you want to check the moves for:")
                    print ""
                    checkPossibleMoves(square)
                    print ""

            #Move
            if x == '1':
                start = raw_input("Select starting square:")
                end = raw_input("Select ending square:")
                print ""
                a = pieceMove(start, end)
                if a[0] == "Good":
                    redo = []
                    history.append(copy.deepcopy(myBoard))
                    piece = myBoard.getPieceAt(end)
                    if piece=="Pawn" and (piece.getPosition()[1] =='1' or piece.getPosition()[1] =='8'):
                        choice = raw_input("Choose an option:\n1.Knight\n2.Bishop\n3.Rook\n4.Queen\nYour choice:")
                        while choice not in ['1','2','3','4']:
                            choice = raw_input("That is not a valid choice. Choose an option:\n1.Knight\n2.Bishop\n3.Rook\n4.Queen\nYour choice:")
                        pawnUpgrade(piece,myBoard,history,choice)
                    print ""
                    print myBoard
                    print ""
                    if not(myBoard.isEndGame()):
                        if opponentInCheck():
                            print opponentColor,"is in check!\n"
                        if a[1] or a[2]:
                            count = 0
                        elif not(a[1]) and not(a[2]):
                            count += 1
                            if count >=50:
                                print "50 moves with no pawn movement or captue.\nStalemate!"
                                myBoard.endGame()
                                myBoard.winner = "stalemate"
                else:
                    print "Please try again.\n"
                    i -= 1

            #undo
            if x == '3':
                if len(history)>=3:
                    i= i-3
                    #twice to undo the computers move also
                    redo.append(copy.deepcopy(history.pop()))
                    redo.append(copy.deepcopy(history.pop()))
                    myBoard = copy.deepcopy(history[-1])
                    print ""
                    print myBoard
                    print ""
                else:
                    print "No moves to undo.\n"
                    i -= 1
                
            #redo
            if x == '4':
                if len(redo)>=2:
                    i = i+1
                    #twice to redo the computers move also
                    history.append(copy.deepcopy(redo.pop()))
                    history.append(copy.deepcopy(redo.pop()))
                    myBoard = copy.deepcopy(history[-1])
                    print ""
                    print myBoard
                    print ""
                else:
                    print "Nothing to redo.\n"
                    i -= 1
                    
        if threeMoveRep(history, myBoard):
            answer = 0
            if AIcolor.lower()=='both':
                answer = "1"
            while answer not in ["1","2"]:
                answer = raw_input("Would you like to draw?\n1.Yes\n2.No\nYour choice:")
                print ""
            if answer == "1":
                print "Stalemate!"
                myBoard.endGame()
                myBoard.winner = "stalemate"
            if answer == "2":
                print "Will continue game.\n"
                

def montyPythonSim(whiteStrategyNum,blackStrategyNum,numberOfTrials=20):
    """
        Plays numberOfTrials games and calculates the percentage of time black 
        wins and percentage of time white wins. Most print statements removed.
        Option to undo and redo also removed.
    """
    #allows you to designate which players will be AIs and which strategy to use for each AI
    strategies = Strategy.strategies
    whiteStrategy = strategies[int(whiteStrategyNum)-1]
    blackStrategy = strategies[int(blackStrategyNum)-1]
    blackWins = 0.0
    whiteWins = 0.0
    stalecount = 0.0
    for gameNumber in range(numberOfTrials):
        print "Starting game",gameNumber+1,"out of",numberOfTrials
        myBoard = ChessBoard.Board()
        i = -1
        count = 0
        history = []

        while not(myBoard.isEndGame()):
    #        pause = raw_input("pause")
            i += 1
            #AI moves if AI is available
            if i%2==0:
                count = whiteStrategy('white',myBoard,history,count,printStatements=False)
                
            elif i%2==1:
                count = blackStrategy('black',myBoard,history,count,printStatements=False)
                        
            if threeMoveRep(history, myBoard):
                print "Stalemate!"
                myBoard.endGame()
                myBoard.winner = "stalemate"
        if myBoard.winner.lower() not in ['black','white','stalemate']:
            print "no winner assigned yet."
            if myBoard.isEndGame() and myBoard.whiteInCheck():
                myBoard.winner = "black"
            elif myBoard.isEndGame() and myBoard.blackInCheck():
                myBoard.winner = "white"
            else:
                myBoard.winner = "stalemate"
                
        if myBoard.winner.lower() == "stalemate":
            stalecount += 1.0
#            print "Stalemate"
        elif myBoard.winner.lower() == "white":
            whiteWins += 1.0
#            print "White wins"
        elif myBoard.winner.lower() == "black":
            blackWins += 1.0
#            print "Black wins"
#        print myBoard
        print "Percentages so far:"
        print "Black won",100.0*blackWins/(gameNumber+1),"% of the time."
        print "White won",100.0*whiteWins/(gameNumber+1),"% of the time."
        print "Stalemate",100.0*stalecount/(gameNumber+1),"% of the time."
    
    print "Final Percentages:"
    print "Black won",100.0*blackWins/numberOfTrials,"% of the time."
    print "White won",100.0*whiteWins/numberOfTrials,"% of the time."
    print "Stalemate",100.0*stalecount/numberOfTrials,"% of the time."

