import time

from ledPixels import *

nPix = 43
speed = 4

ledPix = ledPixels(nPix, board.D18)

for i in range(nPix*speed):
    ledPix.resetPix()
    ledPix.normalDistribution(n=float(i)/speed, sig=2, col=(255, 255,0))
    ledPix.pixels.show()
    time.sleep(0.1/speed)
