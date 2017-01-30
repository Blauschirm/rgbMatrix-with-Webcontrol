import array, time, serial, os.path, os, sys
from random import randint
from subprocess import call
from math import *
from graphics import *
from timeit import default_timer as timer
from PIL import Image



class Matrix:
	
	def __init__(COMPort, cols, rows, hue, Serial, debug, Preview):
		self.COMPort=COMPort
		self.cols=cols
		self.rows=rows
		self.hue=hue
		self.Serial=Serial
		self.debug=debug
		self.Preview=Preview
		self.boxsize = 40
		self.matrix = [[0 for x in range(self.cols)] for x in range(self.rows)]
		self.correcter = [[0 for x in range(self.cols)] for x in range(self.rows)]
		if(self.Preview):win = GraphWin('lolz', 660, 660)
		self.mode=0
		self.px=''
		self.pos=0
		self.framenumber_int=0
		self.Files={
			"mario" : os.path.dirname(os.path.abspath(sys.argv[0])) + "\\Mario.bmp",
			"flappe" : "C:\\Users\\Max\\Pictures\\Pixels\\flappy"
		}
		if self.Serial : self.ser = serial.Serial(self.COMPort, 1000000, timeout=0.1)
	
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


	def isinFiles(self, Motiv):
		if Motiv in self.Files:
			return True
		else:
			return False

	def CopytoMatrix(self, active_frame,step, pos):
		for n in range(self.cols):
			for m in range(self.rows):
				col = active_frame[n,m+step*pos]
				self.matrix[n][m] = LED((col[0]), col[1], col[2])
		Flush(self.matrix)	
		
	def vertical(self):
		if(self.pos>self.framenumber_int): self.pos=0
		CopytoMatrix(self.px,16,self.pos)
		self.pos+=1


			
	def multiple(self, Motiv):
		picname=(str(self.pos)+".bmp")
		complete_filepath = self.Files[Motiv] + "/" + picname
		if((os.path.exists(complete_filepath))==False):
			self.pos=0
			#timeitend()
			#timeitstart()
		else:
			print(picname)
			Picture=Image.open(complete_filepath)
			px = Picture.load()
			CopytoMatrix(px,0,1)
			pos+=1

				
	def single(self, Motiv):
		Picture=Image.open(self.Files[Motiv])
		px = Picture.load()
		CopytoMatrix(px,0,1)
		
	def findmode(self, Motiv):	
		self.pos=0
		if(self.Files[Motiv][-4:] == ".bmp"):	
			Picture = Image.open(self.Files[Motiv])
			px = Picture.load()
			width,height = Picture.size
			if(height%16 == 0 and width%16 ==0):
				if(height>16 and width==16):
					framenumber = round(height)/16
					self.framenumber_int = int(framenumber)
					return 2 #vertical()
				elif(width>16 and height==16):
					framenumber = round(height)/16
					self.framenumber_int = int(framenumber)
					return 3 #horizontal()
				elif(height==16 and width==16):
					return 1 #single
		else:
			picname=(str(0)+".bmp")
			complete_filepath = self.Files[Motiv] + "/" + picname
			Picture = Image.open(complete_filepath)
			px = Picture.load()
			width,height = Picture.size
			if(width==16 and height==16):
				return 4 #multiple()
		print("Filepath not valid")
		return 0
		


	def RenderFrame(Motiv, mode):
		if(mode==1): single(Motiv)
		elif(mode==2): vertical()
		elif(mode==4): multiple(Motiv)
		elif(mode==3): horizontal()
		else: print("Unknown mode")
		
	def Flush(self, Pixel_Matrix):
		output=bytearray()
		if(self.Preview):Windowspreviev()
		for n in range(self.cols):
			for m in range(self.rows):
				output=Pixel_Matrix[n][m].cast(output, hue)
		output.append(1)
		if(Serial):self.ser.write(output)

	def Windowspreviev():
		for i in range(16):													
			for j in range(16):  
				Rect = Rectangle(Point((3+i*boxsize),(3+j*boxsize)), Point((boxsize+3+i*boxsize), (boxsize+3+j*boxsize)))
				color = color_rgb(matrix [i][j].red,matrix[i][j].green,matrix[i][j].blue)
				Rect.setFill(color)
				Rect.draw(win) 





if(__name__=="__main__"):	
	Matrix('COM6', 16, 16, 1, True, False)#, False)
							
	Matrix.RenderFrame("flappe", Matrix.findmode(Matrix, "flappe"))
	if(Matrix.Serial):Matrix.ser.close() 


	if(Matrix.Preview):
		win.getMouse()
		win.close()
		if(Matrix.Serial):Matrix.ser.close() 
