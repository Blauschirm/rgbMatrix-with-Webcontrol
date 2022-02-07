import os
import sys
from platform import platform
from time import localtime, strftime, strptime

import numpy as np
from PIL import Image, ImageOps

def get_char_bitmap(character = ''):
    font_map_path = os.path.dirname(os.path.abspath(sys.argv[0])) + "/static/Images/font_map.bmp"
    grid_width = 6
    grid_height = 6
    padding_x = 1
    padding_y = 1

    map = [
            ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M'],
            ['N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ']
    ]

    def findItem(theList, item):
        return [(ind, theList[ind].index(item)) for ind in range(len(theList)) if item in theList[ind]][0]

    with Image.open(font_map_path) as im:
        (n, m) = findItem(map, character)
        im_inverted = ImageOps.invert(im)
        im_bw = im_inverted.convert('1')
        crop_region = (m * grid_width + padding_x, n * grid_height + padding_y, (m + 1) * grid_width, (n + 1) * grid_height)
        char_bitmap = im_bw.crop(crop_region)
         
    return(np.array(char_bitmap))

def make_folder(basepath):

    def supermakedirs(path, mode):
        if not path or os.path.exists(path):
            return []
        (head, tail) = os.path.split(path)
        res = supermakedirs(head, mode)
        os.mkdir(path)
        os.chmod(path, mode)
        print("set permission to {}".format(mode))
        res += [path]
        return res

    if not os.path.exists(basepath):		
        if platform == "linux" or platform == "linux2":
            supermakedirs(basepath, 0o755)
        else:
            os.makedirs(basepath)

def readHighscores(path):
    Scores=[]
    if os.path.exists(path):
        with open(path,mode='r') as rawScores:
            for line in rawScores:
                tmp=line.strip()
                tmp=tmp.split(',')
                tmp[0] = int(tmp[0])
                tmp[1] = strptime(tmp[1], "%X %x")
                Scores.append(tmp)
    return(Scores)

def writeHighscore(score, name):
    rank=0

    def writetofile(Scores):

        make_folder(basepath)

        with open(fullpath,mode='w+') as rawScores:
            for Score in Scores:
                tmp = str(Score[0]) + ',' + strftime("%X %x",Score[1]) + ',' + Score[2] + '\n'
                rawScores.write(tmp)


    basepath= os.path.join(os.path.dirname(__file__), 'saves')
    fullpath = os.path.join(basepath, "snake.txt")
    
    Scores=readHighscores(fullpath)
    newScore=[score, localtime(), name]

    for index, Score in enumerate(Scores):
        if newScore[0] > Score[0]:
            Scores.insert(index,newScore)
            rank = index + 1
            Scores=Scores[:100]
            writetofile(fullpath, Scores)
            return rank

    Scores.append(newScore)
    rank = len(Scores) + 1
    writetofile(Scores)
    return rank
