# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 15:21:37 2017

@author: aokeke
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import pickle as pkl

class TicTacToeBoard:
    def __init__(self,xPos = [],oPos = []):
        self.board = np.empty((3,3),dtype=str)
        for p in xPos:
            self.board[tuple(p)] = "X"
        for p in oPos:
            self.board[tuple(p)] = "O"
    
    def __hash__(self):
        return hash(self.board.tostring())
    
    def getXPos(self):
        return np.argwhere(self.board=="X")
    def getOPos(self):
        return np.argwhere(self.board=="O")
    def makeMove(self,position,player):
        if player=="X":
            xPosOld = self.getXPos()
            oPos = self.getOPos()
            xPos = np.zeros((len(xPosOld)+1,2),dtype=int)
            xPos[0:len(xPosOld),:] = xPosOld
            xPos[len(xPosOld),:] = position
        elif player=="O":
            xPos = self.getXPos()
            oPosOld = self.getOPos()
            oPos = np.zeros((len(oPosOld)+1,2),dtype=int)
            oPos[0:len(oPosOld),:] = oPosOld
            oPos[len(oPosOld),:] = position
        newBoard = TicTacToeBoard(xPos,oPos)
        return newBoard
    
    def checkIfWon(self,player):
        for i in range(3):
            if np.all(self.board[:,i]==player):
                return True
            if np.all(self.board[i,:]==player):
                return True
        if np.all(self.board[(0,1,2),(0,1,2)]==player):
            return True
        if np.all(self.board[(0,1,2),(2,1,0)]==player):
            return True
        return False
    def gameOver(self):
        if self.checkIfWon("X"):
            return 1
        if self.checkIfWon("O"):
            return 2
        if len(np.argwhere(self.board==""))==0:
            return 3
        return 0
    def getMoves(self):
        if self.gameOver()==0:
            tmoves = np.argwhere(self.board=="")
            moves=set()
            for m in tmoves:
                moves.add(tuple(m))
            return moves
        return set()
    
    def __eq__(self,other):
        if type(other)!=type(self):
            return False
        return np.all(self.board==other.board)
    def __neq__(self,other):
        return not(self.__eq__(other))
    def __str__(self):
        return " "+str(self.board)[1:-1]
    
def test1():
    x = TicTacToeBoard()
    print ("x\n",x)
    print ("x.getMoves()\n",x.getMoves())
    y = x.makeMove((0,0),"X")
    print ("x\n",x)
    print ("x.getMoves()\n",x.getMoves())
    print ("y\n",y)
    print ("y.getMoves()\n",y.getMoves())
    y = y.makeMove((1,1),"X")
    print ("y\n",y)
    print ("y.getMoves()\n",y.getMoves())
    y=y.makeMove((2,2),"X")
    print ("y\n",y)
    print ("y.getMoves()\n",y.getMoves())  
    
def playGame():
    XToMove = True
    game = TicTacToeBoard()
    history = []
    while game.gameOver()==0:
        history.append(game)
        if XToMove:
            player = "X"
        else:
            player = "O"
        print(player,"turn to move.")
        XToMove = not XToMove
        moves = game.getMoves()
        
        validMoveSelected = False
        print (game)
        while not validMoveSelected:
            m = input("Type 'quit' to exit.\nEnter a move in the form of x,y from [0,2]: ")
            try:
                if m=="quit":
                    return history
                elif m=="undo" and len(history)>1:
                    history.pop()
                    game = history.pop()
                    validMoveSelected = True
                else:
                    m = (int(m[0]),int(m[2]))
                    if m in moves:
                        validMoveSelected = True
                        game = game.makeMove(m,player)
                    else:
                        print ("This is not a valid move. Valid moves are:\n",moves)
            except:
                print("Invalid selection. Try again. (eg '1,0')")
    winner = game.gameOver()
    if winner==1:
        print("X Wins")
    elif winner==2:
        print ("O Wins")
    elif winner==3:
        print ("Draw")
    else:
        print ("Error?")
    return history
                

def trainOneGame(moveScoreDict={},temp=1,reinf=0):
    """
    moveScoreDict - dictionary that maps a game to a dictionary of moves mapping to their score and number of times that board was seen
    
    Plays one game and adjusts the moveScoreDict to make better moves more likely.
    """
    XToMove = True
    game = TicTacToeBoard()
    history = {"X":[],"O":[]}
    while game.gameOver()==0:
        if XToMove:
            player = "X"
        else:
            player = "O"
