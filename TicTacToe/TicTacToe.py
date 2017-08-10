# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 15:21:37 2017

@author: aokeke
"""

import numpy as np

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
                
if __name__=="__main__":
    playGame()
    