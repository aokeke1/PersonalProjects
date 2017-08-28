import Pieces
import ChessBoard
import copy, time, random

def startGame():
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
        i += 1                    
        if i%2==0:
            #white turn
            print "It is white's turn to move."
            x = 0
            while x not in ['1','3','4']:
                x = raw_input("Choose an option:\n1.Make move\n2.Check possible moves for a piece\n3.Undo last move\n4.Redo\nYour choice:")
                print ""
                #check possible moves
                if x == '2':
                    square = raw_input("What is the square you want to check the moves for:")
                    print ""
                    myBoard.checkWhitePossibleMoves(square)
                    print ""

            #Move
            if x == '1':
                start = raw_input("Select starting square:")
                end = raw_input("Select ending square:")
                print ""
                a = myBoard.whiteMove(start, end)
                if a[0] == "Good":
                    redo = []
                    history.append(copy.deepcopy(myBoard))
                    print ""
                    print myBoard
                    print ""
                    if myBoard.blackInCheck():
                        print "Black is in check!\n"
                    if a[1] or a[2]:
                        count = 0
                    elif not(a[1]) and not(a[2]):
                        count += 1
                        if count >=50:
                            print "50 moves with no pawn movement or captue.\nStalemate!"
                            myBoard.endGame()
                else:
                    print "Please try again.\n"
                    i -= 1

            #undo
            if x == '3':
                if len(history)>=2:
                    i= i-2
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
                if len(redo)>=1:
                    history.append(copy.deepcopy(redo.pop()))
                    myBoard = copy.deepcopy(history[-1])
                    print ""
                    print myBoard
                    print ""
                else:
                    print "Nothing to redo.\n"
                    i -= 1
        elif i%2==1:
            #black turn
            print "It is black's turn to move."
            x = 0
            while x not in ['1','3','4']:
                x = raw_input("Choose an option:\n1.Make move\n2.Check possible moves for a piece\n3.Undo last move\n4.Redo\nYour choice:")
                print ""
                #check possible moves
                if x == '2':
                    square = raw_input("What is the square you want to check the moves for:")
                    print ""
                    myBoard.checkBlackPossibleMoves(square)
                    print ""
                    
            #Move
            if x == '1':
                start = raw_input("Select starting square:")
                end = raw_input("Select ending square:")
                print ""
                a = myBoard.blackMove(start, end)
                if a[0] == "Good":
                    redo = []
                    history.append(copy.deepcopy(myBoard))
                    print ""
                    print myBoard
                    print ""
                    if myBoard.whiteInCheck():
                        print "White is in check!\n"
                    if a[1] or a[2]:
                        count = 0
                    elif not(a[1]) and not(a[2]):
                        count += 1
                        if count >=50:
                            print "50 moves with no pawn movement or captue.\nStalemate!"
                            myBoard.endGame()
                else:
                    print "Please try again.\n"
                    i -= 1

            #undo
            if x == '3':
                if len(history)>=2:
                    i= i-2
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
                if len(redo)>=1:
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
            while answer not in ["1","2"]:
                answer = raw_input("Would you like to draw?\n1.Yes\n2.No\nYour choice:")
                print ""
                if answer == "1":
                    print "Stalemate!"
                    myBoard.endGame()
                if answer == "2":
                    print "Will continue game.\n"
        
def threeMoveRep(history, myBoard):
    count = 0
    for b in history:
        if myBoard == b:
            count += 1
            if count >=3:
                print count
                return True
    print count
    return False
