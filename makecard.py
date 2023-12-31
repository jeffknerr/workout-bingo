"""
try making a bingo card with workout data from statefile,
using matplotlib...

reads card.txt,
outputs card.png

J. Knerr
Fall 2023
"""

import glob
import click
import matplotlib.pyplot as plt
from utils import *


@click.command()
@click.option("--path", default="./", help="directory of card.txt file")
def main(path):
    if not path.endswith("/"):
        path += "/"
    wrkts = readFile(path + "card.txt")
    fig = plt.figure()
    fig.set_size_inches(10, 10)
    gs = fig.add_gridspec(5, 5, hspace=0, wspace=0)
    axs = gs.subplots(sharex=True, sharey=True)
    fig.suptitle('B I N G O  Card')
# https://stackoverflow.com/questions/25124143/get-rid-of-tick-labels-for-all-subplots
    for ax in axs.flat:
        ax.set_xticks([])
        ax.set_yticks([])
    # add workouts to figure subplots
    axs = axs.flat
    for n, ax in enumerate(axs):
        print(n)
        print(wrkts[n])
        if wrkts[n] == "FREE":
            x = 0.35
            y = 0.45
            textsize = 12
        else:
            x = 0.15
            y = 0.35
            textsize = 8
        ax.text(x, y, wrkts[n], size=textsize)
#   plt.show()
    plt.savefig(path + "card.png")
    # also put X on FREE spot??


def readFile(cardfile):
    """read in the card statefile, return the card workouts"""
    possible_wkts = readWorkouts()
    wkts = []
    inf = open(cardfile, "r")
    for line in inf:
        if not line.startswith("#"):
            i, j, w, d = line.strip().split(",")
            if w != "FREE":
                w = int(w)
                wstr = "W%d:\n" % w
                wstr += "".join(possible_wkts[w-1])
                wkts.append(wstr)
            else:
                wkts.append("FREE")
    inf.close()
    return wkts



main()
