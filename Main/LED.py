#!/usr/bin/python
import array
import time
import serial
import os.path
import os
import sys
from random import randint
from subprocess import call
from math import *
#from graphics import *
from timeit import default_timer as timer
from PIL import Image
from sys import platform
import numpy as np

if platform == "linux" or platform == "linux2":
    Serial = True
    print("Detected Linux OS, starting with serial enabled.")
else:
    Serial = False
    print("Detected Windows, starting without serial output.")


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

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


background = (255, 255, 255)
start = 0
boxsize = 40
cols = 16
rows = 16
hue = 1
matrix = [[0 for x in range(cols)] for x in range(rows)]
correcter = [[0 for x in range(cols)] for x in range(rows)]

Motiv = ''
lenght_validated = False
pos = 0
framenumber_int = 1
Picpath = os.path.dirname(os.path.abspath(
    sys.argv[0])) + "/static/Images/Pixels"


if Serial:
    ser = serial.Serial('/dev/ttyAMA0', 1000000, timeout=0.1)


class Media:
    def __init__(self, path, mode, requestedfps):
        self.path = path
        self.mode = mode
        self.fps = requestedfps

    def getpath(self):
        return self.path

    def getfps(self):
        return self.fps

    def getmode(self):
        return self.mode

    def setmode(self, mode):
        self.mode = mode


Files = {
    "mario": Media(os.path.dirname(os.path.abspath(sys.argv[0])) + "/Mario.bmp", None, 1),
    "flappe": Media(Picpath + "/flappy", None, 5),
    "nyancat": Media(Picpath + "/NyanCat/0.bmp", None, 4),
    "tetris": Media(Picpath + "/tetris", None, 12)
}

Media = Files["mario"]
path = Media.getpath()
px = Image.open(path).load()
WSH = None


def setWSH(WSHandler):
    global WSH
    WSH = WSHandler


class LED:
    def __init__(self, red, green, blue):
        self.red = int(red)
        self.green = int(green)
        self.blue = int(blue)

    def cast(self, out, hue):
        output = bytearray()
        output = out
        self.green = int(self.green*hue)
        if(self.green == 1):
            self.green += 1
        output.append((self.green))

        self.red = int(self.red*hue)
        if(self.red == 1):
            self.red += 1
        output.append((self.red))

        self.blue = int(self.blue*hue)
        if(self.blue == 1):
            self.blue += 1
        output.append((self.blue))
        return output


def findfps(Motiv):
    return Files[Motiv].getfps()


def isinFiles(Motiv):
    if Motiv in Files:
        return True
    else:
        return False


def CopytoMatrix(active_frame, step, posi):
    global matrix
    for n in range(cols):
        for m in range(rows):
            col = active_frame[n, m+step*posi]
            matrix[n][m] = LED((col[0]), col[1], col[2])
    Flush(matrix)


def Fill(matrix, r, g, b):
    for n in range(cols):
        for m in range(rows):
            matrix[n][m] = LED(r, g, b)
    return matrix


def singlecolor():
    global background
    r, g, b = background
    for n in range(cols):
        for m in range(rows):
            matrix[n][m] = LED(r, g, b)
    Flush(matrix)


def vertical():
    global framenumber_int
    global px
    global pos
    CopytoMatrix(px, 16, pos)
    if(pos == framenumber_int):
        pos = 0
    else:
        pos = pos+1


def multiple():
    global pos, Motiv
    global framenumber_int
    global lenght_validated

    if(lenght_validated):
        if(pos == framenumber_int):
            pos = 0
        picname = (str(pos)+".bmp")
        complete_filepath = Files[Motiv].getpath() + "/" + picname
        print(picname)
        Picture = Image.open(complete_filepath)
        px = Picture.load()
        CopytoMatrix(px, 0, 1)
        pos += 1
    else:
        picname = (str(pos)+".bmp")
        complete_filepath = Files[Motiv].getpath() + "/" + picname
        if((os.path.exists(complete_filepath)) == False):
            framenumber_int = pos
            lenght_validated = True
            pos = 0
        else:
            print(picname)
            Picture = Image.open(complete_filepath)
            px = Picture.load()
            CopytoMatrix(px, 0, 1)
            pos += 1


def single():
    global px

    CopytoMatrix(px, 0, 1)


