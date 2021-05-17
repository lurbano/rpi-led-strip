import time
import numpy as np
import argparse

from ledPixels import *

nPix = 43
speed = 4

# get number of pixels from the command line
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--freq", default=1, type=float, help = "Frequency")
parser.add_argument("-p", "--phase", default=0, type=float, help = "Phase")
parser.add_argument("-c", "--color", default="(0,20,0)", type=str, help = "Color")
parser.add_argument("-o", "--offset", default=0, type=float, help = "Offset")

args = parser.parse_args()

color = args.color
color = color.strip()
color = color.replace("(","").replace(")","")
color = color.replace(" ","")
color = color.split(",")
r = color[0]
g = color[1]
b = color[2]
color = (r, g, b)
print("freq:", args.freq)
print("phase:", args.phase)
print("color:", color)
print("offset:", args.offset)


ledPix = ledPixels(nPix, board.D18)
phase = 0.0
#for phase in np.arange(0, 2*np.pi, 0.01):
ledPix.sinFunc(args.freq,args.phase,color, args.offset)
ledPix.pixels.show()
time.sleep(0.01)
