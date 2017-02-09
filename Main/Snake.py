import LED
from LED import *# Flush, FillBlack
import time, collections, os
from time import strftime, localtime, sleep, strptime
from random import randint
from tornado import gen
from operator import itemgetter

direction='r'
lastdir='r'
cols = 16
rows = 16
start=time.time()
snakexy=collections.deque()
foodxy=(0,0)
snakelength = 3
matrix = [[0 for x in range(cols)] for x in range(rows)]
x=2
y=2

dir=os.path.dirname(__file__)

def SnakeRST():
	global x,y, direction, start, snakexy, matrix, foodxy, snakelength, lastdir
	foodxy=(randint(0,15), randint(0,15))
	x=0
	y=0
	matrix = Fill(matrix,0,0,0)
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
	global snakexy

	def GameOver():
		global matrix
		if(snakelength > 3):
			rank = writeHighscore(snakelength,"max")
			print("Rank {} with a score of {} points.".format(rank, snakelength))
		for i in range(2):
			matrix = Fill(matrix,0,0,0)
			Flush(matrix)
			time.sleep(0.5)	
			for i in range(len(snakexy)):
				x,y = snakexy[i]
				matrix[x][y]=LED(0+75*(sin(i)+1),255,0)	
			Flush(matrix)
			time.sleep(0.5)	
	
	global snakelength, x,y,matrix, start, direction, foodxy, lastdir
	if(time.time()-start>=0.1):
		gefressen = False
		newFrame=True
		start=time.time()
		x,y=snakexy[-1]
		if(direction=='l'): x-=1
		if(direction=='r'): x+=1
		if(direction=='u'): y-=1
		if(direction=='d'): y+=1
		if(x<0 or x>15 or y<0 or y>15):
			GameOver()
			SnakeRST()
		else:
			if((x,y)==foodxy):
				snakelength += 1
				gefressen = True
				foodxy=(randint(0,15), randint(0,15))
				while(snakexy.count(foodxy)>0):
					foodxy=(randint(0,15), randint(0,15))
			lastdir=direction
			#snakexy.append((x,y))
			if(len(snakexy)>=snakelength):
				if(gefressen==False):
					snakexy.popleft()
			if(snakexy.count((x,y))>0):
				GameOver()
				SnakeRST()
			snakexy.append((x,y))							
			matrix = Fill(matrix,0,0,0)
			x,y=foodxy
			matrix[x][y]=LED(100,255,100)
			for i in range(len(snakexy)):
				x,y = snakexy[i]
				matrix[x][y]=LED(0+75*(sin(i)+1),255,0)		
			Flush(matrix)
			
def readHighscores(path):
	Scores=[]
	if os.path.exists(path):
		with open(path,mode='r') as rawScores:
			for line in rawScores:
				tmp=line.strip()
				tmp=tmp.split(',')
				tmp[0] = int(tmp[0])
				tmp[1] = strptime(tmp[1], "%X %x")
				Scores.append(tmp)
	return(Scores)

def writeHighscore(score, name):
	rank=0

	def writetofile(path, Scores):		
		with open(fullpath,mode='w+') as rawScores:
			for Score in Scores:
				tmp = str(Score[0]) + ',' + strftime("%X %x",Score[1]) + ',' + Score[2] + '\n'
				rawScores.write(tmp)

	basepath= os.path.join(os.path.dirname(__file__), 'saves')
	fullpath = os.path.join(basepath, "snake.txt")
	
	Scores=readHighscores(fullpath)
	newScore=[score, localtime(), name]

	for index, Score in enumerate(Scores):
		if newScore[0] > Score[0]:
			Scores.insert(index,newScore)
			rank = index + 1
			Scores=Scores[:100]
			if not os.path.exists(basepath):
				os.makedirs(basepath)
			writetofile(fullpath, Scores)
			return rank

	Scores.append(newScore)
	rank = len(Scores) + 1
	writetofile(fullpath, Scores)
	return rank

writeHighscore(4,"test")