"""
try making a workout email for use with bingo cards

- get countdown until ski trip
- pick random workout
- pick random quote
- set all .done to 0
- send unique emails to all

J. Knerr
Fall 2023
"""

import glob
from random import randrange
from datetime import datetime
import smtplib
from email.message import EmailMessage
from utils import *
import os
import sys


def main():
    variables = readVars()
    PATH = variables["PATH"]
    PREFIX = variables["PREFIX"]
    START = variables["START"]
    EMAILFROM = variables["EMAILFROM"]
    SERVER = variables["SERVER"]
    os.chdir(PATH)
    if os.path.isfile(".nogame"):
        print("no game right now...")
        sys.exit(1)
    lines = ""

    today = datetime.today()
    lines += "\n\ndate: %s\n" % (today)
    skiday = datetime(year=2024, month=2, day=4, hour=8)
    countdown = skiday - today
    lines += "\ndays until first ski run!!! %s\n" % (countdown)

    wkts = readWorkouts()
    n = randrange(len(wkts))
    # save workout for use in processemail
    outf = open(".current_workout", "w")
    outf.write("%d\n" % (n+1))
    outf.close()
    lines += "\ntoday's workout (W%d): \n" % (n+1)
    for i in range(len(wkts[n])):
        lines += "%d. %s\n" % (i+1, wkts[n][i].strip())
    quotes = readQuotes()
    lines += "\ntoday's quote:\n"
    qnum = randrange(len(quotes))
    lines += quotes[qnum][0]+"\n"
    lines += "\t\t-- %s\n\n" % (quotes[qnum][1])
    lines += """
*** reply and add "done" to the subject or message to mark workout as Done! ***
    """
    subject = PREFIX + " " + ("ski workout email for %s" % today)
    sendmail(lines, subject, START, EMAILFROM, SERVER)


def sendmail(lines, subject, START, EMAILFROM, SERVER):
    """send the lines in an email"""
    if len(lines) > 0:
        inf = open(".current_game",  "r")
        gamenum = inf.readline().strip()
        inf.close()
        emails = readEmails()
        for EMAILTO in emails:
            url = "\n\nYour current bingo card url:\n"
            url += "%s/games/%s/%s/card.png\n\n" % (START, gamenum, EMAILTO)
            uniqmsg = lines + url
            msg = EmailMessage()
            msg.set_content(uniqmsg)
            msg['Subject'] = subject
            msg['From'] = EMAILFROM
            msg['To'] = EMAILTO
#           msg['Cc'] = EMAILTO
            msg['Reply-To'] = EMAILFROM
            s = smtplib.SMTP(SERVER)
            s.send_message(msg)
            s.quit()
            setdone(gamenum, EMAILTO)


def setdone(gamenum, EMAILTO):
    """set player's .done file to 0"""
    outf = open("games/%s/%s/.done" % (gamenum, EMAILTO), "w")
    outf.write("0\n")
    outf.close()


main()
