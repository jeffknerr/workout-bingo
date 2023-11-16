"""
newgame.py
start a new game, set up directories

J. Knerr
Fall 2023
"""

from random import randrange
from workout import *
from subprocess import getstatusoutput as gso
from utils import *
import os


def main():
    # read in player emails
    emails = readEmails()
    # get last game's number, update for new game
    gamenum = readCurrentGame()
    if gamenum is None:
        gamenum = 1000
    else:
        gamenum += 1
    # write new .current_game file
    outf = open(".current_game", "w")
    outf.write("%d\n" % (gamenum))
    outf.close()
    # delete .nogame if it exists
    try:
        os.remove(".nogame") 
    except FileNotFoundError:
        pass
    # make new game dir
    status, output = gso("mkdir -p games/%d" % gamenum)
    # make email subdirs
    # make card statefile for each email
    # run makecard file for each email/statefile
    # create .done file for current workout
    for email in emails:
        print(email)
        pdir = "games/%d/%s" % (gamenum, email)
        com = "mkdir -p %s" % (pdir)
        status, output = gso(com)
        newcard(pdir)
        newcardimage(pdir)
        newdonefile(pdir)
        # also send email with url???


def newcard(pdir):
    """given a player dir, create a new/random card statefile there"""
    outf = open(pdir+"/card.txt", "w")
    outf.write("#i,j,workout,done(1)/not(0)\n")
    for j in range(5):
        for i in range(5):
            wkt = randrange(1, 11)
            done = 0
            if i == 2 and j == 2:
                wkt = "FREE"
                done = 1
            outf.write("%d,%d,%s,%d\n" % (i, j, str(wkt), done))
    outf.close()


def newcardimage(pdir):
    """given a player dir and card.txt file, create their png image file"""
    com = "python3 makecard.py --path=%s" % pdir
    print(pdir, com)
    status, output = gso(com)
    if status != 0:
        print("uh oh....")
        print(status)


def newdonefile(pdir):
    """given a player dir, make the .done file"""
    com = "echo 1 > %s/.done" % pdir
    status, output = gso(com)
    if status != 0:
        print("uh oh....")
        print(status)


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
