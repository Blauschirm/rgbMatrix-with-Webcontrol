from LED import Flush, LED
import time 
from datetime import datetime
from div import get_char_bitmap
import numpy as np

class Clock():

    def __init__(self, config):
        self.config = config
        self.OffColor = 0, 0, 0
 

    def update(self):
        self.OnColor = self.config.colors["highlight"]
        self.Matrix = [[0 for x in range(16)] for x in range(16)]
        self.hours =  datetime.strftime(datetime.now(), "%H")
        self.minutes =  datetime.strftime(datetime.now(), "%M")

        frame = np.array(self.Matrix)
        frame[2:7, 3:8] = get_char_bitmap(self.hours[0])
        frame[2:7, 9:14] = get_char_bitmap(self.hours[1])
        frame[9:14, 3:8] = get_char_bitmap(self.minutes[0])
        frame[9:14, 9:14] = get_char_bitmap(self.minutes[1])
        frame = np.transpose(frame)

        self.Matrix = np.where(frame == 1, LED(*self.OnColor), frame)
        self.Matrix = np.where(self.Matrix == 0, LED(*self.OffColor), self.Matrix)
        Flush(self.Matrix)



if __name__ == "__main__":

    clock = Clock()
    clock.update()
    clock.update()