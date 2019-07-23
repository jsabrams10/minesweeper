#John Abrams
#5/12/2019
#CS 314 (Prin. Prog.): Final Project
#johnsMinesweeper.py

from collections import deque
import random
from Tkinter import *
import tkMessageBox

class Minesweeper:

    def __init__(self, scheme):

        #LOAD spaceImages
        self.space_mine = PhotoImage(file = "spaceImages/johns_mine.gif")
        self.space_unclicked = PhotoImage(file = "spaceImages/johns_unclicked.gif")
        self.space_clicked = PhotoImage(file = "spaceImages/johns_clicked.gif")
        self.space_flag = PhotoImage(file = "spaceImages/johns_flag.gif")
        self.space_flagWrong = PhotoImage(file = "spaceImages/johns_flagWrong.gif")
        self.space_num = []

        for spaceNum in range(1, 9):
            self.space_num.append(PhotoImage(file = "spaceImages/johns_" + str(spaceNum) + ".gif"))

        #GENERATE frame
        frame = Frame(scheme)
        frame.pack()

        #GENERATE title
        self.title = Label(frame, text = "John's Minesweeper")
        self.title.grid(row = 0, column = 0, columnspan = 10)

        #GENERATE SPACE VARIABLES
        self.clicked = 0
        self.flags = 0
        self.correctFlags = 0

        #GENERATE SPACE VARIABLES
        self.buttons = dict({})
        self.mines = 0

        xLoc = 1
        yLoc = 0

        #RANDOMLY GENERATE mines
        for spaceDex in range(0, 100):

            isMine = 0

            if random.uniform(0.0, 1.0) < 0.1:

                isMine = 1
                self.mines += 1

            self.buttons[spaceDex] = [

                #0) Button
                Button(frame, image = self.space_unclicked),

                #1) isMine (NO: 0; YES: 1)
                isMine,

                #2) SPACE STATE (UNCLICKED: 0; CLICKED: 1; FLAGGED: 2)
                0,

                #3) ID
                spaceDex,

                #4) [x, y] LOCATION IN GRID
                [xLoc, yLoc],

                #5) # OF MINES IN PROXIMITY (CALCULATED AFTER PLACEMENT)
                0
            ]

            self.buttons[spaceDex][0].bind('<Button-1>', self.lClickedWrapper(spaceDex))
            self.buttons[spaceDex][0].bind('<Button-3>', self.rClickedWrapper(spaceDex))

            #INCREMENT SPACE LOCATION
            yLoc += 1

            if yLoc == 10:

                yLoc = 0
                xLoc += 1

        #SET BUTTONS IN grid
        for spaceDex in self.buttons:
            self.buttons[spaceDex][0].grid(row = self.buttons[spaceDex][4][0], column = self.buttons[spaceDex][4][1])

        #CALCULATE SPACE NUMBERS
        for spaceDex in self.buttons:

            minesInProximity = 0

            if(spaceDex > 9) and ((spaceDex + 1) % 10 != 0) and (self.checkForMines(spaceDex - 9)):
                minesInProximity += 1

            if(spaceDex > 9) and (self.checkForMines(spaceDex - 10)):
                minesInProximity += 1

            if(spaceDex > 9) and ((spaceDex + 10) % 10 != 0) and (self.checkForMines(spaceDex - 11)):
                minesInProximity += 1

            if((spaceDex + 10) % 10 != 0) and (self.checkForMines(spaceDex - 1)):
                minesInProximity += 1

            if((spaceDex + 1) % 10 != 0) and (self.checkForMines(spaceDex + 1)):
                minesInProximity += 1

            if(spaceDex < 90) and ((spaceDex + 10) % 10 != 0) and (self.checkForMines(spaceDex + 9)):
                minesInProximity += 1

            if(spaceDex < 90) and (self.checkForMines(spaceDex + 10)):
                minesInProximity += 1

            if(spaceDex < 90) and ((spaceDex + 1) % 10 != 0) and (self.checkForMines(spaceDex + 11)):
                minesInProximity += 1

            #SAVE # OF MINES IN PROXIMITY TO button
            self.buttons[spaceDex][5] = minesInProximity

        #GENERATE TOTAL # MINES
        self.mineLabel = Label(frame, text = "#MINES: " + str(self.mines))
        self.mineLabel.grid(row = 11, column = 0, columnspan = 5)

        #GENERATE TOTAL # FLAGS
        self.flagLabel = Label(frame, text = "#FLAGS: " + str(self.flags))
        self.flagLabel.grid(row = 11, column = 4, columnspan = 5)

    ####################

    def checkForMines(self, spaceDex):

        try:

            if self.buttons[spaceDex][1] == 1:
                return True

        except KeyError:
            pass

    ####################

    def rClickedWrapper(self, spaceDex):
        return lambda Button: self.rClicked(self.buttons[spaceDex])

    ####################

    def lClickedWrapper(self, spaceDex):
        return lambda Button: self.lClicked(self.buttons[spaceDex])

    ####################

    def rClicked(self, buttonData):

        #IF NOT clicked
        if buttonData[2] == 0:

            buttonData[0].config(image = self.space_flag)
            buttonData[2] = 2
            buttonData[0].unbind('<Button-1>')

            #IF isMine
            if buttonData[1] == 1:
                self.correctFlags += 1

            #IF FLAGGED, UNFLAG
            self.flags += 1
            self.updateFlags()

        #IF FLAGGED, UNFLAG
        elif buttonData[2] == 2:

            buttonData[0].config(image = self.space_unclicked)
            buttonData[2] = 0
            buttonData[0].bind('<Button-1>', self.lClickedWrapper(buttonData[3]))

            #IF isMine
            if buttonData[1] == 1:
                self.correctFlags -= 1

            self.flags -= 1
            self.updateFlags()

    ####################

    def lClicked(self, buttonData):

        #IF isMine, gameover
        if buttonData[1] == 1:
            self.gameover()

        else:

            #SWITCH IMAGE
            if buttonData[5] == 0:

                buttonData[0].config(image = self.space_clicked)
                self.clearEmptySpaces(buttonData[3])

            else:
                buttonData[0].config(image = self.space_num[buttonData[5] - 1])

            #IF NOT ALREADY CLICKED, CHANGE STATE AND COUNT
            if buttonData[2] != 1:

                buttonData[2] = 1
                self.clicked += 1

            if self.clicked == 100 - self.mines:
                self.victory()

    ####################

    def checkSpace(self, spaceDex, queue):

        try:

            if self.buttons[spaceDex][2] == 0:

                if self.buttons[spaceDex][5] == 0:

                    self.buttons[spaceDex][0].config(image = self.space_clicked)
                    queue.append(spaceDex)

                else:
                    self.buttons[spaceDex][0].config(image = self.space_num[self.buttons[spaceDex][5] - 1])

                self.buttons[spaceDex][2] = 1
                self.clicked += 1

        except KeyError:
            pass

    ####################

    def clearEmptySpaces(self, spaceDex):

        queue = deque([spaceDex])

        while len(queue) != 0:

            currDex = queue.popleft()

            self.checkSpace(currDex - 9, queue) #TOP RIGHT
            self.checkSpace(currDex - 10, queue) #TOP MIDDLE
            self.checkSpace(currDex - 11, queue) #TOP LEFT
            self.checkSpace(currDex - 1, queue) #LEFT
            self.checkSpace(currDex + 1, queue) #RIGHT
            self.checkSpace(currDex + 9, queue) #BOTTOM LEFT
            self.checkSpace(currDex + 10, queue) #BOTTOM MIDDLE
            self.checkSpace(currDex + 11, queue) #BOTTOM RIGHT

    ####################

    def updateFlags(self):
        self.flagLabel.config(text = "#FLAGS: " + str(self.flags))

    ####################

    def gameover(self):

        #REVEAL MINES AND VERIFY FLAGS
        for spaceDex in self.buttons:

            if self.buttons[spaceDex][1] != 1 and self.buttons[spaceDex][2] == 2:
                self.buttons[spaceDex][0].config(image = self.space_flagWrong)

            if self.buttons[spaceDex][1] == 1 and self.buttons[spaceDex][2] != 2:
                self.buttons[spaceDex][0].config(image = self.space_mine)

        tkMessageBox.showinfo("GAME OVER", "YOU LOSE!")

    ####################

    def victory(self):

        #REVEAL MINES AND VERIFY FLAGS
        for spaceDex in self.buttons:

            if self.buttons[spaceDex][1] != 1 and self.buttons[spaceDex][2] == 2:
                self.buttons[spaceDex][0].config(image = self.space_flagWrong)

            if self.buttons[spaceDex][1] == 1 and self.buttons[spaceDex][2] != 2:
                self.buttons[spaceDex][0].config(image = self.space_mine)

        tkMessageBox.showinfo("GAME OVER", "YOU WIN!")

####################

def main():

    #GENERATE WIDGET
    global seed
    seed = Tk()
    seed.title("John's Minesweeper")
    seed.geometry("275x275")
    seed.resizable(0, 0)

    #INSTANTIATE/RUN GAME
    minesweeper = Minesweeper(seed)
    seed.mainloop()

if __name__ == "__main__":
    main()
