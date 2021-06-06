import time
import numpy as np
import argparse

from ledPixels import *

nPix = 43

ledPix = ledPixels(nPix, board.D18)
phase = 0.0
#for phase in np.arange(0, 2*np.pi, 0.01):
ledPix.sin(args.freq,args.phase,color, args.offset)
ledPix.pixels.show()
