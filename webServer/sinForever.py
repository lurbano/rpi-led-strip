import time
import numpy as np
import argparse

from ledPixels import *

#nPix = 24
#speed = 4

# get number of pixels from the command line
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--freq", default=1, type=float, help = "Frequency")
parser.add_argument("-p", "--phase", default=0, type=float, help = "Phase")
parser.add_argument("-c", "--color", default="0,20,0", type=str, help = "Color: 3 values, comma separated. E.g.: 20,0,0")
parser.add_argument("-o", "--offset", default=0, type=float, help = "Offset: Scales result somewhat. Best from 0 and 1")
parser.add_argument("-s", "--speed", default=0.01, type=float, help = "Speed: 0.01 works reasonably well.")
parser.add_argument("-n", "--ncycles", default=1, type=float, help = "Number of cycles for animation.")
parser.add_argument("-x", "--nPix", default=20, type=int, help = "Number of LED Pixels.")
parser.add_argument("-t", "--timestep", default=0.01, type=float, help = "dt: delay between LED updates.")
parser.add_argument("-r", "--rainbow", default=False, type=bool, help = "Rainbow overlay.")


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
print("timestep:", args.timestep)

try:
    ncycles = args.ncycles
except:
    ncycles = 10
try:
    speed = args.speed
except:
    speed = 0.1

ledPix = ledPixels(args.nPix, board.D18)
phase = 0.0

sins = []
sins.append(sinFunc(args.freq, args.phase, args.offset, color, args.speed))
sins.append(sinFunc(args.freq, args.phase, args.offset, (0,0,50), 1.25*args.speed))
sins.append(sinFunc(args.freq, args.phase, args.offset, (50,0,0), 1.5*args.speed))

if args.rainbow:
    ledPix.rainbow()

direction = 1.0

while True:
    for i in np.arange(0, 2*np.pi/abs(speed), speed):
        ledPix.resetPix()
        for s in sins:
            s.currentPhase += s.speed * direction
            ledPix.sin(s.freq, s.currentPhase, s.color, s.offset)
        ledPix.pixels.show()
        time.sleep(0.01)

    direction *= -1.0
