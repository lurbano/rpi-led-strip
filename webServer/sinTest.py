import time
import numpy as np

from ledPixels import *

nPix = 24
speed = 4

ledPix = ledPixels(nPix, board.D18)

for i in range(nPix):
    r = np.sin(np.pi*i/nPix)
    ledPix.pixels[i] = (255*r,0,0)
ledPix.pixels.show()

# for i in range(nPix*speed):
#     ledPix.resetPix()
#     ledPix.normalDistribution(n=float(i)/speed, sig=2, col=(255, 0,0))
#     ledPix.normalDistribution(n=nPix-float(i)/speed, sig=2, col=(0, 255,0))
#     ledPix.pixels.show()
#     time.sleep(0.1/speed)
