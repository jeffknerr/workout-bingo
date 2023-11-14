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


def main():
    lines = ""

    today = datetime.today()
    lines += "\n\ndate: %s\n" % (today)
    skiday = datetime(year=2024, month=2, day=4, hour=8)
    countdown = skiday - today
    lines += "\ndays until first ski run!!! %s\n\n" % (countdown)

    wkts = readWorkouts()
    n = randrange(len(wkts))
    # save workout for use in processemail
    outf = open(".current_workout", "w")
    outf.write("%d\n" % n)
    outf.close()
    lines += "\ntoday's workout (W%d): \n" % (n+1)
    for i in range(len(wkts[n])):
        lines += "%d. %s\n" % (i+1, wkts[n][i].strip())
    lines += "\n\n"
    lines += """

*** reply with "done" in subject or message to mark workout as Done! ***

    """
    quotes = readQuotes()
    lines += "today's quote:\n"
    qnum = randrange(len(quotes))
    lines += quotes[qnum][0]+"\n"
    lines += "\t\t-- %s\n\n" % (quotes[qnum][1])
    subject = "[JK Bingo] ski workout email for %s" % today
    sendmail(lines, subject)


def sendmail(lines, subject):
    """send the lines in an email"""
    if len(lines) > 0:
        START = "https://www.cs.swarthmore.edu/~knerr"
        inf = open(".current_game",  "r")
        gamenum = inf.readline().strip()
        inf.close()
        emails = readEmails()
        EMAILFROM = "knerr@cs.swarthmore.edu"
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
            s = smtplib.SMTP('allspice.cs.swarthmore.edu')
            s.send_message(msg)
            s.quit()
            setdone(gamenum, EMAILTO)


def setdone(gamenum, EMAILTO):
    """set player's .done file to 0"""
    outf = open("games/%s/%s/.done" % (gamenum, EMAILTO), "w")
    outf.write("0\n")
    outf.close()


def readQuotes():
    """read in the witty quotes"""
    qts = []
    inf = open("quotes.txt", "r")
    for line in inf:
        quote, who = line.strip().split("#")
        qts.append([quote, who])
    inf.close()
    return qts


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


def readEmails():
    """read in the email addresses"""
    emails = []
    inf = open(".emails", "r")
    for line in inf:
        email = line.strip()
        emails.append(email)
    inf.close()
    return emails


main()
