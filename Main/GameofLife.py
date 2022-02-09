from LED import Flush, LED
from random import randint
import numpy as np

class Tile():
    def __init__(self):
        self.isAlive = False
        self.willLive = False
        self.neighbours = 0
        self.shape = (16,16,3)


    def update(self):
        self.isAlive = self.willLive
        self.willLive = False

    def getRGB(self):
        if self.isAlive: 
            return (0,255,0)
        else: 
            return (0,0,0)

    def check(self):
        if(self.isAlive):
            if self.neighbours < 2:
                self.willLive = False
            elif self.neighbours == 2 or self.neighbours ==3:
                self.willLive = self.isAlive
            elif self.neighbours > 3:
                self.willLive = False
        elif self.neighbours == 3:
            self.willLive = True
    
    def getisAlive(self):
        return self.isAlive

    def setneighbours(self, i):
        self.neighbours = i

    def setisAlive(self, b):
        self.willLive = b

class GameofLife:
    def __init__(self):
        self.Board = [[0 for x in range(16)] for x in range(16)]
        for i in range(16):
            for j in range(16):
                self.Board[i][j]=Tile()
        self.startpopulation = 100
        self.matrix=np.zeros(self.shape, np.ubyte)

    def reset(self):
        i = 0

        while i < self.startpopulation:
            self.Board[randint(0,15)][randint(0,15)].setisAlive(True)
            i+=1

    def update(self):
        def calcTile(i,j,Board):
            tmpneighbours = -1
            y = j-1
            while y <= j+1:
                x = i-1
                while x <= i+1:
                    if( x >= 0 and y >= 0):
                        try:
                            lives = Board[x][y].getisAlive()
                        except IndexError:
                            lives = False
                        if lives: tmpneighbours += 1
                    x=x+1
                y=y+1
                Board[i][j].setneighbours = tmpneighbours

        for i in range(16):
            for j in range(16):
                self.matrix[j, i] = self.Board[j][i].getRGB()
                calcTile(i, j, self.Board)
                self.Board[j][i].check()
                self.Board[j][i].update()

        Flush(self.matrix)