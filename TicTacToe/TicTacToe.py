# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 15:21:37 2017

@author: aokeke
"""

import numpy as np

class TicTacTieBoard:
    def init(self,xPos,oPos):
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