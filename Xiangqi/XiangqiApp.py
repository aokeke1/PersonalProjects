# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 20:46:51 2017

@author: arinz
"""
import tkinter as tk
from PIL import ImageTk,Image
import numpy as np
import Xiangqi1 as xq
import time

class XiangqiApp(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.createWidgets()
        self.pack()
        
    def createWidgets(self):
        self.gameBoard = tk.Frame(self)
        self.gameBoard.grid(row=0,column=0)
        
        self.imageSize = (60,60)
        self.hasSelectedPiece = False
        self.depth = 1
        self.gameOver = False
        self.gameType = 'pvc'
        

        
        self.infoLabel = tk.Label(self,text="Information will appear here.")
        self.infoLabel.grid(row=1,column=0)
        
        self.buttonPanel = tk.Frame(self)
        self.buttonPanel.grid(row=2,column=0)
        self.newGameButton = tk.Button(self.buttonPanel,text="New Game",command=self.newGame)
        self.newGameButton.grid(row=0,column=0)
        self.compMoveButton = tk.Button(self.buttonPanel,text="Make Computer Move",command=self.makeComputerMove)
        self.compMoveButton.grid(row=0,column=1)
        
        self.makeEmptySquareDict()
        self.makePieceImageDict()
        self.newGame(shouldDestroy=False)
        
    def makeEmptySquareDict(self):
        
        self.emptySquareDict = {}
        for r in range(10):
            for c in range(9):
                imageName = "("+str(r)+","+str(c)+")"
                image = Image.open("BoardImages/"+imageName+".png")
                tempImage = ImageTk.PhotoImage(image)
                self.emptySquareDict[(r,c)] = tempImage

    def makePieceImageDict(self):
        self.pieceDict = {}
        for i in range(-7,8):
            if i==0:
                continue
            image = Image.open("PieceImages/"+str(i)+".png")
            tempImage = ImageTk.PhotoImage(image)
            self.pieceDict[i] = tempImage

                
    def newGame(self,shouldDestroy=True):
        
        if shouldDestroy:
            for r in range(10):
                for c in range(9):
                   self.buttonGrid[r,c].destroy() 
        
        self.gameInfo = np.array([[-5, -4, -3, -2, -1, -2, -3, -4, -5],
                                  [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
                                  [ 0, -6,  0,  0,  0,  0,  0, -6,  0],
                                  [-7,  0, -7,  0, -7,  0, -7,  0, -7],
                                  [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
                                  [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
                                  [ 7,  0,  7,  0,  7,  0,  7,  0,  7],
                                  [ 0,  6,  0,  0,  0,  0,  0,  6,  0],
                                  [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
                                  [ 5,  4,  3,  2,  1,  2,  3,  4,  5]])
        self.playerToMove = 'red'
        self.validMoves = xq.get_valid_red_moves(self.gameInfo)
        
        self.buttonGrid = np.empty((10,9),dtype=tk.Button)
        for r in range(10):
            for c in range(9):
                tempButton = tk.Button(self.gameBoard,relief=tk.SUNKEN,highlightthickness = 0, bd = 0,bg="white")
                tempButton.grid(row=r,column=c)
                tempButton.bind('<Button-1>',self.movePiece)
                self.buttonGrid[r,c] = tempButton
                if self.gameInfo[r,c]==0:
                    tempButton.configure(image=self.emptySquareDict[(r,c)])
                else:
                    tempButton.configure(image=self.pieceDict[self.gameInfo[r,c]])
        if self.gameType[0]=='c':
            self.makeComputerMove()
                
    def movePiece(self,event):
        if not self.gameOver:
            if not self.hasSelectedPiece:
                self.posSelected = event.widget.grid_info()['row'],event.widget.grid_info()['column']
                if self.gameInfo[self.posSelected]!=0:
                    self.hasSelectedPiece = True
            else:
                self.hasSelectedPiece = False
                self.endPosSelected = event.widget.grid_info()['row'],event.widget.grid_info()['column']
                if self.posSelected in self.validMoves and self.endPosSelected in self.validMoves[self.posSelected]:
                    text = "Valid move selection: "+str((self.posSelected,self.endPosSelected))
                    piece = self.gameInfo[self.posSelected]
                    self.gameInfo[self.endPosSelected] = self.gameInfo[self.posSelected]
                    self.gameInfo[self.posSelected] = 0
                    self.buttonGrid[self.posSelected].configure(image=self.emptySquareDict[self.posSelected])
                    self.buttonGrid[self.endPosSelected].configure(image=self.pieceDict[piece])
                    
                    self.infoLabel['text'] = text
                    self.master.update_idletasks()
                    self.updateTurn()
                else:
                    text = "Invalid move selection: "+str((self.posSelected,self.endPosSelected))
                    self.infoLabel['text'] = text
                    self.master.update_idletasks()
                if self.gameOver:
                    if self.playerToMove=='red':
                         text = "Game Over. Black wins."
                    else:
                        text = "Game Over. Red wins."
                    self.infoLabel['text'] = text
                    self.master.update_idletasks()
                
    def updateTurn(self):
        if self.playerToMove=='red':
            self.playerToMove='black'
            self.validMoves = xq.get_valid_black_moves(self.gameInfo)
        else:
            self.playerToMove='red'
            self.validMoves = xq.get_valid_red_moves(self.gameInfo)
        if len(self.validMoves)==0:
            self.gameOver = True
        if self.gameType[0]=='c' and self.playerToMove=='red':
            self.makeComputerMove()
        elif self.gameType[2]=='c' and self.playerToMove=='black':
            self.makeComputerMove()
       
#        print(self.playerToMove+" turn to move.")
#        print("Valid Moves:",self.validMoves)

    def makeComputerMove(self):
        if not self.gameOver:
            start = time.time()
            best_move, score = xq.alpha_beta(self.gameInfo, self.depth, self.playerToMove, -float('inf'), float('inf'))
            end = time.time()
            square1,square2 = best_move
            #assume computer always makes valid moves
            piece = self.gameInfo[square1]
            print ('(piece,best_move)',(piece,best_move))
            self.gameInfo[square2] = self.gameInfo[square1]
            self.gameInfo[square1] = 0
            self.buttonGrid[square1].configure(image=self.emptySquareDict[square1])
            self.buttonGrid[square2].configure(image=self.pieceDict[piece])
            self.updateTurn()
            text = "This took " + str(round(end-start,2)) +" seconds. Score = "+str(score)
            if self.gameOver:
                if self.playerToMove=='red':
                     text += " Game Over. Black wins."
                else:
                    text += " Game Over. Red wins."
            self.infoLabel['text'] = text
        
        
root = tk.Tk()
app = XiangqiApp(root)
try:
    app.mainloop()
except:
    try:
        app.destroy()
    except:
        pass
    app.quit()
        