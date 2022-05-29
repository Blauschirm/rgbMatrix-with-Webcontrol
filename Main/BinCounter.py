from LED import numpy_flush
import time 
from datetime import datetime

class BinCounter():

    def __init__(self, config = {}, c = 0):
        self.count = c
        self.Matrix = [[0 for x in range(16)] for x in range(16)]
        self.config = config
        self.OffColor = (0, 0, 0)
        self.BDay = int(datetime.strptime("20 26 Nov 1993", "%H %d %b %Y").timestamp() * 2)

    def update(self):
        count = int(round(time.mktime(time.localtime()) * 2)) + datetime.now().microsecond//500000 - self.BDay
        for j in range(16):
            for i in range(16):
                if count:
                    if count & 1:
                        self.Matrix[j][i] = self.config["config_colors_highlight"] if "config_colors_highlight" in self.config else (255, 120, 0)
                    else:
                        self.Matrix[j][i] = self.OffColor
                    count = count >> 1
                else:
                    self.Matrix[j][i] = self.OffColor
        numpy_flush(self.Matrix)
        self.count += 1

if __name__ == "__main__":

    BC = BinCounter()
    for i in range(5):
        BC.update()
        time.sleep(0.1)
