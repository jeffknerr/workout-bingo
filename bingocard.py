"""
try making a bingo card with workout data

J. Knerr
Fall 2023
"""

from graphics import *
import glob
from random import randrange

def main():
    w = 1000
    h = 1000
    gw = GraphWin("bingo card", w, h)
    gw.setCoords(0, 0, 5, 5)
    wkts = readWorkouts()
    for i in range(5):
        for j in range(5):
            n = randrange(len(wkts))
            print(i, j, n, wkts[n])
            p = Point(i+0.5, j+0.5)
            if i==2 and j==2:
                t = Text(p, "** FREE **")
            else:
                t = Text(p, "".join(wkts[n]))
                wnum = "W%d" % (n+1)
                p = Point(i+0.5, j+0.85)
                t2 = Text(p, wnum)
                t2.draw(gw)
            t.draw(gw)
    drawLines(gw)
    gw.getKey()

def drawLines(gw):
    """draw the box lines"""
    W = 3
    for i in range(6):
        p1 = Point(i, 0)
        p2 = Point(i, 5)
        l = Line(p1, p2)
        l.setWidth(W)
        l.draw(gw)
    for j in range(6):
        p1 = Point(0, j)
        p2 = Point(5, j)
        l = Line(p1, p2)
        l.setWidth(W)
        l.draw(gw)

def readWorkouts():
    """read in the workouts"""
    wkts = []
    files = glob.glob("w*.txt")
    for f in files:
        inf = open(f, "r")
        lines = inf.readlines()
        wkts.append(lines)
        inf.close()
    return wkts

main()
