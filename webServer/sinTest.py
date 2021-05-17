import time
import numpy as np

from ledPixels import *

nPix = 24
speed = 4

ledPix = ledPixels(nPix, board.D18)

for phase in np.arange(0, 2*pi, 0.1):
    ledPix.sinFunc(2,phase,(0,0,255))
    ledPix.pixels.show()
    time.sleep(0.1)
