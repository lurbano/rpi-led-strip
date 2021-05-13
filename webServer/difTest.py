import board
import neopixel
import time
#import numpy as np
#import matplotlib.pyplot as plt


from ledPixels import *

nPix = 20
r = []
for i in range(nPix):
    r.append(0)

ledPix = ledPixels(nPix, board.D18)

ledPix.pixels[5] = (0, 255, 0)
ledPix.pixels[10] = (255, 0, 0)
ledPix.pixels[15] = (0, 0, 255)
ledPix.pixels.show()

# for i in range(10):
#     ledPix.diffuse(k=0.1)
#     for j in range(nPix):
#         r[j] = round(ledPix.pixels[j][0])
#     #print(i, r)
#     time.sleep(0.01)

ledPix.diffuse(k=0.1, nsteps=100)
