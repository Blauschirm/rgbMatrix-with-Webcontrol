#!/usr/bin/python

from sys import platform
import numpy as np
import serial

if platform == "linux" or platform == "linux2":
    Serial = True
    print("Detected Linux OS, starting with serial enabled.")
else:
    Serial = False
    print("Detected Windows, starting without serial output.")

brightness = 1

if Serial:
    ser = serial.Serial('/dev/ttyAMA0', 1000000, timeout=0.1)

active_websockets = set()

def setWSH(active_ws):
    global active_websockets
    active_websockets = active_ws

def numpy_flush(matrix_rgb):

    rgb_to_grb_conversion = np.array([1, 0, 2])
    white_balance_values = np.array([1, 0.96, 0.82])

    np_matrix_rgb = np.array(matrix_rgb, np.ubyte)
    # dim all values with hue and floor to unit8, or ubytes
    np_matrix_dimmed = np.array(np_matrix_rgb * brightness, np.ubyte)
    # apply the white balance for the LEDs
    np_matrix_dimmed_wb = np.array(np_matrix_dimmed * white_balance_values, np.ubyte)
    # convert matrix to grb matrix for the WS2812b LEDs
    np_matrix_dimmed_wb_grb = np_matrix_dimmed_wb[:, :, rgb_to_grb_conversion]
    # replace all 1s with 2s, because the Arduino interprets 1s as the seperation between frames
    np_matrix_dimmed_wb_grb_ones_removed = np.where(
        np_matrix_dimmed_wb_grb == 1, 2, np_matrix_dimmed_wb_grb)
    # transpose the matrix just because my matrix is wired up column by column (sorry)
    np_matrix_dimmed_wb_grb_ones_removed_transposed = np.transpose(
        np_matrix_dimmed_wb_grb_ones_removed, (1, 0, 2))

    # write all the quadruplets into one 1D array, one after the other
    np_matrix_dimmed_wb_grb_ones_removed_transposed_flat = np.ravel(
        np_matrix_dimmed_wb_grb_ones_removed_transposed)
    # construct python bytes containing the raw data bytes in the array.
    serial_bytearray = bytearray(
        np_matrix_dimmed_wb_grb_ones_removed_transposed_flat)
    # add the 1 to mark the end of the frame
    serial_bytearray.append(1)

    # for the websocket and js canvas we just flatten the matrix row by row and cast it to bytes
    np_matrix_dimmed_flat = np.ravel(np_matrix_dimmed)
    websocket_bytearray = bytes(np_matrix_dimmed_flat)

    if(Serial):
        ser.write(serial_bytearray)
    if(active_websockets):
        for wsh in active_websockets:
            wsh.write_message(websocket_bytearray, binary=True)

