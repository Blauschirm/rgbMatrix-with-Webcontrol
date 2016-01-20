import array, time, serial, os.path
from random import randint
from subprocess import call
from math import *
from graphics import *
from PIL import Image
from timeit import default_timer as timer
from Tornado1 import StartWebsocket


path = "C:/Users/Max/Pictures/Pixels/365/bmp/8.bmp"
flappe = "C:/Users/Max/Pictures/Pixels/flappy"
tetris = "C:/Users/Max/Pictures/Pixels/tetris"
NyanCat = "C:/Users/Max/Pictures/Pixels/NyanCat/0.bmp"
Link_walk = "C:/Users/Max/Pictures/Pixels/link-walk"
LSD1 = "C:/Users/Max/Pictures/Pixels/LSD/mrdiv_polytronic/0.bmp"
Gameboy = "C:/Users/Max/Pictures/Pixels/Gameboy/0.bmp"
Lemmingsfall = "C:/Users/Max/Pictures/Pixels/Lemmings/Lemmingasfall"
white = "C:/Users/Max/Pictures/Pixels/white.bmp"
mushrooms = "C:/Users/Max/Pictures/Pixels/mushrooms"

debug=True
Preview=False
sent = 0
boxsize = 40
cols = 16
rows = 16
hue = 0.1
matrix = [[0 for x in range(cols)] for x in range(rows)]
correcter = [[0 for x in range(cols)] for x in range(rows)]
ser = serial.Serial('COM5', 1000000, timeout=0.1)
if(Preview):win = GraphWin('lolz', 660, 660)
StartWebsocket()


class LED:
	
	def __init__(self, red, green, blue):
		self.red = int(red*hue)
		self.green = int(green*hue)
		self.blue = int(blue*hue)
        
	def cast(self):
		global sent
		if(self.green==1):
			self.green+=1
		ser.write((self.green).to_bytes(1, byteorder='little'))
		sent+=1
		if(self.red==1):
			self.red+=1
		ser.write((self.red).to_bytes(1, byteorder='little'))
		sent+=1
		if(self.blue==1):
			self.blue+=1
		ser.write((self.blue).to_bytes(1, byteorder='little'))
		sent+=1
 
def DisplayMedia(filepath,delay):

	def CopytoMatrix(active_frame,step,pos):
		for n in range(cols):
			for m in range(rows):
				col = active_frame[n,m+step*pos]
				matrix[n][m] = LED((col[0]), col[1], col[2])
		Flush(matrix)	
	def vertical():
		framenumber = round(height)/16
		framenumber_int = int(framenumber)
		if(width % 16==0):
			if(height % 16==0):
				while(1):
					try:
						for i in range(framenumber_int):
							CopytoMatrix(px,16,i)
							time.sleep(delay)
					except KeyboardInterrupt:
						break
			else:
				print("Hoehe passt nicht")
		else:
			print("Breite passt nicht")
	def multiple():
		pos=0
		while(1):
			try:
				picname=(str(pos)+".bmp")
				complete_filepath = filepath + "/" + picname
				if((os.path.exists(complete_filepath))==False):
					pos=0
				else:
					print(picname)
					Picture=Image.open(complete_filepath)
					px = Picture.load()
					CopytoMatrix(px,0,1)
					pos+=1
					time.sleep(delay)
			except KeyboardInterrupt:
				break
	def single():
		Picture=Image.open(filepath)
		px = Picture.load()
		CopytoMatrix(px,0,1)
		
	if(filepath[-4:] == ".bmp"):	
		Picture=Image.open(filepath)
		px = Picture.load()
		width,height = Picture.size
		if(height>16):
			mode = vertical()
		elif(width>16):
			mode = horizontal()
		else:
			mode=single()
	else:
		mode=multiple()
	
def Windowspreviev():
	for i in range(16):													
		for j in range(16):  
			Rect = Rectangle(Point((3+i*boxsize),(3+j*boxsize)), Point((boxsize+3+i*boxsize), (boxsize+3+j*boxsize)))
			color = color_rgb(matrix[i][j].red,matrix[i][j].green,matrix[i][j].blue)
			Rect.setFill(color)
			Rect.draw(win) 
								
def Flush(Pixel_Matrix):

	global sent
	if(Preview):Windowspreviev()
	for n in range(16):
		for m in range(16):
			Pixel_Matrix[n][m].cast()
	ser.write((1).to_bytes(1, byteorder='little'))
	sent+=1
	
if(debug):	
	start = timer()
	
DisplayMedia(flappe,0.1)

print("Gesendete Bytes:")

ser.close() 	
if(debug):
	end = timer()
	print(end - start)
	print("for this frame")

if(Preview):
	win.getMouse()
	win.close()
