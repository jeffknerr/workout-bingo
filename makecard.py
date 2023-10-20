"""
try making a bingo card with workout data from statefile,
using matplotlib...

J. Knerr
Fall 2023
"""

from graphics import *
import glob
from random import randrange
import matplotlib.pyplot as plt
import numpy as np

def main():
    w = 1000
    h = 1000

    # Some example data to display
    x = np.linspace(0, 2 * np.pi, 400)
    y = np.sin(x ** 2)

    fig = plt.figure()
    gs = fig.add_gridspec(5, 5, hspace=0, wspace=0)
    axs = gs.subplots(sharex=True, sharey=True)
#   axs[0, 0].plot(x, y ** 2)
#   axs[1, 3].plot(x, 0.3 * y, 'o')
#   axs[2, 1].plot(x, y, '+')
    plt.tick_params(
        axis='both',       # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        left=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False) # labels along the bottom edge are off
    plt.show()


def drawLines(gw):
    """draw the box lines"""
    W = 3
    for i in range(6):
        p1 = Point(i, 0)
        p2 = Point(i, 5)
        l = Line(p1, p2)
        l.setWidth(W)
        l.draw(gw)
    for j in range(6):
        p1 = Point(0, j)
        p2 = Point(5, j)
        l = Line(p1, p2)
        l.setWidth(W)
        l.draw(gw)

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
