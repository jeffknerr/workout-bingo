"""
utils.py
put stuff in here used by other programs

J. Knerr
Nov 2023
"""

import glob


def readDone(e, g):
    """read in current player (e) done file for game g"""
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


if __name__ == "__main__":
    main()
