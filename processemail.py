#! /usr/bin/python3
"""
processemail.py
get email from procmail,
do something with it...

J. Knerr
Nov 2023
"""


import sys
import email
import email.parser
import os
from subprocess import getstatusoutput as gso
from utils import *
from pathlib import Path
from workout import *


def main():
    inputstdin = sys.stdin
    msg = email.parser.Parser().parse(inputstdin)
    # email.message.Message object
    if msg.is_multipart():
        for m in msg.get_payload():
            text = parse_single_body(m)
    else:
        text = parse_single_body(msg)
#   debug(msg)
    sub = msg['Subject']
    frm = msg['From']

    # if they replied with done in subject or message text
    rsynccom = "rsync -av --delete games ~/public_html"
    if ("done" in sub.lower()) or ("done" in text.lower()):
        # starts in ~/mdir
        path = "/home/knerr/repos/workout-bingo"
        os.chdir(path)
        # if it's from a valid player
        emails = readEmails()
        for e in emails:
            if e in frm:
                # get workout
                w = readCurrentWorkout()
                g = readCurrentGame()
                if w is not None:
                    # check .done file
                    alreadyDone = readDone(e, g)
                    if not alreadyDone:
                        markcard(e, w, g)
                        # rsync over to pub_html
                        status, output = gso(rsynccom)
                        # check for winner/gameover
                        if checkwinner(e, g):
                            # touch .nogame file
                            Path(".nogame").touch()
                            # email all that game is over
                            return


def checkwinner(e, g):
    """check if game over/someone has won"""
    # read in e's card.txt file
    cardfile = "./games/%d/%s/card.txt" % (g, e)
    cardState = readState(cardfile)
    # cardState is list of Workout objects
    # first 5 are j=0, next 5 are j=1, next 5 are j=2, etc
    # check all of the options (rows, cols, diags)
    # if any are all 1's, set gameover to True
    # first check the rows
    for j in range(5):
        counter = 0
        for i in range(5):
            k = i + j
            if cardState[k].isDone():
                counter += 1
        if counter == 5:
            return True
    # now check the columns
    for i in range(5):
        counter = 0
        for j in range(5):
            k = (j*5) + i
            if cardState[k].isDone():
                counter += 1
        if counter == 5:
            return True
    # last check the diagonals
    counter = 0
    for k in [0, 6, 12, 18, 24]:
        if cardState[k].isDone():
            counter += 1
    if counter == 5:
        return True
    counter = 0
    for k in [20, 16, 12, 8, 4]:
        if cardState[k].isDone():
            counter += 1
    if counter == 5:
        return True
    # if we get here, game is not over yet    
    return False


def markcard(e, w, g):
    """given email, workout, and game number, mark that player's card"""
    cfile = "./games/%d/%s/card.txt" % (g, e)
    ifile = "./games/%d/%s/card.png" % (g, e)
    # run markcard.py to mark the card.png file
    com = "python3 markcard.py --workout %s --cardfile %s --imgfile %s" % (w, cfile, ifile)
    status, output = gso(com)
    # set .done to 1
    dfile = "./games/%d/%s/.done" % (g, e)
    outf = open(dfile, "w")
    outf.write("1\n")
    outf.close()
    os.chmod(dfile, 0o644)
    os.chmod(cfile, 0o644)
    os.chmod(ifile, 0o644)


def parse_single_body(email):
    payload = email.get_payload(decode=True)
    # The payload is binary. It must be converted to
    # python string depending on input charset
    # Input charset may vary, based on message
    try:
        text = payload.decode("utf-8")
        return text
    except UnicodeDecodeError:
        print("Error: cannot parse message as UTF-8")
        return  


def debug(msg):
    """write debug info to file in ~/mdir"""
    ofile = open("debug.txt", "w")
    ofile.write("\n")
    ofile.write(str(type(msg)))
    ofile.write("\n")
    ofile.write("S: " + msg['Subject'] + "\n")
    ofile.write("F: " + msg['From'] + "\n")
    ofile.write("T: " + msg['To'] + "\n")
    if msg.is_multipart():
        for m in msg.get_payload():
            text = parse_single_body(m)
    else:
        # Single part message is passed directly
        text = parse_single_body(msg)
    ofile.write("===================\n")
    ofile.write(text)
    ofile.write("\n===================\n")
    ofile.close()


main()
