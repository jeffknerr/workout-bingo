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

def main():
    inputstdin = sys.stdin
    msg = email.parser.Parser().parse(inputstdin)
    # email.message.Message object
    if msg.is_multipart():
        for m in msg.get_payload():
            text = parse_single_body(m)
    else:
        text = parse_single_body(msg)
#   ofile = open("debug.txt", "w")
#   ofile.write("\n")
#   ofile.write(str(type(msg)))
#   ofile.write("\n")
#   ofile.write("S: " + msg['Subject'] + "\n")
#   ofile.write("F: " + msg['From'] + "\n")
#   ofile.write("T: " + msg['To'] + "\n")
#   if msg.is_multipart():
#       for m in msg.get_payload():
#           text = parse_single_body(m)
#   else:
#       # Single part message is passed directly
#       text = parse_single_body(msg)
#   ofile.write("===================\n")
#   ofile.write(text)
#   ofile.write("\n===================\n")
#   ofile.close()
    sub = msg['Subject']
    frm = msg['From']

    # if they replied with done
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


def markcard(e, w, g):
    """given email and workout, mark that player's card"""
    # cd to correct dir
    os.chdir("./games/%s/%s" % (g, e))
    # run ../../../markcard.py to mark the card.png file
    com = "python3 ../../../markcard.py --workout %s --cardfile card.txt" % w
    status, output = gso(com)
    # set .done to 1
    outf = open(".done", "w")
    outf.write("1\n")
    outf.close()
    # rsync over to pub_html


def readDone(e, g):
    """read in current player (e) done file"""
    try:
        path = "games/%s/%s/.done" % (g, e)
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
        w = str(inf.readline().strip()) + 1
        inf.close()
        return w
    except FileNotFoundError:
        return None


def readCurrentGame():
    """read in current game number"""
    try:
        inf = open(".current_game", "r")
        g = inf.readline().strip()
        inf.close()
        return g
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
