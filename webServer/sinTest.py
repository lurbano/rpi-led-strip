import time
import numpy as np

from ledPixels import *

nPix = 24
speed = 4

ledPix = ledPixels(nPix, board.D18)


ledPix.sinFunc(2,0,(0,0,255))
ledPix.pixels.show()
