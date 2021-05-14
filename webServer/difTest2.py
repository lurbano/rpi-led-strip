import board
import neopixel
import time
#import numpy as np
#import matplotlib.pyplot as plt


from ledPixels import *

nPix = 20

ledPix = ledPixels(nPix, board.D18)

# ledPix.pixels[5] = (0, 255, 0)
# ledPix.pixels[10] = (255, 0, 0)
# ledPix.pixels[15] = (0, 0, 255)
# ledPix.pixels.show()
#
# ledPix.diffuse(k=0.1, nsteps=100)

for i in range(nPix):
    ledPix.clear()
    ledPix.pixels[i] = (0,255,0)
    ledPix.diffuse(nsteps=10)
    time.sleep(0.1)
