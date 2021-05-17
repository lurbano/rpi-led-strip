import time
import numpy as np

from ledPixels import *

nPix = 43
speed = 4

ledPix = ledPixels(nPix, board.D18)
phase = 0.0
#for phase in np.arange(0, 2*np.pi, 0.01):
ledPix.sinFunc(1,phase,(0,0,20), 0)
ledPix.pixels.show()
time.sleep(0.01)
