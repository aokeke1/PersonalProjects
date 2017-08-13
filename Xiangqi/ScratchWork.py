# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 20:46:51 2017

@author: arinz
"""
import tkinter as tk
from PIL import ImageTk,Image,ImageOps,ImageDraw
import numpy as np


class XiangqiApp(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.createWidgets()
        self.pack()
        
    def createWidgets(self):
        self.gameBoard = tk.Frame(self)
        self.gameBoard.grid(row=0,column=0)
        
        self.imageSize = (60,60)
        self.makeEmptySquareDict()
        self.makePieceImageDict()
        self.newGame(shouldDestroy=False)


#    def makeEmptySquareDict(self):
#        
#        image = Image.open("BoardImages/corner.png")
#
#        image = image.resize(self.imageSize,Image.ANTIALIAS)
#
#        self.cornerImage1 = ImageTk.PhotoImage(image)
#        image = image.rotate(90)
#        self.cornerImage2 = ImageTk.PhotoImage(image)
#        image = image.rotate(90)
#        self.cornerImage3 = ImageTk.PhotoImage(image)
#        image = image.rotate(90)
#        self.cornerImage4 = ImageTk.PhotoImage(image)
#        
#        image = Image.open("BoardImages/edge1.png")
#        image = image.resize(self.imageSize,Image.ANTIALIAS)
#        self.edge1 = ImageTk.PhotoImage(image)
#        image = image.rotate(90)
#        self.edge2 = ImageTk.PhotoImage(image)
#        image = image.rotate(90)
#        self.edge3 = ImageTk.PhotoImage(image)
#        image = image.rotate(90)
#        self.edge4 = ImageTk.PhotoImage(image)
#        
#
#        
#        image = Image.open("BoardImages/edge2.png")
#        image = image.resize(self.imageSize,Image.ANTIALIAS)
#        self.edge5 = ImageTk.PhotoImage(image)
#        image = image.rotate(180)
#        self.edge6 = ImageTk.PhotoImage(image)
#        image = image.rotate(180)
#        image = ImageOps.mirror(image)
#        self.edge7 = ImageTk.PhotoImage(image)
#        image = image.rotate(180)
#        self.edge8 = ImageTk.PhotoImage(image)
#
#        image = Image.open("BoardImages/middle2.png")
#        image = image.resize(self.imageSize,Image.ANTIALIAS)
#        self.mid1 = ImageTk.PhotoImage(image)
#        image = Image.open("BoardImages/middle1.png")
#        image = image.resize(self.imageSize,Image.ANTIALIAS)
#        self.mid2 = ImageTk.PhotoImage(image)
#        image = Image.open("BoardImages/middle3.png")
#        image = image.resize(self.imageSize,Image.ANTIALIAS)
#        self.mid3 = ImageTk.PhotoImage(image)
##        image = image.rotate(90)
#        image = ImageOps.mirror(image)
#        self.mid4 = ImageTk.PhotoImage(image)
#        image = image.rotate(90)
#        self.mid5 = ImageTk.PhotoImage(image)
##        image = image.rotate(90)
#        image = ImageOps.mirror(image)
#        self.mid6 = ImageTk.PhotoImage(image)
#        
#        self.emptySquareDict = {}
#        for r in range(10):
#            for c in range(9):
#                if (r==0 or r==5) and c==0:
#                    self.emptySquareDict[(r,c)] = self.cornerImage1
#                elif (r==9 or r==4) and c==0:
#                    self.emptySquareDict[(r,c)] = self.cornerImage2
#                elif (r==9 or r==4) and c==8:
#                    self.emptySquareDict[(r,c)] = self.cornerImage3
#                elif (r==0 or r==5) and c==8:
#                    self.emptySquareDict[(r,c)] = self.cornerImage4
#                elif r==0 and c==3:
#                    self.emptySquareDict[(r,c)] = self.edge5
#                elif r==0 and c==5:
#                    self.emptySquareDict[(r,c)] = self.edge7
#                elif r==9 and c==3:
#                    self.emptySquareDict[(r,c)] = self.edge8
#                elif r==9 and c==5:
#                    self.emptySquareDict[(r,c)] = self.edge6
#                elif (r==1 or r==8) and c==4:
#                    self.emptySquareDict[(r,c)] = self.mid1
#                elif r==2 and c==3:
#                    self.emptySquareDict[(r,c)] = self.mid3
#                elif r==2 and c==5:
#                    self.emptySquareDict[(r,c)] = self.mid4
#                elif r==7 and c==3:
#                    self.emptySquareDict[(r,c)] = self.mid6
#                elif r==7 and c==5:
#                    self.emptySquareDict[(r,c)] = self.mid5
#                elif c==0:
#                    self.emptySquareDict[(r,c)] = self.edge2
#                elif c==8:
#                    self.emptySquareDict[(r,c)] = self.edge4
#                elif r==4 or r==9:
#                    self.emptySquareDict[(r,c)] = self.edge3
#                elif r==5 or r==0:
#                    self.emptySquareDict[(r,c)] = self.edge1
#                else:
#                    self.emptySquareDict[(r,c)] = self.mid2
    def makeEmptySquareDict(self):
        
        self.emptySquareDict = {}
        for r in range(10):
            for c in range(9):
                imageName = "("+str(r)+","+str(c)+")"
                image = Image.open("BoardImages2/"+imageName+".png")
                tempImage = ImageTk.PhotoImage(image)
                self.emptySquareDict[(r,c)] = tempImage

#    def makePieceImageDict(self):
#        self.pieceDict = {}
#        image = Image.open("Unused/pieces.png")
#        imageWidth,imageHeight = image.size
#        w = int(imageWidth/7)
#        h = int(imageHeight/2)
#        print ('(imageWidth,imageHeight)',(imageWidth,imageHeight))
#        print ('(w,h)',(w,h))
#        size1 = (int(w), int(h))
#        size2 = (int(w/2), int(h/2))
##        print ("size",size)
#        mask = Image.new('L', size1, 0)
#        draw = ImageDraw.Draw(mask) 
#        draw.ellipse((0, 0) + size1, fill=255)
#        tempImage = image.crop((0, 0, w, h))
#        output = ImageOps.fit(tempImage, mask.size, centering=(0.5, 0.5))
#        output.putalpha(mask)
#        output = output.resize(self.imageSize,Image.ANTIALIAS)
#        output.save('output.png')
#
##        for i in range(-7,8):
##            if i==0:
##                continue
##            if i>0:
##                yMin = 0
##                yMax = h
##            else:
##                yMin = h
##                yMax = 2*h
##            if abs(i)==7:
##                xMin = 6*w
##                xMax = 7*w
##            elif abs(i)==6:
##                xMin = 5*w
##                xMax = 6*w
##            elif abs(i)==5:
##                xMin = 4*w
##                xMax = 5*w
##            elif abs(i)==4:
##                xMin = 2*w
##                xMax = 3*w
##            elif abs(i)==3:
##                xMin = 3*w
##                xMax = 4*w
##            elif abs(i)==2:
##                xMin = w
##                xMax = 2*w
##            elif abs(i)==1:
##                xMin = 0
##                xMax = w
##            tempImage = image.crop((xMin, yMin, xMax, yMax))
##            output = ImageOps.fit(tempImage, mask.size, centering=(0.5, 0.5))
##            output.putalpha(mask)
##            output = output.resize(self.imageSize,Image.ANTIALIAS)
##            output.save(str(i)+'.png')
#    def makePieceImageDict(self):
#        self.pieceDict = {}
##        image = Image.open("Unused/Xiang_board2.png")
#        image = Image.open("Unused/koreanboard2.png")
#        image = ImageOps.expand(image, border=12, fill=255)
#        imageWidth,imageHeight = image.size
#        deltaW = 0
#        deltaH = 0
#        w = int((imageWidth-deltaW)/9)
#        h = int((imageHeight-deltaH)/10)
#
#        for r in range(10):
#            for c in range(9):
##                output = image.crop((r*w+deltaW, c*h+deltaH, (r+1)*w+deltaW, (c+1)*h+deltaH))
#                output = image.crop((c*h+deltaH, r*w+deltaW, (c+1)*h+deltaH, (r+1)*w+deltaW))
#                output = output.resize(self.imageSize,Image.ANTIALIAS)
#                output.save('BoardImages2/('+str(r)+','+str(c)+').png')

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
        self.buttonGrid = np.empty((10,9),dtype=tk.Button)
        for r in range(10):
            for c in range(9):
                tempButton = tk.Button(self.gameBoard,relief=tk.SUNKEN,highlightthickness = 0, bd = 0,bg="white")
                tempButton.grid(row=r,column=c)
                self.buttonGrid[r,c] = tempButton
                if self.gameInfo[r,c]==0:
                    tempButton.configure(image=self.emptySquareDict[(r,c)])
                else:
#                    background = self.emptySquareDict[(r,c)]
#                    foreground = self.pieceDict[self.gameInfo[r,c]]
#                    background.paste(foreground, (0, 0))
#                    tempButton.configure(image=background)
##                    composite = Image.alpha_composite(background, foreground)
##                    tempButton.configure(image=background)
                    tempButton.configure(image=self.pieceDict[self.gameInfo[r,c]])
        
        
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
        