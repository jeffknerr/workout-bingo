"""
mark a bingo card, if it has the given workout

J. Knerr
Fall 2023
"""

from random import choice
import click
import os
from workout import *
from subprocess import getstatusoutput as gso
from utils import *


@click.command()
@click.option("--workout", required=True, help="workout to mark done")
@click.option("--cardfile", required=True, help="bingo card state file")
@click.option("--imgfile", required=True, help="bingo card image file")
def main(workout, cardfile, imgfile):
    # read in workout state file
    cardState = readState(cardfile)
    # find matching workout locations that are not done yet
    locations = check(cardState, workout)
    if len(locations) > 0:
        # pick one
        location = choice(locations)
        # update cardState
        location.setDone()
#       print(location)
        # write out new state.txt file
        writeCard(cardState, cardfile)
        # call imagemagick to mark the card image file
        magick(location, cardfile, imgfile)


def magick(location, cardfile, imgfile):
    """mark the png file at the given location"""
    xoffset = 125+45
    yoffset = 120+110
    boxsize = 155
    x = xoffset + boxsize*location.geti()
    y = yoffset + boxsize*location.getj()
    innercom = "text %d,%d 'X'" % (x, y)
    f1 = imgfile
    f2 = "output.png"
    com = 'convert -font helvetica -fill blue -pointsize 100 -draw "%s" %s %s' % (innercom, f1, f2) 
    status, output = gso(com)
    if status == 0:
        os.rename(f2, f1)
#   print(status, output)


def check(cardState, workout):
    """see if workout is in the card, return list of matching locations"""
    locations = []
    for w in cardState:
        if (w.getWorkout() == workout) and w.notDone():
            locations.append(w)
    return locations


def writeCard(cardState, cardfile):
    """write out cardState to new txt file"""
    newfile = "newcard.txt"
    inf = open(newfile, "w")
    header = "#i,j,workout,done(1)/not(0)"
    inf.write(header + "\n")
    for workout in cardState:
        i = workout.geti()
        j = workout.getj()
        w = workout.getWorkout()
        d = workout.getDone()
        inf.write("%s,%s,%s,%s\n" % (str(i), str(j), str(w), str(d)))
    inf.close()
    os.rename(newfile, cardfile)


main()
