import time
import numpy as np
import argparse

from ledPixels import *

#nPix = 24
#speed = 4

# get number of pixels from the command line
parser = argparse.ArgumentParser()
# parser.add_argument("-f", "--freq", default=1, type=float, help = "Frequency")
# parser.add_argument("-p", "--phase", default=0, type=float, help = "Phase")
parser.add_argument("-c", "--color", default="0,100,0", type=str, help = "Color: 3 values, comma separated. E.g.: 20,0,0")
parser.add_argument("-n", "--nPix", default=20, type=int, help = "Number of LED Pixels.")
parser.add_argument("-b", "--brightness", default=0.75, type=float, help = "Brightness.")


args = parser.parse_args()

nPix = args.nPix
color = strToCol(args.color)

# print("nPix:", args.nPix)
# print('brightness:', args.brightness)
print(args)


ledPix = ledPixels(args.nPix, board.D18)

ledPix.brightness = args.brightness

ledPix.clear()
ledPix.normalDistribution(20)
ledPix.show()
