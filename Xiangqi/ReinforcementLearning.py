# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 08:51:38 2017

@author: arinz
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import pickle as pkl
import operator
import cProfile
import Xiangqi as XQ

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

def reformatMoves(moves):
    moveSet = set()
    for start in moves:
        for end in moves[start]:
            moveSet.add((start,end))
    return moveSet


def trainOneGame(moveScoreDict={},temp=1,chanceToRandom = 0.5,reinforceParameters=None):
    """
    moveScoreDict - dictionary that maps a game to a dictionary of moves mapping to their score and number of times that board was seen
    
    Plays one game and adjusts the moveScoreDict to make better moves more likely.
    """
    try:
        RToMove = True
        game = XQ.Xiangqi()
        history = {"R":[],"B":[]}
        history2 = {"R":{},"B":{}}
        moveCount = 0
        while True:
            moveCount += 1
            if RToMove:
                player = "R"
                moves = game.get_valid_red_moves()
                moves = reformatMoves(moves)
                if len(moves)==0:
                    winner = 2
                    #Player who just made the move wins
                    break
            else:
                player = "B"
                moves = game.get_valid_black_moves()
                moves = reformatMoves(moves)
                if len(moves)==0:
                    winner = 1
                    #Player who just made the move wins
                    break
    
    #        print(player,"turn to move.")
            RToMove = not RToMove
            
            
            #Add a new game and its moves to the dictionary
            if (game,player) not in moveScoreDict:
                tempScores= {}
                for m in moves:
                    tempScores[m] = 0
                moveScoreDict[(game,player)] = {"scores":tempScores,"timesSeen":0}
            
            #Semirandomly choose a move
            moveSelected = chooseMove((game,player),moveScoreDict,temp=temp,chanceToRandom = chanceToRandom)
                
            if (game,moveSelected) not in history2[player]:
                history2[player][(game,moveSelected)] = 1
            elif history2[player][(game,moveSelected)]>=3:
                #Draw?
                winner = 3
                break
            else:
                history2[player][(game,moveSelected)] += 1
            history[player].append((game,moveSelected))
            
            game = game.make_move(moveSelected[0],moveSelected[1])
    
