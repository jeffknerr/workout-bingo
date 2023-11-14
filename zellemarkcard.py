"""
mark a bingo card, if it has the given workout

J. Knerr
Fall 2023
"""

from random import choice
import click
from workout import *
from subprocess import getstatusoutput as gso


@click.command()
@click.option("--workout", required=True, help="workout to mark done")
@click.option("--cardfile", required=True, help="bingo card state file")
def main(workout, cardfile):
    # read in workout state file
    cardState = readState(cardfile)
    # find matching workout locations that are not done yet
    locations = check(cardState, workout)
    if len(locations) > 0:
        # pick one
        location = choice(locations)
        # update cardState
        location.setDone()
        print(location)
        # write out new state.txt file
        writeCard(cardState, cardfile)
        # call imagemagick to mark the card image file
        magick(location, cardfile)


def magick(location, cardfile):
    """mark the png file at the given location"""
    x = 60 + 200*location.geti()
    y = 130 + 200*location.getj()
    innercom = "text %d,%d 'X'" % (x, y)
    f1 = "card.png"
    f2 = "output.png"
    com = 'convert -font helvetica -fill blue -pointsize 100 -draw "%s" %s %s' % (innercom, f1, f2) 
    status, output = gso(com)
    print(status, output)


def readState(cardfile):
    """given a cardx.txt filename, read in state of card"""
    workouts = []
    inf = open(cardfile, "r")
    for line in inf:
        if not line.startswith("#"):
            i, j, w, d = line.strip().split(",")
            w = Workout(int(i), int(j), w, int(d))
            workouts.append(w)
    inf.close()
    return workouts


def check(cardState, workout):
    """see if workout is in the card, return list of matching locations"""
    locations = []
    for w in cardState:
        if (w.getWorkout() == workout) and w.notDone():
            locations.append(w)
    return locations


def writeCard(cardState, cardfile):
    """write out cardState to new txt file"""
    inf = open("new"+cardfile, "w")
    header = "#i,j,workout,done(1)/not(0)"
    inf.write(header + "\n")
    for workout in cardState:
        i = workout.geti()
        j = workout.getj()
        w = workout.getWorkout()
        d = workout.getDone()
        inf.write("%s,%s,%s,%s\n" % (str(i), str(j), str(w), str(d)))
    inf.close()


main()