def findmode(Motiv):
    global px, pos, framenumber_int
    pos = 0
    lenght_validated = False
    Media = Files[Motiv]
    if(Media.getmode() == None):
        if(Media.getpath()[-4:] == ".bmp"):
            Picture = Image.open(Files[Motiv].getpath())
            px = Picture.load()
            width, height = Picture.size
            if(height % 16 == 0 and width % 16 == 0):
                if(height > 16 and width == 16):
                    framenumber = height/16-1
                    framenumber_int = int(framenumber)
                    Media.setmode = 'v'
                    return 'v'  # 2, vertical
                elif(width > 16 and height == 16):
                    framenumber = width/16-1
                    framenumber_int = int(framenumber)
                    Media.setmode = 'h'
                    return 'h'  # 3, horizontal
                elif(height == 16 and width == 16):
                    Media.setmode = 's'
                    return 's'  # 1, single
        else:
            picname = "0.bmp"
            complete_filepath = os.path.join(Files[Motiv].getpath(), picname)
            Picture = Image.open(complete_filepath)
            px = Picture.load()
            width, height = Picture.size
            if(width == 16 and height == 16):
                Media.setmode = 'm'
                return 'm'  # 4, multiple()
        print("Filepath not valid")
        return 0
    else:
        return Media.getmode()


def Flush(Pixel_Matrix):
    global ser
    global WSH
    soutput = bytearray()
    woutput = []

    for n in range(cols):
        for m in range(rows):
            soutput = Pixel_Matrix[n][m].cast(soutput, hue)
    soutput.append(1)
    if(Serial):
        ser.write(soutput)

    for m in range(cols):
        for n in range(rows):
            woutput.append(Pixel_Matrix[n][m].red)
            woutput.append(Pixel_Matrix[n][m].green)
            woutput.append(Pixel_Matrix[n][m].blue)
    if(WSH):
        WSH.write_message(bytes(woutput), binary=True)

def numpy_flush(np_matrix_rgb):
    global ser
    global WSH
    
    shape = np_matrix_rgb.shape
    # dim all values with hue and floor to unit8, or ubytes
    np_matrix_dimmed = np.array(np_matrix_rgb * hue, np.ubyte)
    # convert matrix to grb matrix for the WS2812b LEDs
    np_matrix_dimmed_grb = np.flip(np_matrix_dimmed, 2) 
    # replace all 1s with 2s, because the Arduino interprets 1s as the seperation between pixels (g, r, b, 1, g, r, b, 1, ...)
    np_matrix_dimmed_grb_ones_removed = np.where(np_matrix_dimmed_grb == 1, 2, np_matrix_dimmed_grb)
    # generate a matrix of ones but with 4 color values per pixel and place our matrix in it, making every pixel (g, r, b, 1)
    np_matrix_dimmed_grb_ones_removed_seperated = np.ones((shape[0], shape[1], shape[2] + 1), np.ubyte)
    np_matrix_dimmed_grb_ones_removed_seperated[:, :, :3] = np_matrix_dimmed_grb_ones_removed
    # transpose the matrix just because my matrix is wired up column by column (sorry)
    np_matrix_dimmed_grb_ones_removed_seperated_transposed = np.transpose(np_matrix_dimmed_grb_ones_removed_seperated, (1, 0, 2))
    # write all the quadruplets into one 1D array, one after the other
    np_matrix_dimmed_grb_ones_removed_seperated_transposed_flat = np.ravel(np_matrix_dimmed_grb_ones_removed_seperated_transposed)
    # construct python bytes containing the raw data bytes in the array.
    serial_bytearray = np_matrix_dimmed_grb_ones_removed_seperated_transposed_flat.tobytes()

    # for the websocket and js canvas we just flatten the matrix row by row and cast it to bytes
    np_matrix_dimmed_flat = np.ravel(np_matrix_dimmed)
    websocket_bytearray = np_matrix_dimmed_flat.tobytes()

    if(Serial):
        ser.write(serial_bytearray)
    if(WSH):
        WSH.write_message(websocket_bytearray, binary=True)



def setMotiv(tbMotiv, mode):
    global Motiv, px, pos, lenght_validated
    Motiv = tbMotiv
    lenght_validated = False
    pos = 0
    if(mode in ('s', 'v', 'h')):
        Picture = Image.open(Files[Motiv].getpath())
        px = Picture.load()