#        print (moveCount,"moves made")
#        if winner==1:
#            print("R Wins")
#        elif winner==2:
#            print ("B Wins")
#        elif winner==3:
#            print ("Draw")
#        else:
#            print ("Error?")
            
        #adjust moveScoreDict based on who won
        moveScoreDict = reinforce(winner,history,moveScoreDict,reinforceParameters)
        return moveScoreDict,winner
    except IndexError:
        minLook = 0
        maxLook = len(history["R"])+len(history["B"])
        if maxLook>100:
            minLook=maxLook-15
        for i in range(minLook,maxLook):
            if i%2==0:
                game,move = history["R"][i//2]
                player = "R"
                allMoves = game.get_valid_red_moves()
            else:
                game,move = history["B"][i//2]
                player ="B"
                allMoves = game.get_valid_black_moves()
            
            print ("Move number",i+1)
            print (game)
            print ("allMoves:",allMoves)
            print (player,"made move:",move)
            print ("---------------------")
        print("moveCount:",moveCount)
        print ("RToMove",RToMove)
        print ("moves",moves)
        print ("Current Board:")
        print (game)
        raise IndexError
def chooseMove(gameAndPlayer,moveScoreDict,temp=1,chanceToRandom = 0.5):
    """
    game            - TicTacBoard
    moveScoreDict   - dictionary that maps a game to a dictionary of moves mapping to their score
    
    Semi-randomly chooses a move using a softmax function and moveScoreDict
    """
    scoresMapped = moveScoreDict[gameAndPlayer]["scores"]
    scores = []
    moves = []
    for m in scoresMapped:
        scores.append(scoresMapped[m])
        moves.append(m)
    if np.random.random()<chanceToRandom:
        scores = np.zeros((len(scores),))
    softmax = np.exp((scores - np.max(scores))/temp)/(np.sum(np.exp((scores - np.max(scores))/temp)))
    chosenIndex = np.random.choice(list(range(len(moves))),p=softmax)
    chosenMove = moves[chosenIndex]
    return chosenMove

def reinforce(winner,history,moveScoreDict,reinforceParameters=None):
    """
    winner          - 1 = R Won, 2 = B won, 3 = Draw
    history         - dictionary that maps "X" and "O" to a list of [move,TicTacToeBoard]
    moveScoreDict   - dictionary that maps a game to a dictionary of moves mapping to their score
    
    Positively reinforces winning and negatively reinforces losing. Exponential Progression
    """
    if reinforceParameters is None:
        reinforceParameters = {"winWeight":1e6,"loseWeight":-1e6,"drawWeight":0.5,"gamma":0.8}
    
    if winner==1:
        winPlayer = "R"
        losePlayer = "B"
        drawPlayer1 = "-"
        drawPlayer2 = "-"
    elif winner==2:
        winPlayer = "B"
        losePlayer = "R"
        drawPlayer1 = "-"
        drawPlayer2 = "-"
    elif winner==3:
        winPlayer = "-"
        losePlayer = "-"
        drawPlayer1 = "R"
        drawPlayer2 = "B"
    
    if winPlayer != "-":
        for i,(b,m) in enumerate(history[winPlayer]):
            moveScoreDict[(b,winPlayer)]["timesSeen"] += 1
            moveScoreDict[(b,winPlayer)]["scores"][m] += reinforceParameters["winWeight"]*(reinforceParameters["gamma"]**(len(history[winPlayer])-1-i))
            
    if losePlayer != "-":
        for i,(b,m) in enumerate(history[losePlayer]):
            moveScoreDict[(b,losePlayer)]["timesSeen"] += 1
            moveScoreDict[(b,losePlayer)]["scores"][m] += reinforceParameters["loseWeight"]*(reinforceParameters["gamma"]**(len(history[losePlayer])-1-i))

    if drawPlayer1 != "-":
        for i,(b,m) in enumerate(history[drawPlayer1]):
            moveScoreDict[(b,drawPlayer1)]["timesSeen"] += 1
            moveScoreDict[(b,drawPlayer1)]["scores"][m] *= reinforceParameters["drawWeight"]
    if drawPlayer2 != "-":
        for i,(b,m) in enumerate(history[drawPlayer2]):
            moveScoreDict[(b,drawPlayer2)]["timesSeen"] += 1
            moveScoreDict[(b,drawPlayer2)]["scores"][m] *= reinforceParameters["drawWeight"]
    return moveScoreDict

def trainNTimes(n=1000,temp=1,chanceToRandom = 0.5,shouldSave=False,startingDictFileName = None,reinforceParameters=None):
    if startingDictFileName is not None:
        try:
            #Load moveScoreDict
            info = pkl.load(open(startingDictFileName,"rb"))
            moveScoreDict = info["moveScoreDict"]
        except:
            moveScoreDict = {}
    else:
        moveScoreDict = {}
    start = time.time()
    print ("temp="+str(temp)+",n="+str(n)+",chanceToRandom="+str(chanceToRandom),flush=True)
    winnerInfo = [[0],[0],[0],[0]]
    winnerInfo2 = [[0],[0],[0],[0]]
    try:
        for i in range(n):
    #        print ("i =",i)
            if n>100:
                if i%(n//50)==0:
                    print (100*i/n,"% complete",flush=True)
                    print (len(moveScoreDict),"boards seen so far",flush=True)
                    print (time.time()-start,"seconds have elapsed")
            moveScoreDict,winner = trainOneGame(moveScoreDict,temp=temp,chanceToRandom=chanceToRandom,reinforceParameters=reinforceParameters)
            winnerInfo[0].append(winnerInfo[0][-1]+1)
            for j in range(1,4):
                if j==winner:
                    winnerInfo[j].append(winnerInfo[j][-1]+1)
                else:
                    winnerInfo[j].append(winnerInfo[j][-1])
    except KeyboardInterrupt:
        #Stop short
        pass
    for i in range(1,len(winnerInfo[0])):
        winnerInfo2[0].append(i)
        for j in range(1,4):
            winnerInfo2[j].append(winnerInfo[j][i]/i)
            
    plt.figure(1)                # the first figure
    plt.subplot(211)             # the first subplot in the first figure
    plt.plot(winnerInfo[0], winnerInfo[1],label="R Wins")
    plt.plot(winnerInfo[0], winnerInfo[2],label="B Wins")
    plt.plot(winnerInfo[0], winnerInfo[3],label="Draws")
    plt.legend()

    plt.subplot(212)             # the second subplot in the first figure
    plt.plot(winnerInfo2[0], winnerInfo2[1],label="R Wins")
    plt.plot(winnerInfo2[0], winnerInfo2[2],label="B Wins")
    plt.plot(winnerInfo2[0], winnerInfo2[3],label="Draws")
    plt.legend()
    print (len(moveScoreDict),"game boards seen")

    if shouldSave:
        fileName = "temp="+str(temp)+",n="+str(n)+",chanceToRandom="+str(chanceToRandom)+","+time.ctime().replace(":","_")+".pkl"
        print ("data saved in fileName:",fileName)
        info = {"temp":temp,"n":n,"moveScoreDict":moveScoreDict}
        output = open(fileName,"wb")
        pkl.dump(info,output)
        output.close()
    print ("This took",time.time()-start,"seconds")
    return moveScoreDict

if __name__=="__main__":
    np.random.seed(1)
#    myBoard = XQ.Xiangqi()
#    blackMoves = myBoard.get_valid_black_moves()
#    redMoves = myBoard.get_valid_red_moves()
#    
#    print (myBoard)
#    print (blackMoves)
#    print (redMoves)
    
#    moveScoreDict,winner = trainOneGame(moveScoreDict={},temp=1,chanceToRandom = 0.5)
    
#    print (moveScoreDict)
#    print (winner)
    
    reinforceParameters = {"winWeight":50,"loseWeight":-50,"drawWeight":0.5,"gamma":0.95}
#    reinforceParameters = None
    moveScoreDict = trainNTimes(n=100,temp=1,chanceToRandom = 0,shouldSave=True,startingDictFileName = None,reinforceParameters=reinforceParameters)
    myBoard = XQ.Xiangqi()
    print (moveScoreDict[(myBoard,"R")])