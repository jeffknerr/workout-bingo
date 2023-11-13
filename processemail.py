#! /usr/bin/python3
"""
processemail.py
get email from procmail,
do something with it...

J. Knerr
Nov 2023
"""

import sys
from subprocess import getstatusoutput as gso
import email
import email.parser
import os


def main():
    inputstdin = sys.stdin
    msg = email.parser.Parser().parse(inputstdin)
#   ofile = open("debug.txt", "w")
#   ofile.write("S: " + msg['Subject'] + "\n")
#   ofile.write("F: " + msg['From'] + "\n")
#   ofile.write("T: " + msg['To'] + "\n")
#   ofile.close()
    sub = msg['Subject']
    frm = msg['From']

    # if they replied with done
    if "done" in sub.lower():
        # starts in ~/mdir
        path = "/home/knerr/repos/workout-bingo"
        os.chdir(path)
        # if it's from a valid player
        emails = readEmails()
        for e in emails:
            if e in frm:
                # get workout
                w = readCurrentWorkout()
                if w != None:
                    # check .done file
                    alreadyDone = readDone(e)
                    if not alreadyDone: 
                        markcard(e, w)


def readDone(e):
    """read in current player (e) done file"""
    inf = open(".current_game", "r")
    g = inf.readline().strip()
    inf.close()
    try:
        path = "games/%s/%s/.done" % (g,e)
        inf = open(path, "r")
        d = inf.readline().strip()
        inf.close()
        return d == 1
    except FileNotFoundError:
        return True

def readCurrentWorkout():
    """read in current workout number"""
    try:
        inf = open(".current_workout", "r")
        w = inf.readline().strip()
        inf.close()
        return w
    except FileNotFoundError:
        return None

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


main()
