"""
start a new game, set up directories

J. Knerr
Fall 2023
"""

import glob
from random import randrange
from workout import *
from subprocess import getstatusoutput as gso


def main():
    # read in emails, get current game number
    emails = readEmails()
    gamenum = readCurrentGame()
    # make new game dir
    status, output = gso("mkdir -p games/%d" % gamenum)
    # make email subdirs
    # make card statefile for each email
    # run makecard file for each email/statefile
    for email in emails:
        print(email)
        pdir = "games/%d/%s" % (gamenum, email)
        com = "mkdir -p %s" % (pdir)
        status, output = gso(com)
        newcard(pdir)


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


def readEmails():
    """read in player emails"""
    emails = []
    try:
        inf = open(".emails", "r")
        for line in inf:
            email = line.strip()
            emails.append(email)
        inf.close()
    except FileNotFoundError:
        print("No .emails file??? Add emails, 1 per line, to .emails file!")
    return emails
       

def readCurrentGame():
    """read in current game number, increment"""
    try:
        inf = open(".current_game", "r")
        oldnum = int(inf.readline().strip())
        newnum = oldnum + 1
        inf.close()
    except FileNotFoundError:
        newnum = 1000
    outf = open(".current_game", "w")
    outf.write("%d\n" % (newnum))
    outf.close()
    return newnum
        

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
