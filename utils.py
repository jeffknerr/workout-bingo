"""
utils.py
put stuff in here used by other programs

J. Knerr
Nov 2023
"""

import glob
from workout import *
import smtplib
from email.message import EmailMessage

VPATH="/home/knerr/repos/workout-bingo/"

def readVars():
    """read site variables from file"""
    variables = {}
    try:
        inf = open(VPATH + ".variables", "r")
        for line in inf:
            if not line.startswith("#"):
                data = line.strip().split("=")
                key = data[0].strip()
                value = data[1].strip()
                variables[key] = value
        inf.close()
    except FileNotFoundError:
        print("Need to create .variables file...")
        return None
    return variables

def checkwinner(e, g):
    """check if game over/someone has won"""
    # read in e's card.txt file
    cardfile = "./games/%d/%s/card.txt" % (int(g), e)
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


def readState(cardfile):
    """given a card.txt filename, read in state of card"""
    workouts = []
    inf = open(cardfile, "r")
    for line in inf:
        if not line.startswith("#"):
            i, j, w, d = line.strip().split(",")
            w = Workout(int(i), int(j), w, int(d))
            workouts.append(w)
    inf.close()
    return workouts


def readDone(e, g):
    """read in current player (e) done file for game g"""
    try:
        path = "games/%s/%s/.done" % (g, e)
        inf = open(path, "r")
        d = inf.readline().strip()
        inf.close()
        return d == "1"
    except FileNotFoundError:
        return True


def readCurrentWorkout():
    """read in current workout number"""
    try:
        inf = open(".current_workout", "r")
        w = str(inf.readline().strip())
        inf.close()
        return int(w)
    except FileNotFoundError:
        return None


def readCurrentGame():
    """read in current game number, return integer if exists"""
    try:
        inf = open(".current_game", "r")
        g = inf.readline().strip()
        inf.close()
        return int(g)
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


def emailgameover(e, g):
    """email all that game is over"""
    imgfile = "./games/%d/%s/card.png" % (int(g), e)
    variables = readVars()
    START = variables["START"]
    EMAILFROM = variables["EMAILFROM"]
    SERVER = variables["SERVER"]
    url = "%s/games/%s/%s/card.png\n" % (START, g, e)
    index = "%s/games/%s\n" % (START, g)
    emails = readEmails()
    lines = """
  We have a winner!!!!
  >>>> %s <<<<

  winning card: %s

  All cards: %s

  Another game starting soon...  :)

    """ % (e, url, index)

    EMAILTO = ",".join(emails)
    msg = EmailMessage()
    msg.set_content(lines)
    msg['Subject'] = "B I N G O Winner! (game: %d)" % (int(g))
    msg['From'] = EMAILFROM
    msg['To'] = EMAILTO
    msg['Reply-To'] = EMAILFROM
    s = smtplib.SMTP(SERVER)
    s.send_message(msg)
    s.quit()


def main():
    """some test code"""
    w = readCurrentWorkout()
    print(w)
    g = readCurrentGame()
    print(g)
    emails = readEmails()
    print(emails)
    done = readDone(emails[0], g)
    print(done)
    workouts = readWorkouts()
    print(workouts[0])
    quotes = readQuotes()
    print(quotes[0])
    gameover = checkwinner(emails[0], g)
    print(gameover)
#   if gameover:
#       emailgameover(emails[0], g)
    result = readVars()
    print(result)


if __name__ == "__main__":
    main()
