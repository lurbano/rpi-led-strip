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
# parser.add_argument("-c", "--color", default="0,20,0", type=str, help = "Color: 3 values, comma separated. E.g.: 20,0,0")
# parser.add_argument("-o", "--offset", default=0, type=float, help = "Offset: Scales result somewhat. Best from 0 and 1")
# parser.add_argument("-s", "--speed", default=0.005, type=float, help = "Speed: 0.01 works reasonably well.")
# parser.add_argument("-n", "--ncycles", default=10, type=float, help = "Number of cycles for animation.")
parser.add_argument("-r", "--hour", default=True, action='store_false', help = "Do NOT Show Hour")
parser.add_argument("-m", "--min", default=True, action='store_false', help = "Do NOT Show Minutes")
parser.add_argument("-s", "--sec", default=True, action='store_false', help = "Do NOT Show Seconds")
parser.add_argument("-n", "--nPix", default=20, type=int, help = "Number of LED Pixels.")
parser.add_argument("-b", "--brightness", default=0.75, type=float, help = "Brightness.")
parser.add_argument("-d", "--stdev", default=1.0, type=float, help = "Standard Deviation.")


args = parser.parse_args()

nPix = args.nPix
# color = args.color
# color = color.strip()
# color = color.replace(" ","")
# color = color.split(",")
# r = float(color[0])
# g = float(color[1])
# b = float(color[2])
# color = (r, g, b)

# print("nPix:", args.nPix)
# print('brightness:', args.brightness)
print(args)

mCol = (0, 50, 0)
sCol = (0, 0, 50)
hCol = (50, 0, 0)


ledPix = ledPixels(args.nPix, board.D18)

ledPix.brightness = args.brightness

print(time.localtime())

while True:
    t = time.localtime()
    hPix = int((t.tm_hour / 24.) * nPix)
    mPix = int((t.tm_min / 60.) * nPix)
    sPix = int((t.tm_sec / 60.) * nPix)

    #print(f"hour:{t.tm_hour}; hPix")

    #print(f'hLights:{hLights}; mLights:{mLights}; sLights:{sLights}')

    ledPix.reset()

    if (args.hour):
        for i in range(hPix):
            ledPix.pixels[i] = hCol
    if (args.min):
        ledPix.superimpose(mPix, mCol)
    if (args.sec):
        ledPix.superimpose(sPix, sCol)
        # sPix = t.tm_sec * nPix / 60.0
        # ledPix.normalDistribution(n=sPix, col=sCol, sig=args.stdev)

    ledPix.pixels.show()
    time.sleep(0.1)


# ledPix.threeSins(freq=args.freq, speed=args.speed, dt=args.timestep, ncycles=args.ncycles)
