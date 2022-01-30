from LED import Flush, LED
import time 
from datetime import datetime

class BinCounter():

    def __init__(self, c = 0):
        self.count = c
        self.Matrix = [[0 for x in range(16)] for x in range(16)]
        self.OnColor = 255, 120, 0
        self.OffColor = 0, 0, 0
        self.BDay = int(datetime.strptime("20 26 Nov 1993", "%H %d %b %Y").timestamp() * 1000)
        print(self.BDay)

    def update(self):
        #count = self.count
        count = int(round(time.mktime(time.localtime()) * 1000)) + datetime.now().microsecond//1000 - self.BDay
        print(count)
        #print(count)
        for j in range(16):
            for i in range(16):
                if count:
                    if count & 1:
                        self.Matrix[i][j] = LED(*self.OnColor)
                    else:
                        self.Matrix[i][j] = LED(*self.OffColor)
                    count = count >> 1
                else:
                    self.Matrix[i][j] = LED(*self.OffColor)
        Flush(self.Matrix)
        self.count += 1

if __name__ == "__main__":

    BC = BinCounter()
    while 1:
        BC.update()
        time.sleep(0.1)
