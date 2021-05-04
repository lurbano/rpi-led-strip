import board
import neopixel
import argparse

nPix = 20

# get number of pixels from the command line
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--nPix", help = "Number of pixels")
args = parser.parse_args()

if args.nPix:
	try:
		nPix = int(args.nPix)
	except:
		print("using default (20) pixels: -nPix 20")


pixels = neopixel.NeoPixel(board.D18, 20)

for i in range(nPix):
    pixels[i] = (0,0,0)
