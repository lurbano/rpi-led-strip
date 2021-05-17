import time
import numpy as np

from ledPixels import *

nPix = 24
speed = 4

ledPix = ledPixels(nPix, board.D18)
phase = 0.0
#for phase in np.arange(0, 2*np.pi, 0.01):
ledPix.sinFunc(2,phase,(0,0,10), 1)
ledPix.pixels.show()
time.sleep(0.01)
