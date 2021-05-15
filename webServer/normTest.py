import time

from ledPixels import *

nPix = 43

ledPix = ledPixels(nPix, board.D18)

for i in range(nPix):
    ledPix.normalDistribution(n=i, sig=2)
    time.sleep(0.1)
