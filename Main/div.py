import os
from platform import platform
from time import strftime, localtime, strptime

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

    def writetofile(path, Scores):

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
    writetofile(fullpath, Scores)
    return rank