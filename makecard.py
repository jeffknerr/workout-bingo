"""
try making a bingo card with workout data from statefile,
using matplotlib...

J. Knerr
Fall 2023
"""

import glob
import matplotlib.pyplot as plt


def main():
    wrkts = readFile("card.txt")
    fig = plt.figure()
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
        ax.text(0.3, 0.45, wrkts[n], size=8)
#   plt.show()
    plt.savefig("card.png")


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
                wkts.append("".join(possible_wkts[w-1]))
            else:
                wkts.append("FREE")
    inf.close()
    return wkts


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
