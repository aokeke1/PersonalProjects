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
            self.board[p] = "X"
        for p in oPos:
            self.board[p] = "O"
    
    def __hash__(self):
        return hash(self.board.tostring())
    
    def getXPos(self):
        return np.argwhere(self.board=="X")
    def getOPos(self):
        return np.argwhere(self.board=="O")
    def makeMove(self,position,team):
        if team=="X":
            xPosOld = self.getXPos()
            oPos = self.getOPos()
            xPos = np.zeros((len(xPosOld)+1,2),dtype=int)
            xPos[0:len(xPosOld),:] = xPosOld
            xPos[len(xPosOld),:] = position
        elif team=="O":
            xPos = self.getXPos()
            oPosOld = self.getOPos()
            oPos = np.zeros((len(oPosOld)+1,2),dtype=int)
            oPos[0:len(oPosOld),:] = xPosOld
            oPos[len(oPosOld),:] = position
        newBoard = self.init(xPos,oPos)
        return newBoard
    def __str__(self):
        return " "+str(self.board)[1:-1]