#        print(player,"turn to move.")
        XToMove = not XToMove
        moves = game.getMoves()
        
        #Add a new game and its moves to the dictionary
        if game not in moveScoreDict:
            tempScores= {}
            for m in moves:
                tempScores[m] = 0
            moveScoreDict[game] = {"scores":tempScores,"timesSeen":0}
        
        #Semirandomly choose a move
        moveSelected = chooseMove(game,moveScoreDict,temp=temp)
        history[player].append((game,moveSelected))
        game = game.makeMove(moveSelected,player)

    winner = game.gameOver()
#    if winner==1:
#        print("X Wins")
#    elif winner==2:
#        print ("O Wins")
#    elif winner==3:
#        print ("Draw")
    if winner not in [1,2,3]:
        print ("Error?")
        
    #adjust moveScoreDict based on who won
    if reinf==1:
        moveScoreDict = reinforce1(winner,history,moveScoreDict)
    elif reinf==2:
        moveScoreDict = reinforce2(winner,history,moveScoreDict)
    else:
        moveScoreDict = reinforce(winner,history,moveScoreDict)
    return moveScoreDict,winner

def chooseMove(game,moveScoreDict,temp=20):
    """
    game            - TicTacBoard
    moveScoreDict   - dictionary that maps a game to a dictionary of moves mapping to their score
    
    Semi-randomly chooses a move using a softmax function and moveScoreDict
    """
    scoresMapped = moveScoreDict[game]["scores"]
    scores = []
    moves = []
    for m in scoresMapped:
        scores.append(scoresMapped[m])
        moves.append(m)
    softmax = np.exp((scores - np.max(scores))/temp)/(np.sum(np.exp((scores - np.max(scores))/temp)))
#    print ("moves\t",moves)
#    print ("scores\t",scores)
#    print ("softmax\t",softmax)
#    print (game)
#    print ("softmax:",softmax)
#    print ("moves:",moves)
#    print ("list(range(len(moves))):",list(range(len(moves))))
    chosenIndex = np.random.choice(list(range(len(moves))),p=softmax)
    chosenMove = moves[chosenIndex]
    return chosenMove
def reinforce(winner,history,moveScoreDict,winWeight = 1,loseWeight=-1,drawWeight=0):
    """
    winner          - 1 = X Won, 2 = O won, 3 = Draw
    history         - dictionary that maps "X" and "O" to a list of [move,TicTacToeBoard]
    moveScoreDict   - dictionary that maps a game to a dictionary of moves mapping to their score
    
    Positively reinforces winning and negatively reinforces losing. Constant change
    """
    if winner==1:
        winPlayer = "X"
        losePlayer = "O"
        drawPlayer1 = "-"
        drawPlayer2 = "-"
    elif winner==2:
        winPlayer = "O"
        losePlayer = "X"
        drawPlayer1 = "-"
        drawPlayer2 = "-"
    elif winner==3:
        winPlayer = "-"
        losePlayer = "-"
        drawPlayer1 = "X"
        drawPlayer2 = "O"
    
    if winPlayer != "-":
        for b,m in history[winPlayer]:
            moveScoreDict[b]["timesSeen"] += 1
            moveScoreDict[b]["scores"][m] += winWeight
            
    if losePlayer != "-":
        for b,m in history[losePlayer]:
            moveScoreDict[b]["timesSeen"] += 1
            moveScoreDict[b]["scores"][m] += loseWeight
    if drawPlayer1 != "-":
        for b,m in history[drawPlayer1]:
            moveScoreDict[b]["timesSeen"] += 1
            moveScoreDict[b]["scores"][m] += drawWeight
    if drawPlayer2 != "-":
        for b,m in history[drawPlayer2]:
            moveScoreDict[b]["timesSeen"] += 1
            moveScoreDict[b]["scores"][m] += drawWeight   
    return moveScoreDict

