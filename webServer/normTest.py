import time

from ledPixels import *

nPix = 20

ledPix = ledPixels(nPix, board.D18)

ledPix.normalDistribution(n=10, sig=2)
