#!/usr/bin/env python
import tkinter as tk
import tkinter.messagebox
import os
import copy
import matrix

class App:
    def __init__(self,master = None):
        self.mainFrame = tk.Tk()
        self.mainFrame.grid()
        self.mainFrame.title("2048 v1.2 Doodle")
        self.mainFrame.resizable(False, False)
        self.size = 4
        self.createWidgets()
        self.initColor()
        self.mat = matrix.Matrix(self.size)
        self.loadGame()
        self.matQueue = [copy.deepcopy(self.mat.matrix)]
        self.scoreQueue = [self.curScoreNum["text"]]
        self.event()

    def createWidgets(self):
        self.upFrame = tk.LabelFrame(self.mainFrame, bg = "#EE7600")
        self.upFrame.grid(sticky = "NEWS")
        self.upFrame.columnconfigure(0, minsize = 180)
        self.upFrame.columnconfigure(1, minsize = 180)

        self.curScoreText = tk.Label(self.upFrame, text = "Score", bg = "#EE7600")
        self.curScoreNum = tk.Label(self.upFrame, text = "0", bg = "#EE7600")
        self.recordText = tk.Label(self.upFrame, text = "Record", bg = "#EE7600")
        self.recordNum = tk.Label(self.upFrame, text = "0", bg = "#EE7600")
        self.curScoreText.grid(row = 0, column = 0, sticky = "NEWS")
        self.curScoreNum.grid(row = 1, column = 0, sticky = "NEWS")
        self.recordText.grid(row = 0, column = 1, sticky = "NEWS")
        self.recordNum.grid(row = 1, column = 1, sticky = "NEWS")

        self.downFrame = tk.LabelFrame(self.mainFrame, bg = "#BBADA0")
        self.downFrame.grid(sticky = "NEWS")

        self.labelMatrix = []
        self.cellGap = 1
        for i in range(self.size):
            row = []
            for j in range(self.size):
                cell = tk.Label(self.downFrame, width = 8, height = 4, bg = "#CCC0B4")
                cell.grid(row = i, column = j, padx = self.cellGap, pady = self.cellGap)
                row.append(cell)
            self.labelMatrix.append(row)

    def initColor(self):
        self.colorDict = {
        0 : ['#CCC0B4', '#CCC0B4'],
        2 : ['#EEE4DA', '#000000'],
        4 : ['#EDE0C8', '#000000'],
        8 : ['#F2B179', '#000000'],
        16 : ['#EC8D54', '#000000'],
        32 : ['#F67C5F', '#000000'],
        64 : ['#EA5937', '#000000'],
        128 : ['#804000', '#000000'],
        256 : ['#F1D04B', '#000000'],
        512 : ['#EEE4DA', '#000000'],
        1024 : ['#EDE0C8', '#000000'],
        2048 : ['#F2B179', '#000000'],
        4096 : ['#EC8D54', '#000000'],
        8192 : ['#F67C5F', '#000000'],
        16384 : ['#EA5937', '#000000'],
        32768 : ['#804000', '#000000'],
        65536 : ['#F1D04B', '#000000']
        }

    def loadGame(self):
        fileName = "2048.dat"
        if(os.path.exists(fileName)):
            f = open(fileName,'r')

            line = f.readline()
            try:
                type(int(line)) == int
                self.curScoreNum["text"] = str(int(line))
            except:
                self.newGame()
                return

            line = f.readline()
            try:
                type(int(line)) == int
                self.recordNum["text"] = str(int(line))
            except:
                self.newGame()
                return

            self.mat.matrix = []
            lines = f.readlines()
            for line in lines:
                try:
                    self.mat.matrix.append(list(map(int,line.split(","))))
                    if len(self.mat.matrix[-1]) != self.size:
                        self.newGame()
                        return
                except:
                    self.newGame()
                    return
            if len(self.mat.matrix) != self.size:
                self.newGame()
                return
            self.setMatrixLabel()
        else:
            self.newGame()

    def newGame(self):
        self.mat.matrix = [[0 for i in range(self.size)] for i in range(self.size)]
        self.mat.generateNum()
        self.mat.generateNum()
        self.setMatrixLabel()
        self.curScoreNum["text"] = '0'

    def setMatrixLabel(self):
        for i in range(self.size):
            for j in range(self.size):
                self.labelMatrix[i][j]["text"] = str(self.mat.getNum(i,j))
                self.labelMatrix[i][j]["bg"] = self.colorDict[self.mat.getNum(i,j)][0]
                self.labelMatrix[i][j]["fg"] = self.colorDict[self.mat.getNum(i,j)][1]
                self.labelMatrix[i][j]["font"] = ("宋体","-20","bold")

    def event(self):
        self.mainFrame.bind("<KeyPress-Up>",self.move)
        self.mainFrame.bind("<KeyPress-Down>",self.move)
        self.mainFrame.bind("<KeyPress-Left>",self.move)
        self.mainFrame.bind("<KeyPress-Right>",self.move)
        self.mainFrame.bind("<KeyPress-r>",self.reset)
        self.mainFrame.bind("<KeyPress-R>",self.reset)
        self.mainFrame.bind("<KeyPress-b>",self.undo)
        self.mainFrame.bind("<KeyPress-B>",self.undo)
        self.mainFrame.protocol('WM_DELETE_WINDOW',self.quitGame)

    def move(self,event):
        score = 0
        if event.keysym == "Up":
            score = self.mat.move("Up")
        elif event.keysym == "Down":
            score = self.mat.move("Down")
        elif event.keysym == "Left":
            score = self.mat.move("Left")
        elif event.keysym == "Right":
            score = self.mat.move("Right")
        if score == -1:
            return
        else:
            if self.mat.isVacant():
                self.mat.generateNum()
            self.matQueue.append(copy.deepcopy(self.mat.matrix))
            self.addScore(score)
            self.scoreQueue.append(self.curScoreNum["text"])
            if len(self.scoreQueue) > 50:
                self.matQueue.pop(0)
                self.scoreQueue.pop(0)
            self.setMatrixLabel()
            self.gameOver()

    def addScore(self,score):
        self.curScoreNum["text"] = str(int(self.curScoreNum["text"])+score)
        if int(self.curScoreNum["text"]) > int(self.recordNum["text"]):
            self.recordNum["text"] = self.curScoreNum["text"]

    def gameOver(self):
        if self.mat.gameOver():
            if tk.messagebox.askquestion("Game Over","Game over!\nPlay again?") == 'yes':
                self.newGame()
                self.setMatrixLabel()
                return
            else:
                self.quitGame()

    def reset(self,event):
        if tk.messagebox.askquestion("OMG","Reset?") == 'yes':
            self.newGame()

    def undo(self,event):
        try:
            self.matQueue.pop()
            self.scoreQueue.pop()
            self.mat.matrix = copy.deepcopy(self.matQueue[-1])
            self.setMatrixLabel()
            self.curScoreNum["text"] = self.scoreQueue[-1]
        except:
            pass

    def quitGame(self):
        if tk.messagebox.askquestion("OMG","Do you want to quit?") == 'yes':
            fileName = "2048.dat"
            file = open(fileName,'w')
            lines = []
            lines.append(self.curScoreNum["text"]+'\n')
            lines.append(self.recordNum["text"]+'\n')
            for i in range(self.size):
                lines.append(','.join(list(map(str,self.mat.matrix[i])))+'\n')
            file.writelines(lines)
            file.close()
            self.mainFrame.destroy()


if __name__ == "__main__":
    app = App()
    app.mainFrame.mainloop()
