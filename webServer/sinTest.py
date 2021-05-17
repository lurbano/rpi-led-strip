import time
import numpy as np

from ledPixels import *

nPix = 24
speed = 4

ledPix = ledPixels(nPix, board.D18)

for i in range(nPix):
    r = 100 * np.sin(2*((2*np.pi*i/nPix)+np.pi))
    g = 100 * np.sin((2*np.pi*i/nPix))
    r = max(r, 0.0)
    g = max(g, 0.0)
    print(r)
    ledPix.pixels[i] = (r,g, 0)
    print(ledPix.pixels[i])
ledPix.pixels.show()

# for i in range(nPix*speed):
#     ledPix.resetPix()
#     ledPix.normalDistribution(n=float(i)/speed, sig=2, col=(255, 0,0))
#     ledPix.normalDistribution(n=nPix-float(i)/speed, sig=2, col=(0, 255,0))
#     ledPix.pixels.show()
#     time.sleep(0.1/speed)
