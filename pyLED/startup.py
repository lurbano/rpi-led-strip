import board
import neopixel

nPix = 3

# get number of pixels from the command line
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--nPix", help = "Number of pixels")
args = parser.parse_args()
if args.nPix:
	try:
		nPix = int(args.nPix)
	except:
		print("using default (20) pixels: -nPix 20")
# end command line arguements

# set up pixels
pixels = neopixel.NeoPixel(board.D18, 20)

pixels[0] = (0,255,0)
