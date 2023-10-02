"""
try making a workout email for use with bingo cards

J. Knerr
Fall 2023
"""

import glob
from random import randrange
from datetime import datetime

def main():
    wkts = readWorkouts()
    today = datetime.today()
    print(today)
    skiday = datetime(year=2024, month=2, day=4, hour=8)
    countdown = skiday - today
    print("days until first ski run!!! ", countdown)
    print()
    n = randrange(len(wkts))
    print("today's workout (W%d):" % (n+1))
    print(wkts[n])
    print()
    quotes = readQuotes()
    print("today's quote:")
    qnum = randrange(len(quotes))
    print(quotes[qnum][0])
    print("\t\t--", quotes[qnum][1])

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

main()
