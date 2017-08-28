import Tkinter as tk
from PIL import ImageTk, Image
import copy
import ChessBoard, Pieces, wrapper

def coordToSquare(coord):
    #Converts coordinate to move format with letter
    if coord[0] in range(8) and coord[1] in range(8):
        row = 8-coord[0]
        col = "ABCDEFGH"[coord[1]]
        return col+str(row)
    print coord
    print "This isn't a valid coord"
def squareToCoord(square):
    #Converts move format with letter to coordinate
    if square[0] in "ABCDEFGH" and square[1] in "12345678":
        return (8-int(square[1]),"ABCDEFGH".find(square[0]))
    print square
    print "This isn't a valid square"

class simpleapp_tk(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.count = 0
        self.initialize()

        

    def initialize(self):
        self.grid()

        #load all the pictures
        self.darkSquare = ImageTk.PhotoImage(Image.open('darkSquare.jpg'))
        self.lightSquare = ImageTk.PhotoImage(Image.open('lightSquare.jpg'))
        self.whiteKingDark = ImageTk.PhotoImage(Image.open('whiteKingDark.jpg'))
        self.whiteKingLight = ImageTk.PhotoImage(Image.open('whiteKingLight.jpg'))
        self.blackKingDark = ImageTk.PhotoImage(Image.open('blackKingDark.jpg'))
        self.blackKingLight = ImageTk.PhotoImage(Image.open('blackKingLight.jpg'))
        self.whiteQueenDark = ImageTk.PhotoImage(Image.open('whiteQueenDark.jpg'))
        self.whiteQueenLight = ImageTk.PhotoImage(Image.open('whiteQueenLight.jpg'))
        self.blackQueenDark = ImageTk.PhotoImage(Image.open('blackQueenDark.jpg'))
        self.blackQueenLight = ImageTk.PhotoImage(Image.open('blackQueenLight.jpg'))
        self.whiteRookDark = ImageTk.PhotoImage(Image.open('whiteRookDark.jpg'))
        self.whiteRookLight = ImageTk.PhotoImage(Image.open('whiteRookLight.jpg'))
        self.blackRookDark = ImageTk.PhotoImage(Image.open('blackRookDark.jpg'))
        self.blackRookLight = ImageTk.PhotoImage(Image.open('blackRookLight.jpg'))
        self.whiteBishopDark = ImageTk.PhotoImage(Image.open('whiteBishopDark.jpg'))
        self.whiteBishopLight = ImageTk.PhotoImage(Image.open('whiteBishopLight.jpg'))
        self.blackBishopDark = ImageTk.PhotoImage(Image.open('blackBishopDark.jpg'))
        self.blackBishopLight = ImageTk.PhotoImage(Image.open('blackBishopLight.jpg'))
        self.whiteKnightDark = ImageTk.PhotoImage(Image.open('whiteKnightDark.jpg'))
        self.whiteKnightLight = ImageTk.PhotoImage(Image.open('whiteKnightLight.jpg'))
        self.blackKnightDark = ImageTk.PhotoImage(Image.open('blackKnightDark.jpg'))
        self.blackKnightLight = ImageTk.PhotoImage(Image.open('blackKnightLight.jpg'))
        self.whitePawnDark = ImageTk.PhotoImage(Image.open('whitePawnDark.jpg'))
        self.whitePawnLight = ImageTk.PhotoImage(Image.open('whitePawnLight.jpg'))
        self.blackPawnDark = ImageTk.PhotoImage(Image.open('blackPawnDark.jpg'))
        self.blackPawnLight = ImageTk.PhotoImage(Image.open('blackPawnLight.jpg'))
        
        self.letters = ["A","B","C","D","E","F","G","H"]
        self.numbers = ["8","7","6","5","4","3","2","1"]
##        self.blankBoard()
        self.moveSelection = []
        self.checkList = []
        self.checkCond = False
        self.moveCond = False
        self.turns = 0
        self.history = []
        self.redo = []
        self.myBoard = ChessBoard.Board()
        self.instructions = tk.StringVar()
        self.turnLabel = tk.StringVar()
        self.win = None
##        print "???"
        self.updateBoardLayout()
        self.history.append(copy.deepcopy(self.myBoard))
        self.count = 0
        self.pawnCond = False
        self.instructions.set("Game Start")


        #Make Move Button
        button = tk.Button(self, command=self.makeMove, text="Make Move",width=15)
        button.grid(column=1,row=9,columnspan=2)
        #Check Move Button
        button = tk.Button(self, command=self.checkMoves, text="Check Valid Moves",width=15)
        button.grid(column=3,row=9,columnspan=2)
        #Undo Button
        button = tk.Button(self, command=self.undo, text="Undo",width=7)
        button.grid(column=5,row=9,columnspan=1)
        #Redo Button
        button = tk.Button(self, command=self.redoMove, text="Redo",width=7)
        button.grid(column=6,row=9,columnspan=1)
        #New Game Button
        button = tk.Button(self, command=self.newGame, text="New Game",width=15)
        button.grid(column=7,row=9,columnspan=2)

        #PawnFates
        button = tk.Button(self, text="Knight",width=15)
        button["command"] = lambda x=1 :self.pawnChoiceButton(x)
        button.grid(column=1,row=10,columnspan=2)
        button = tk.Button(self, text="Bishop",width=15)
        button["command"] = lambda x=2 :self.pawnChoiceButton(x)
        button.grid(column=3,row=10,columnspan=2)
        button = tk.Button(self, text="Rook",width=15)
        button["command"] = lambda x=3 :self.pawnChoiceButton(x)
        button.grid(column=5,row=10,columnspan=2)
        button = tk.Button(self, text="Queen",width=15)
        button["command"] = lambda x=4 :self.pawnChoiceButton(x)
        button.grid(column=7,row=10,columnspan=2)

##        self.option1 = tk.StringVar()
##        self.option2 = tk.StringVar()
##        self.option3 = tk.StringVar()
##        self.option4 = tk.StringVar()
##        button = tk.Button(self, command=self.OnButtonClick, textvariable=self.option1,width=15)
##        button.grid(column=1,row=10,columnspan=2)
##        button = tk.Button(self, command=self.OnButtonClick, textvariable=self.option2,width=15)
##        button.grid(column=3,row=10,columnspan=2)
##        button = tk.Button(self, command=self.OnButtonClick, textvariable=self.option3,width=15)
##        button.grid(column=5,row=10,columnspan=2)
##        button = tk.Button(self, command=self.OnButtonClick, textvariable=self.option4,width=15)
##        button.grid(column=7,row=10,columnspan=2)

        
        #Where the instructions are displayed
        self.label2 = tk.Label(self,textvariable=self.instructions,fg="black",bg="white")
        self.label2.grid(column=0,row=12,columnspan=9,rowspan=1,sticky="EW")
        #Where the instructions are displayed

        self.label1 = tk.Label(self,textvariable=self.turnLabel,fg="black",bg="white")
        self.label1.grid(column=0,row=11,columnspan=9,rowspan=1,sticky="EW")
        
        #no resizing window allowed
        self.resizable(False,False)
        #prevents the window from changing sizes to match the text
        self.update()
        self.geometry(self.geometry())

    def OnButtonClick(self,val):
##        pass
##        print "Here"
        if self.pawnCond:
            self.instructions.set("Nothing can be done until the pawn is upgraded.")
            return
        x = val/10
        y = val%10
        coord = (x,y)
        square = coordToSquare(coord)
        if self.moveCond:
##            print "Here1"
            self.moveSelection.append(square)
            if len(self.moveSelection) == 1:
                self.instructions.set("Select the square you want to move to.")
            elif len(self.moveSelection) == 2:
                self.instructions.set("Your move is: "+self.moveSelection[0]+" to "+self.moveSelection[1])
##                print "Click 'Confirm' if this is correct."
                self.confirmMove(self.moveSelection[0],self.moveSelection[1])
##                self.moveSelection = []
##                self.moveCond = False
        elif self.checkCond:
##            print "Here2"
            print "Checking the moves for",square
            if self.turns%2==0:
                result = self.myBoard.checkWhitePossibleMoves(square)
            else:
                result = self.myBoard.checkBlackPossibleMoves(square)
            if result != None:
                self.instructions.set(str(result[0])+" : "+str(result[1]))
            elif result == None:
                self.instructions.set("Either this is not your piece or there is no piece in this square.")
            self.checkCond = False

    def pawnChoiceButton(self, val):
        piece = self.updatePawnCond()
        winner = None
        if self.pawnCond:
            piece.chooseTrans(val)
            #Remove the last board update and replace it with the board after you have
            #chosen the upgrade
            self.history.pop()
            self.history.append(copy.deepcopy(self.myBoard))
            self.updateBoardLayout()
            if self.myBoard.blackInCheck():
                self.instructions.set("Black is in check!")
            if self.myBoard.whiteInCheck():
                self.instructions.set("White is in check!")
            if not(self.myBoard.whiteHasMoves()):
                if not(self.myBoard.whiteInCheck()):
                    print "Stalemate!"
                    winner = self.myBoard.endGame("Stalemate!")
                elif self.myBoard.whiteInCheck():
                    print "Checkmate! Black wins!"
                    winner = self.myBoard.endGame("Checkmate! Black wins!")
            if self.myBoard.isEndGame():
                if winner != None:
                    self.winner = winner
                print self.winner
                self.endIt()
            self.pawnCond = False
        elif not(self.pawnCond):
            print "You don't have any pawns that can be upgraded."
        

    def updatePawnCond(self):
        #updates pawn condition and returns the pawn if there is a pawn
        for piece in self.myBoard.getAllRemainingPieces():
            if piece == "Pawn":
                if piece.getPosition()[1] == "1" or piece.getPosition()[1] == "8":
                    self.pawnCond = True
                    return piece
        
    def confirmMove(self, start, end):
        if self.pawnCond:
            self.instructions.set("Nothing can be done until the pawn is upgraded.")
            return
        if self.turns%2==0:
            a = self.myBoard.whiteMove(start, end)
            if a[0] == "Good":
                self.turns += 1
                self.redo = []
                self.history.append(copy.deepcopy(self.myBoard))
                self.updateBoardLayout()
                if self.myBoard.blackInCheck():
                    self.instructions.set("Black is in check!")
                if self.myBoard.winner != None:
                    self.win = self.myBoard.winner
                if a[1] or a[2]:
                    self.count = 0
                elif not(a[1]) and not(a[2]):
                    self.count += 1
                    if self.count>=50:
                        print "50 moves with no pawn movement or captue."
                        self.win = "50 Moves Stalemate"
                        self.myBoard.endGame()
                        self.endIt()
                self.updatePawnCond()
                if self.pawnCond:
                    self.instructions.set("Choose what you want your pawn to turn into.")
                    
            else:
                self.instructions.set("This is not a valid move. Please try again.")
                
        else:
            a = self.myBoard.blackMove(start, end)
            if a[0] == "Good":
                self.turns += 1
                self.redo = []
                self.history.append(copy.deepcopy(self.myBoard))
                self.updateBoardLayout()
                if self.myBoard.whiteInCheck():
                    self.instructions.set("White is in check!")
                if self.myBoard.winner != None:
                    self.win = self.myBoard.winner
                if a[1] or a[2]:
                    self.count = 0
                elif not(a[1]) and not(a[2]):
                    self.count += 1
                    if self.count>=50:
                        print "50 moves with no pawn movement or captue.\nStalemate!"
                        self.win = "50 Moves Stalemate"
                        self.myBoard.endGame()
                        self.endIt()
            else:
                self.instructions.set("This is not a valid move. Please try again.")
        if a[0] == "Good":
            self.updatePawnCond()
            if self.pawnCond:
                self.instructions.set("Choose what you want your pawn to turn into.")
        if self.myBoard.isEndGame():
##            print self.win
            self.endIt()
##        print self.win, "winner"
        self.moveSelection = []
        self.moveCond = False
        
    def endIt(self):
##        pass
##        print self.myBoard.winner
##        print self.win
##        print "here123"
        
        if not(self.myBoard.whiteHasMoves()):
            if not(self.myBoard.whiteInCheck()):
##                print "Stalemate!"
                self.win = "Stalemate!"
            elif self.myBoard.whiteInCheck():
##                print "Checkmate! Black wins!"
                self.win = "Checkmate! Black wins!"
                
        if not(self.myBoard.blackHasMoves()):
            if not(self.myBoard.blackInCheck()):
##                print "Stalemate!"
                self.win = "Stalemate!"
            elif self.myBoard.blackInCheck():
##                print "Checkmate! White wins!"
                self.win = "Checkmate! White wins!"
                
##        print self.myBoard.winner
##        print self.win
##        print "here223"
        
        if self.myBoard.winner != None:
            self.winner = self.myBoard.winner
        self.instructions.set("Game Over: "+str(self.win))
    def makeMove(self):
        if self.pawnCond:
            self.instructions.set("Nothing can be done until the pawn is upgraded.")
            return
##        print "Here3"
        self.moveCond = True
        self.checkCond = False
        self.checkList = []
        self.instructions.set("Select the piece you want to move.")
    def checkMoves(self):
        if self.pawnCond:
            self.instructions.set("Nothing can be done until the pawn is upgraded.")
            return
##        print "Here4"
        self.checkCond = True
        self.moveCond = False
        self.moveSelection = []
        self.instructions.set("Select one of your pieces to check the moves for.")
    def undo(self):
##        pass
        if self.pawnCond:
            self.instructions.set("Nothing can be done until the pawn is upgraded.")
            return
        if len(self.history)>=2:
            self.turns -= 1
            self.redo.append(copy.deepcopy(self.history.pop()))
            self.myBoard = copy.deepcopy(self.history[-1])
            self.updateBoardLayout()
        else:
            if self.turns%2 == 0:
                self.instructions.set("No moves to undo. It is White's turn to move.")
            elif self.turns%2 == 1:
                self.instructions.set("No moves to undo. It is Black's turn to move.")
        
    def redoMove(self):
##        pass
        if self.pawnCond:
            self.instructions.set("Nothing can be done until the pawn is upgraded.")
            return
        if len(self.redo)>=1:
            self.turns += 1
            self.history.append(copy.deepcopy(self.redo.pop()))
            self.myBoard = copy.deepcopy(self.history[-1])
            self.updateBoardLayout()
            
        else:
            if self.turns%2 == 0:
                self.instructions.set("Nothing to redo. It is White's turn to move.")
            elif self.turns%2 == 1:
                self.instructions.set("Nothing to redo. It is Black's turn to move.")

    def newGame(self):
        if self.pawnCond:
            self.instructions.set("Nothing can be done until the pawn is upgraded.")
            return
        self.moveSelection = []
        self.checkList = []
        self.checkCond = False
        self.moveCond = False
        self.turns = 0
        self.history = []
        self.redo = []
        self.winner = None
        self.myBoard = ChessBoard.Board()
        self.updateBoardLayout()
        self.history.append(copy.deepcopy(self.myBoard))
        self.pawnCond = False
        self.instructions.set("Game Start")
    def updateBoardLayout(self):
        self.boardRows = []
        for i in range(8):
            temp = []
            for j in range(8):
                if (i+j)%2==0:
                    temp.append(self.lightSquare)
                else:
                    temp.append(self.darkSquare)
            self.boardRows.append(temp)
            
        allPieces = self.myBoard.getAllRemainingPieces()
        for piece in allPieces:
            square = piece.getPosition()
            coord = squareToCoord(square)

            
            if (coord[0]+coord[1])%2==0:
                light=True
            elif (coord[0]+coord[1])%2==1:
                light=False
            if piece.getColor()=="Black":
                if piece == "King":
                    if light:
                        self.boardRows[coord[0]][coord[1]] = self.blackKingLight
                    else:
                        self.boardRows[coord[0]][coord[1]] = self.blackKingDark
                if piece == "Queen":
                    if light:
                        self.boardRows[coord[0]][coord[1]] = self.blackQueenLight
                    else:
                        self.boardRows[coord[0]][coord[1]] = self.blackQueenDark
                if piece == "Rook":
                    if light:
                        self.boardRows[coord[0]][coord[1]] = self.blackRookLight
                    else:
                        self.boardRows[coord[0]][coord[1]] = self.blackRookDark
                if piece == "Bishop":
                    if light:
                        self.boardRows[coord[0]][coord[1]] = self.blackBishopLight
                    else:
                        self.boardRows[coord[0]][coord[1]] = self.blackBishopDark
                if piece == "Knight":
                    if light:
                        self.boardRows[coord[0]][coord[1]] = self.blackKnightLight
                    else:
                        self.boardRows[coord[0]][coord[1]] = self.blackKnightDark
                if piece == "Pawn":
                    if light:
                        self.boardRows[coord[0]][coord[1]] = self.blackPawnLight
                    else:
                        self.boardRows[coord[0]][coord[1]] = self.blackPawnDark
            elif piece.getColor()=="White":
                if piece == "King":
                    if light:
                        self.boardRows[coord[0]][coord[1]] = self.whiteKingLight
                    else:
                        self.boardRows[coord[0]][coord[1]] = self.whiteKingDark
                if piece == "Queen":
                    if light:
                        self.boardRows[coord[0]][coord[1]] = self.whiteQueenLight
                    else:
                        self.boardRows[coord[0]][coord[1]] = self.whiteQueenDark
                if piece == "Rook":
                    if light:
                        self.boardRows[coord[0]][coord[1]] = self.whiteRookLight
                    else:
                        self.boardRows[coord[0]][coord[1]] = self.whiteRookDark
                if piece == "Bishop":
                    if light:
                        self.boardRows[coord[0]][coord[1]] = self.whiteBishopLight
                    else:
                        self.boardRows[coord[0]][coord[1]] = self.whiteBishopDark
                if piece == "Knight":
                    if light:
                        self.boardRows[coord[0]][coord[1]] = self.whiteKnightLight
                    else:
                        self.boardRows[coord[0]][coord[1]] = self.whiteKnightDark
                if piece == "Pawn":
                    if light:
                        self.boardRows[coord[0]][coord[1]] = self.whitePawnLight
                    else:
                        self.boardRows[coord[0]][coord[1]] = self.whitePawnDark

        for i in range(8):
            label = tk.Label(self,text = self.letters[i],fg="white",bg="blue")
            label.grid(column=i+1,row=0,columnspan=1,rowspan=1,sticky="EW")
            label = tk.Label(self,text = self.numbers[i],fg="white",bg="blue")
            label.grid(column=0,row=i+1,columnspan=1,rowspan=1,sticky="NSE")
        for i in range(1,9):
            for j in range(1,9):
                if (i+j)%2==0:
                    button = tk.Button(self, image = self.boardRows[i-1][j-1])
                elif (i+j)%2==1:
                    button = tk.Button(self, image = self.boardRows[i-1][j-1])
                button["command"] = lambda x=(10*(i-1)+(j-1)):self.OnButtonClick(x)
                button.grid(column=j,row=i)
        if self.turns %2 == 0:
            self.turnLabel.set("It is White's turn to move.")
        elif self.turns %2 == 1:
            self.turnLabel.set("It is Black's turn to move.")

#add a resetPieceSelection
#add in makeMove/checkMove instructions
#show piece selections on and possible moves in label
#add a button to carry out the function


        
##        if self.count==0:
##            self.path = 'whiteQueenDark.jpg'
##            self.img.paste(Image.open(self.path))
##        elif self.count==1:
##            self.path = 'whiteBishopDark.jpg'
##            self.img.paste(Image.open(self.path))
##            self.img.paste(Image.open(self.path))
##        elif self.count==2:
##            self.path = 'lightSquare.jpg'
##            self.img.paste(Image.open(self.path))
####            self.path = 'blackRook.jpg'
####            self.img.paste(Image.open(self.path))
##        elif self.count==3:
##            self.path = 'darkSquare.jpg'
##            self.img.paste(Image.open(self.path))
####            self.path = 'blackKing.jpg'
####            self.img.paste(Image.open(self.path))
##        elif self.count==4:
####            self.path = 'lightSquare.jpg'
####            self.img.paste(Image.open(self.path))
##            self.path = 'whiteKnightLight.jpg'
##            self.img.paste(Image.open(self.path))
##        else:
##            print "Done"
##        self.count+=1
####        self.labelVariable.set(self.entryVariable.get()+" (You clicked the button)")
####        self.entry.focus_set()
####        self.entry.selection_range(0,Tkinter.END)

app = simpleapp_tk()
app.title('my application')
##path = 'whiteQueen.jpg'
##img = ImageTk.PhotoImage(Image.open(path))
app.mainloop()


