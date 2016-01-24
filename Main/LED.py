import array, time, serial, os.path, os, sys
from random import randint
from subprocess import call
from math import *
from graphics import *
from timeit import default_timer as timer
from PIL import Image

Serial=True
debug=True
Preview=False


#mark1
#path = "C:/Users/Max/Pictures/Pixels/365/bmp/8.bmp"
#flappe = "C:/Users/Max/Pictures/Pixels/flappy"
#tetris = "C:/Users/Max/Pictures/Pixels/tetris"
#NyanCat = "C:/Users/Max/Pictures/Pixels/NyanCat/0.bmp"
#Link_walk = "C:/Users/Max/Pictures/Pixels/link-walk"
#LSD1 = "C:/Users/Max/Pictures/Pixels/LSD/rainbow-spiral/0.bmp"
#Gameboy = "C:/Users/Max/Pictures/Pixels/Gameboy/0.bmp"
#Lemmingsfall = "C:/Users/Max/Pictures/Pixels/Lemmings/Lemmingasfall"
#white = "C:/Users/Max/Pictures/Pixels/white.bmp"
#mushrooms = "C:/Users/Max/Pictures/Pixels/mushrooms"
#outrun ="C:\\Users\\Max\\Pictures\\Pixels\\365\\365daypixelartchallenge\\0.bmp"


start = 0
boxsize = 40
cols = 16
rows = 16
hue = 0.1
matrix = [[0 for x in range(cols)] for x in range(rows)]
correcter = [[0 for x in range(cols)] for x in range(rows)]
if(Preview):win = GraphWin('lolz', 660, 660)

Motiv=''
lenght_validated=False
pos=0
framenumber_int=1






if Serial : ser = serial.Serial('COM6', 1000000, timeout=0.1)




class Media:
	def __init__(self, path, mode, fps=None):
		self.path = path
		self.mode = mode
		if(fps): 
			self.fps=fps
		else: 
			self.fps=24
			
	def getpath(self):
		return self.path
		
	def getfps(self):
		return self.fps
		
	def getmode(self):
		return self.mode
		
	def setmode(self, mode):
		self.mode = mode
		
Files={
	"mario" : Media(os.path.dirname(os.path.abspath(sys.argv[0])) + "\\Mario.bmp",1),
	"flappe" : Media("C:\\Users\\Max\\Pictures\\Pixels\\flappy",None,5),
	"nyancat" : Media("C:/Users/Max/Pictures/Pixels/NyanCat/0.bmp",None,15),
	"tetris" : Media("C:/Users/Max/Pictures/Pixels/tetris",None,24)
}

Media=Files["mario"]
path=Media.getpath()
px = Image.open(path).load()

class LED:
	def __init__(self, red, green, blue):
		self.red = int(red)
		self.green = int(green)
		self.blue = int(blue)
     
	def cast(self, out, hue):
		output=bytearray()
		output=out
		self.green=int(self.green*hue)
		if(self.green==1):
			self.green+=1
		output.append((self.green))
		
		self.red=int(self.red*hue)
		if(self.red==1):
			self.red+=1
		output.append((self.red))
		
		self.blue=int(self.blue*hue)
		if(self.blue==1):
			self.blue+=1
		output.append((self.blue))
		return output

def findfps(Motiv):
	return Files[Motiv].getfps()

def setBools(Serialbool, Debugbool, previewbool):
	Serial = Serialbool
	debu = Debugbool
	Preview = previewbool

def isinFiles(Motiv):
	if Motiv in Files:
		return True
	else:
		return False

def CopytoMatrix(active_frame,step, posi):
	global matrix
	for n in range(cols):
		for m in range(rows):
			col = active_frame[n,m+step*posi]
			matrix[n][m] = LED((col[0]), col[1], col[2])
	Flush(matrix)	
	
def FillBlack(matrix):
	for n in range(cols):
		for m in range(rows):
			matrix[n][m] = LED(0,0,0)
	return matrix
	
def vertical():
	global framenumber_int
	global px
	global pos
	CopytoMatrix(px,16,pos)
	if(pos==framenumber_int): pos=0
	else: pos=pos+1
	
def multiple():
	global pos, Motiv
	global framenumber_int
	global lenght_validated

	if(lenght_validated):
		if(pos==framenumber_int):
			pos=0
		picname=(str(pos)+".bmp")
		complete_filepath = Files[Motiv].getpath() + "/" + picname
		print(picname)
		Picture=Image.open(complete_filepath)
		px = Picture.load()
		CopytoMatrix(px,0,1)
		pos+=1
	else:
		picname=(str(pos)+".bmp")
		complete_filepath = Files[Motiv].getpath() + "/" + picname
		if((os.path.exists(complete_filepath))==False):
			framenumber_int=pos
			lenght_validated=True
			pos=0
		else:
			print(picname)
			Picture=Image.open(complete_filepath)
			px = Picture.load()
			CopytoMatrix(px,0,1)
			pos+=1
			
def single():
	global px
	
	CopytoMatrix(px,0,1)
	
def findmode(Motiv):
	global px, pos, framenumber_int
	pos=0
	lenght_validated = False
	Media = Files[Motiv]
	if(Media.getmode()==None):
		if(Media.getpath()[-4:] == ".bmp"):	
			Picture = Image.open(Files[Motiv].getpath())
			px = Picture.load()
			width,height = Picture.size
			if(height%16 == 0 and width%16 ==0):
				if(height>16 and width==16):
					framenumber = height/16-1
					framenumber_int = int(framenumber)
					Media.setmode=2
					return 2 #vertical()
				elif(width>16 and height==16):
					framenumber = width/16-1
					framenumber_int = int(framenumber)
					Media.setmode=3
					return 3 #horizontal()
				elif(height==16 and width==16):
					Media.setmode=1
					return 1 #single
		else:
			picname=(str(0)+".bmp")
			complete_filepath = Files[Motiv].getpath() + "/" + picname
			Picture = Image.open(complete_filepath)
			px = Picture.load()
			width,height = Picture.size
			if(width==16 and height==16):
				Media.setmode=4
				return 4 #multiple()
		print("Filepath not valid")
		return 0
	else:
		return Media.getmode()
	
def Flush(Pixel_Matrix):
	global ser
	output=bytearray()
	if(Preview):Windowspreviev()
	for n in range(cols):
		for m in range(rows):
			output=Pixel_Matrix[n][m].cast(output, hue)
	output.append(1)
	if(Serial):ser.write(output)

def Windowspreviev():
	for i in range(16):													
		for j in range(16):  
			Rect = Rectangle(Point((3+i*boxsize),(3+j*boxsize)), Point((boxsize+3+i*boxsize), (boxsize+3+j*boxsize)))
			color = color_rgb(matrix [i][j].red,matrix[i][j].green,matrix[i][j].blue)
			Rect.setFill(color)
			Rect.draw(win) 

def setMotiv(tbMotiv, mode):
	global Motiv, px, pos, lenght_validated
	Motiv = tbMotiv
	lenght_validated=False
	pos=0
	if(mode==1 or mode== 2 or mode==3):
		Picture = Image.open(Files[Motiv].getpath())
		px = Picture.load()

	


if(__name__=="__main__"):
	tbMotiv="mario"							
	RenderFrame(tbMotiv, findmode(tbMotiv))
	if(Serial):ser.close() 

if(Preview):
	win.getMouse()
	win.close()
	if(Serial):ser.close() 


