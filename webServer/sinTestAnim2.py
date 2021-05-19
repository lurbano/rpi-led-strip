import time
import numpy as np
import argparse

from ledPixels import *

# nPix = 24
# speed = 4

# get number of pixels from the command line
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--freq", default=1, type=float, help = "Frequency")
parser.add_argument("-p", "--phase", default=0, type=float, help = "Phase")
parser.add_argument("-c", "--color", default="0,20,0", type=str, help = "Color: 3 values, comma separated. E.g.: 20,0,0")
parser.add_argument("-o", "--offset", default=0, type=float, help = "Offset: Scales result somewhat. Best from 0 and 1")
parser.add_argument("-s", "--speed", default=0.1, type=float, help = "Speed: 0.1 works reasonably well.")
parser.add_argument("-n", "--ncycles", default=1, type=float, help = "Number of cycles for animation.")
parser.add_argument("-x", "--nPix", default=20, type=int, help = "Number of LED Pixels.")

args = parser.parse_args()

color = args.color
color = color.strip()
color = color.replace(" ","")
color = color.split(",")
r = float(color[0])
g = float(color[1])
b = float(color[2])
color = (r, g, b)
print("freq:", args.freq)
print("phase:", args.phase)
print("color:", color)
print("offset:", args.offset)
print("speed:", args.speed)
print("ncycles:", args.ncycles)

ledPix = ledPixels(args.nPix, board.D18)
phase = 0.0

for i in np.arange(0, args.ncycles* 2*np.pi, 0.1):
    ledPix.resetPix()
    ledPix.sin(args.freq, args.phase+(i*args.speed), color, args.offset)
    ledPix.sin(args.freq, args.phase-(i*args.speed), (0,0,100), args.offset)
    ledPix.pixels.show()
    time.sleep(0.01)
