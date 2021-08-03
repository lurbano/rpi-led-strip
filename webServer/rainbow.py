import time
import numpy as np
import argparse

from ledPixels import *

#nPix = 24
#speed = 4

# get number of pixels from the command line
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--speed", default=0.005, type=float, help = "Speed: 0.01 works reasonably well.")
parser.add_argument("-n", "--nPix", default=20, type=int, help = "Number of LED Pixels.")
parser.add_argument("-t", "--timestep", default=0.01, type=float, help = "dt: delay between LED updates.")
parser.add_argument("-b", "--brightness", default=0.75, type=float, help = "Brightness.")
parser.add_argument("-c", "--nCycles", default=0, type=int, help = "number of cycles. Default = 0 = forever.")


args = parser.parse_args()

color = args.color
color = color.strip()
color = color.replace(" ","")
color = color.split(",")
r = float(color[0])
g = float(color[1])
b = float(color[2])
color = (r, g, b)
print("speed:", args.speed)
print("nPix:", args.nPix)
print("timestep:", args.timestep)
print('brightness:', args.brightness)

ledPix = ledPixels(args.nPix, board.D18)

ledPix.brightness = args.brightness
direction = 1.0

if args.nCycles == 0:
    while 1:
        ledPix.rainbow_cycle(args.timestep)
else:
    for i in range(args.nCycles):
        ledPix.rainbow_cycle(args.timestep)