def reinforce1(winner,history,moveScoreDict,winWeight = 1,loseWeight=-1,drawWeight=0):
    """
    winner          - 1 = X Won, 2 = O won, 3 = Draw
    history         - dictionary that maps "X" and "O" to a list of [move,TicTacToeBoard]
    moveScoreDict   - dictionary that maps a game to a dictionary of moves mapping to their score
    
    Positively reinforces winning and negatively reinforces losing. Linear Progression
    """
    if winner==1:
        winPlayer = "X"
        losePlayer = "O"
        drawPlayer1 = "-"
        drawPlayer2 = "-"
    elif winner==2:
        winPlayer = "O"
        losePlayer = "X"
        drawPlayer1 = "-"
        drawPlayer2 = "-"
    elif winner==3:
        winPlayer = "-"
        losePlayer = "-"
        drawPlayer1 = "X"
        drawPlayer2 = "O"
    
    if winPlayer != "-":
        for i,(b,m) in enumerate(history[winPlayer]):
            moveScoreDict[b]["timesSeen"] += 1
            moveScoreDict[b]["scores"][m] += winWeight*(i+1)/len(history[winPlayer])
            
    if losePlayer != "-":
        for i,(b,m) in enumerate(history[losePlayer]):
            moveScoreDict[b]["timesSeen"] += 1
            moveScoreDict[b]["scores"][m] += loseWeight*(i+1)/len(history[losePlayer])
    if drawPlayer1 != "-":
        for i,(b,m) in enumerate(history[drawPlayer1]):
            moveScoreDict[b]["timesSeen"] += 1
            moveScoreDict[b]["scores"][m] += drawWeight*(i+1)/len(history[drawPlayer1])
    if drawPlayer2 != "-":
        for i,(b,m) in enumerate(history[drawPlayer2]):
            moveScoreDict[b]["timesSeen"] += 1
            moveScoreDict[b]["scores"][m] += drawWeight*(i+1)/len(history[drawPlayer2])
    return moveScoreDict
def reinforce2(winner,history,moveScoreDict,winWeight = 1,loseWeight=-1,drawWeight=0):
    """
    winner          - 1 = X Won, 2 = O won, 3 = Draw
    history         - dictionary that maps "X" and "O" to a list of [move,TicTacToeBoard]
    moveScoreDict   - dictionary that maps a game to a dictionary of moves mapping to their score
    
    Positively reinforces winning and negatively reinforces losing. Quadratic progression.
    """
    if winner==1:
        winPlayer = "X"
        losePlayer = "O"
        drawPlayer1 = "-"
        drawPlayer2 = "-"
    elif winner==2:
        winPlayer = "O"
        losePlayer = "X"
        drawPlayer1 = "-"
        drawPlayer2 = "-"
    elif winner==3:
        winPlayer = "-"
        losePlayer = "-"
        drawPlayer1 = "X"
        drawPlayer2 = "O"
      
    F = 0.1
    F3 = 0.5 # F3<1
    F4 = 2 #F4>1
    C = F
    
    if winPlayer != "-":
        for i,(b,m) in enumerate(history[winPlayer]):
            moveScoreDict[b]["timesSeen"] += 1
            
            L = len(history[winPlayer])
            F2 = F3/((L+F4)*F) + 1  # F*(F2-1)/F3<1/L
            B = ((F2-1)*F + (F3**2)/(L**2)) / (F3 - (F3**2)/L)
            A = (1-L*B)/(L**2)
            adj = A*i*i+B*i+C
            moveScoreDict[b]["scores"][m] += winWeight*adj
            
    if losePlayer != "-":
        for i,(b,m) in enumerate(history[losePlayer]):
            moveScoreDict[b]["timesSeen"] += 1
            
            L = len(history[losePlayer])
            F2 = F3/((L+F4)*F) + 1  # F*(F2-1)/F3<1/L
            B = ((F2-1)*F + (F3**2)/(L**2)) / (F3 - (F3**2)/L)
            A = (1-L*B)/(L**2)
            adj = A*i*i+B*i+C
            moveScoreDict[b]["scores"][m] += loseWeight*adj
    if drawPlayer1 != "-":
        for i,(b,m) in enumerate(history[drawPlayer1]):
            moveScoreDict[b]["timesSeen"] += 1
            
            L = len(history[drawPlayer1])
            F2 = F3/((L+F4)*F) + 1  # F*(F2-1)/F3<1/L
            B = ((F2-1)*F + (F3**2)/(L**2)) / (F3 - (F3**2)/L)
            A = (1-L*B)/(L**2)
            adj = A*i*i+B*i+C
            moveScoreDict[b]["scores"][m] += drawWeight*adj
    if drawPlayer2 != "-":
        for i,(b,m) in enumerate(history[drawPlayer2]):
            moveScoreDict[b]["timesSeen"] += 1
            
            L = len(history[drawPlayer2])
            F2 = F3/((L+F4)*F) + 1  # F*(F2-1)/F3<1/L
            B = ((F2-1)*F + (F3**2)/(L**2)) / (F3 - (F3**2)/L)
            A = (1-L*B)/(L**2)
            adj = A*i*i+B*i+C
            moveScoreDict[b]["scores"][m] += drawWeight*adj 
    return moveScoreDict

