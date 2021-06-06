import time
import numpy as np
import argparse

from ledPixels import *

nPix = 20
speed = 0.1
ncycles = 4

freq = 3
phase = 0.0
offset = 0.0
color = (100,0,0)

ledPix = ledPixels(nPix, board.D18)


for i in np.arange(0, ncycles* 2*np.pi, 0.1):
    ledPix.resetPix()
    ledPix.sin(freq, phase+(i*speed), color, offset)

    ledPix.pixels.show()
    time.sleep(0.01)
