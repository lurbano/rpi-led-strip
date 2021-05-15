import time

from ledPixels import *

nPix = 43

ledPix = ledPixels(nPix, board.D18)

for i in range(nPix*2):
    ledPix.normalDistribution(n=float(i)/2.0, sig=2)
    time.sleep(0.1)
