from LED import numpy_flush
from datetime import datetime
from div import get_char_bitmap
import numpy as np
import math

class Clock():

    def __init__(self, config):
        self.config = config
        self.OffColor = (0, 0, 0)
 

    def update(self):
        on_color = self.config["config_colors_highlight"]
        hours =  datetime.strftime(datetime.now(), "%H")
        minutes =  datetime.strftime(datetime.now(), "%M")

        frame = np.zeros((16,16))

        if self.config["config_clock_offset"]:
            frame[1:6, 1:6] = get_char_bitmap(hours[0])
            frame[1:6, 7:12] = get_char_bitmap(hours[1])
            frame[10:15, 5:10] = get_char_bitmap(minutes[0])
            frame[10:15, 11:16] = get_char_bitmap(minutes[1])
        else:
            frame[2:7, 3:8] = get_char_bitmap(hours[0])
            frame[2:7, 9:14] = get_char_bitmap(hours[1])
            frame[9:14, 3:8] = get_char_bitmap(minutes[0])
            frame[9:14, 9:14] = get_char_bitmap(minutes[1])

        matrix = [[on_color if r == 1 else self.OffColor for r in c] for c in frame]

        if self.config["config_clock_seconds"]:
            
            seconds = datetime.now().second
            us_in_s = datetime.now().microsecond / 1000000
            
            sf = np.zeros(60)
            sm = np.zeros((16,16))    

            sf[seconds] = 1
            if self.config["config_clock_seconds_smoothed"]:
                sf[( seconds - 1 )%60] = 1 - us_in_s
                sf[( seconds + 1 )%60] = us_in_s

            sm[0, 8:16] = sf[0:8]
            sm[1:16, 15] = sf[8:23]
            sm[15, 0:15] = np.flip(sf[23:38])
            sm[0:15, 0] = np.flip(sf[38:53])
            sm[0, 1:8] = sf[53:60]

            frame_with_seconds_dot = np.full((16,16,3), on_color) * sm.reshape((16,16,1))
            matrix = matrix + frame_with_seconds_dot
        
        numpy_flush(matrix)
