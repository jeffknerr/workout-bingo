"""
mark a bingo card, at a specific spot (to fix errors, or 
mark the FREE spot)

J. Knerr
Fall 2023
"""

from random import choice
import click
import os
from workout import *
from subprocess import getstatusoutput as gso
from utils import *


@click.command()
@click.option("--imgfile", required=True, help="bingo card image file")
@click.option("--i", required=True, help="column to mark")
@click.option("--j", required=True, help="row to mark")
def main(imgfile, i, j):
        magick(i, j, imgfile)


def magick(i, j, imgfile):
    """mark the png file at the given location"""
    xoffset = 125+45
    yoffset = 120+110
    boxsize = 155
    x = xoffset + boxsize*int(i)
    y = yoffset + boxsize*int(j)
    innercom = "text %d,%d 'X'" % (x, y)
    f1 = imgfile
    f2 = "output.png"
    com = 'convert -font helvetica -fill blue -pointsize 100 -draw "%s" %s %s' % (innercom, f1, f2) 
    status, output = gso(com)
    if status == 0:
        os.rename(f2, f1)


main()
