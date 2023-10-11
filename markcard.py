"""
mark a bingo card, if it has the given workout

J. Knerr
Fall 2023
"""

import graphics
import glob
from random import choice
import click


@click.command()
@click.option("--workout", required=True, help="workout to mark done")
@click.option("--cardfile", required=True, help="bingo card state file")
def main(workout, cardfile):
    # read in workout state file
    # if given workout is not done in state file,
    # put an X in the correct spot
    # update state file and card image
    cardState = readState(cardfile)
    locations = check(cardState, workout)
    if len(locations) > 0:
        location = choice(locations)
        # update cardState
        locations[location] = 1
        # write out new state
        # write out new card


def readState(cardfile):
    """given a cardx.txt filename, read in state of card"""
    return []


def check(cardState, workout):
    """see if workout is in the card, return list of locations"""
    locations = []
    return locations


def writeCard(cardState):
    """write out cardState to new image file"""
    w = 1000
    h = 1000
    gw = graphics.GraphWin("bingo card", w, h)
    gw.setCoords(0, 0, 5, 5)
    wkts = readWorkouts()
    for i in range(5):
        for j in range(5):
            n = cardState[i][j][2]
            p = graphics.Point(i+0.5, j+0.5)
            if i == 2 and j == 2:
                t = graphics.Text(p, "** FREE **")
            else:
                t = graphics.Text(p, "".join(wkts[n]))
                wnum = "W%d" % (n+1)
                p = graphics.Point(i+0.5, j+0.85)
                t2 = graphics.Text(p, wnum)
                t2.draw(gw)
            t.draw(gw)
    drawLines(gw)
    gw.getKey()


def drawLines(gw):
    """draw the box lines"""
    W = 3
    for i in range(6):
        p1 = graphics.Point(i, 0)
        p2 = graphics.Point(i, 5)
        lh = graphics.Line(p1, p2)
        lh.setWidth(W)
        lh.draw(gw)
    for j in range(6):
        p1 = graphics.Point(0, j)
        p2 = graphics.Point(5, j)
        lv = graphics.Line(p1, p2)
        lv.setWidth(W)
        lv.draw(gw)


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