def trainNTimes(n=1000,moveScoreDict = {},temp=1,reinf=0):
    print ("temp="+str(temp)+",n="+str(n)+",reinf="+str(reinf),flush=True)
    winnerInfo = [[0],[0],[0],[0]]
    winnerInfo2 = [[0],[0],[0],[0]]
    for i in range(n):
        moveScoreDict,winner = trainOneGame(moveScoreDict,temp=temp,reinf=reinf)
        winnerInfo[0].append(winnerInfo[0][-1]+1)
        for j in range(1,4):
            if j==winner:
                winnerInfo[j].append(winnerInfo[j][-1]+1)
            else:
                winnerInfo[j].append(winnerInfo[j][-1])
    for i in range(1,n+1):
        winnerInfo2[0].append(i)
        for j in range(1,4):
            winnerInfo2[j].append(winnerInfo[j][i]/i)
            
    plt.figure(1)                # the first figure
    plt.subplot(211)             # the first subplot in the first figure
    plt.plot(winnerInfo[0], winnerInfo[1],label="X Wins")
    plt.plot(winnerInfo[0], winnerInfo[2],label="O Wins")
    plt.plot(winnerInfo[0], winnerInfo[3],label="Draws")
    plt.legend()

    plt.subplot(212)             # the second subplot in the first figure
    plt.plot(winnerInfo2[0], winnerInfo2[1],label="X Wins")
    plt.plot(winnerInfo2[0], winnerInfo2[2],label="O Wins")
    plt.plot(winnerInfo2[0], winnerInfo2[3],label="Draws")
    plt.legend()
    print (len(moveScoreDict),"game boards seen")
    fileName = "temp="+str(temp)+",n="+str(n)+",reinf="+str(reinf)+","+time.ctime().replace(":","_")+".pkl"
    print ("data saved in fileName:",fileName)
    info = {"temp":temp,"n":n,"moveScoreDict":moveScoreDict}
    output = open(fileName,"wb")
    pkl.dump(info,output)
    output.close()

    return moveScoreDict

def playAI(fileName,AIPlayer="X"):
    
    #Load moveScoreDict
    info = pkl.load(open(fileName,"rb"))
    moveScoreDict = info["moveScoreDict"]
    
    
    XToMove = True
    game = TicTacToeBoard()
    history = []
    while game.gameOver()==0:
        history.append(game)
        if XToMove:
            player = "X"
        else:
            player = "O"
        print(player,"turn to move.")
        XToMove = not XToMove
        moves = game.getMoves()
        if AIPlayer!=player:
            validMoveSelected = False
            print (game)
            while not validMoveSelected:
                m = input("Type 'quit' to exit.\nEnter a move in the form of x,y from [0,2]: ")
                try:
                    if m=="quit":
                        return history
                    elif m=="undo" and len(history)>1:
                        history.pop()
                        game = history.pop()
                        validMoveSelected = True
                    else:
                        m = (int(m[0]),int(m[2]))
                        if m in moves:
                            validMoveSelected = True
                            game = game.makeMove(m,player)
                        else:
                            print ("This is not a valid move. Valid moves are:\n",moves)
                except:
                    print("Invalid selection. Try again. (eg '1,0')")
        else:
            #Add a new game and its moves to the dictionary
            if game not in moveScoreDict:
                print ("Game not previously seen!!!!!!!")
                tempScores= {}
                for m in moves:
                    tempScores[m] = 0
                moveScoreDict[game] = {"scores":tempScores,"timesSeen":0}
            
            #Semirandomly choose a move
            moveSelected = chooseMove(game,moveScoreDict,temp=0.001)
            game = game.makeMove(moveSelected,player)
    print (game)
    winner = game.gameOver()
    if winner==1:
        print("X Wins")
    elif winner==2:
        print ("O Wins")
    elif winner==3:
        print ("Draw")
    else:
        print ("Error?")
    return history

if __name__=="__main__":
#    playGame()
    np.random.seed(0)
#    moveScoreDict,winner = trainOneGame()
    moveScoreDict = trainNTimes(n=100000,temp=20,reinf=2)
#    fileName = "temp=20,n=100000,Thu Aug 10 11_46_39 2017.pkl"
#    fileName = "temp=40,n=1000000,Thu Aug 10 12_27_40 2017.pkl"
#    playAI(fileName,AIPlayer="O")
    pass