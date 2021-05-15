import time

from ledPixels import *

nPix = 43

ledPix = ledPixels(nPix, board.D18)

for i in range(nPix*3):
    ledPix.resetPix()
    ledPix.normalDistribution(n=float(i)/3.0, sig=2, col=(255, 255,0))
    ledPix.pixels.show()
    time.sleep(0.1)
