""" Simple Snake Game """

from collections import deque
from math import sin
from random import randint
from time import sleep

from div import writeHighscore
from LED import LED, Fill, Flush


class Snake:

    def __init__(self):
        self.cols = self.rows = 16
        self.foodxy = (randint(0, 15), randint(0, 15))
        self.x = self.y = 0
        self.matrix = [[0 for x in range(self.cols)] for x in range(self.rows)]
        self.matrix = Fill(self.matrix, 0, 0, 0)
        self.snakexy = deque()
        self.snakexy.append((0, 8))
        self.direction = 'r'
        self.lastdir = 'r'
        self.snakelength = 3

    def reset(self):
        self.foodxy = (randint(0, 15), randint(0, 15))
        self.x = self.y = 0
        self.matrix = [[0 for x in range(self.cols)] for x in range(self.rows)]
        self.matrix = Fill(self.matrix, 0, 0, 0)
        self.snakexy = deque()
        self.snakexy.append((0, 8))
        self.direction = 'r'
        self.lastdir = 'r'
        self.snakelength = 3

    def setDir(self, tbdir):
        if tbdir == "r" and self.lastdir == "l":
            return
        if tbdir == "l" and self.lastdir == "r":
            return
        if tbdir == "u" and self.lastdir == "d":
            return
        if tbdir == "d" and self.lastdir == "u":
            return
        self.direction = tbdir

    def getDir(self):
        if self.direction == 'l':
            self.x -= 1
        if self.direction == 'r':
            self.x += 1
        if self.direction == 'u':
            self.y -= 1
        if self.direction == 'd':
            self.y += 1

    def Gameover(self):
        if self.snakelength > 3:
            rank = writeHighscore(self.snakelength, "max")
            print("Rank {} with a score of {} points.".format(rank, self.snakelength))
        for i in range(2):
            self.matrix = Fill(self.matrix, 0, 0, 0)
            Flush(self.matrix)
            sleep(0.5)
            for i in range(len(self.snakexy)):
                x, y = self.snakexy[i]
                self.matrix[x][y] = LED(0+75*(sin(i)+1), 255, 0)
            Flush(self.matrix)
            sleep(0.5)

    def update(self):
        self.x, self.y = self.snakexy[-1]
        self.getDir()

        #Collision detection
        if self.x < 0 or self.x >= self.rows or self.y < 0 or self.y >= self.cols or (self.x, self.y) in self.snakexy:
            self.Gameover()
            self.reset()
            return

        if (self.x, self.y) == self.foodxy:
            self.snakelength += 1
            self.foodxy = (randint(0, 15), randint(0, 15))
            while self.foodxy in self.snakexy:
                self.foodxy = (randint(0, 15), randint(0, 15))
        elif len(self.snakexy) >= self.snakelength:
            self.snakexy.popleft()

        self.lastdir = self.direction
        self.snakexy.append((self.x, self.y))							
        self.matrix = Fill(self.matrix, 0, 0, 0)
        x, y = self.foodxy
        self.matrix[x][y]=LED(100, 255, 100)
        for i in range(len(self.snakexy)):
            x, y = self.snakexy[i]
            self.matrix[x][y] = LED(0+75*(sin(i)+1), 255, 0)
        Flush(self.matrix)