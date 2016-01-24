import LED
from LED import *# Flush, FillBlack
import time, collections
from random import randint
from tornado import gen
direction='r'
lastdir='r'
cols = 16
rows = 16
start=time.time()
snakexy=collections.deque()
foodxy=(0,0)
snakelength=3
matrix = [[0 for x in range(cols)] for x in range(rows)]
x=2
y=2

def SnakeRST():
	global x,y, direction, start, snakexy, matrix, foodxy, snakelength, lastdir
	foodxy=(randint(0,15), randint(0,15))
	x=0
	y=0
	matrix = FillBlack(matrix)
	snakexy.clear()
	snakexy.append((0,8))
	direction='r'
	lastdir='r'
	start=time.time()
	snakelength = 3

def setDir(tbdir):
	global direction, lastdir
	if(tbdir=="r" and lastdir=="l"): return
	if(tbdir=="l" and lastdir=="r"): return
	if(tbdir=="u" and lastdir=="d"): return
	if(tbdir=="d" and lastdir=="u"): return
	direction=tbdir
	

def snake():
	def GameOver():
		global matrix
		for i in range(2):
			matrix = FillBlack(matrix)
			Flush(matrix)
			print("dark")
			time.sleep(0.5)	
			for i in range(len(snakexy)):
				x,y = snakexy[i]
				matrix[x][y]=LED(0,255,0)	
			Flush(matrix)
			print("white")
			time.sleep(0.5)	
	
	global x,y,matrix, start, direction, snakelength, foodxy, lastdir
	if(time.time()-start>=0.1):
		newFrame=True
		start=time.time()
		x,y=snakexy[-1]
		if(direction=='l'): x-=1
		if(direction=='r'): x+=1
		if(direction=='u'): y-=1
		if(direction=='d'): y+=1
		if(x<0 or x>15 or y<0 or y>15):
			print("Game Over, boundries")
			GameOver()
			SnakeRST()
			
		elif(snakexy.count((x,y))>0):
			print("Game Over, self")
			GameOver()
			SnakeRST()

		else:
			if((x,y)==foodxy):
				snakelength += 1
				foodxy=(randint(0,15), randint(0,15))
				while(snakexy.count(foodxy)>0):
					foodxy=(randint(0,15), randint(0,15))
			lastdir=direction
	
			snakexy.append((x,y))
			if(len(snakexy)>snakelength):
				snakexy.popleft()
							
			matrix = FillBlack(matrix)
			x,y=foodxy
			matrix[x][y]=LED(100,255,100)
			for i in range(len(snakexy)):
				x,y = snakexy[i]
				matrix[x][y]=LED(0,255,0)		
			Flush(matrix)
			

