#!/usr/bin/python

from random import randint
from sys import platform
import numpy as np
import serial

if platform == "linux" or platform == "linux2":
    Serial = True
    print("Detected Linux OS, starting with serial enabled.")
else:
    Serial = False
    print("Detected Windows, starting without serial output.")


# mark1
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

cols = 16
rows = 16
hue = 1
matrix = np.zeros((cols, rows, 3))
correction_matrix = np.zeros((cols, rows, 3))


if Serial:
    ser = serial.Serial('/dev/ttyAMA0', 1000000, timeout=0.1)

WSH = None

def setWSH(WSHandler):
    global WSH
    WSH = WSHandler


def numpy_flush(matrix_rgb):
    global ser
    global WSH

    rgb_to_grb_conversion = np.array([1, 0, 2])

    np_matrix_rgb = np.array(matrix_rgb, np.ubyte)
    # dim all values with hue and floor to unit8, or ubytes
    np_matrix_dimmed = np.array(np_matrix_rgb * hue, np.ubyte)
    # convert matrix to grb matrix for the WS2812b LEDs
    np_matrix_dimmed_grb = np_matrix_dimmed[:, :, rgb_to_grb_conversion]
    # replace all 1s with 2s, because the Arduino interprets 1s as the seperation between frames
    np_matrix_dimmed_grb_ones_removed = np.where(
        np_matrix_dimmed_grb == 1, 2, np_matrix_dimmed_grb)
    # transpose the matrix just because my matrix is wired up column by column (sorry)
    np_matrix_dimmed_grb_ones_removed_transposed = np.transpose(
        np_matrix_dimmed_grb_ones_removed, (1, 0, 2))

    # write all the quadruplets into one 1D array, one after the other
    np_matrix_dimmed_grb_ones_removed_transposed_flat = np.ravel(
        np_matrix_dimmed_grb_ones_removed_transposed)
    # construct python bytes containing the raw data bytes in the array.
    serial_bytearray = bytearray(
        np_matrix_dimmed_grb_ones_removed_transposed_flat)
    # add the 1 to mark the end of the frame
    serial_bytearray.append(1)

    # for the websocket and js canvas we just flatten the matrix row by row and cast it to bytes
    np_matrix_dimmed_flat = np.ravel(np_matrix_dimmed)
    websocket_bytearray = bytes(np_matrix_dimmed_flat)

    if(Serial):
        ser.write(serial_bytearray)
    if(WSH):
        WSH.write_message(websocket_bytearray, binary=True)
