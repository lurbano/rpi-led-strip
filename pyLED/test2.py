import board
import neopixel

nPix = 20

pixels = neopixel.NeoPixel(board.D18, npix)

for i in range(0, nPix,2):
	pixels[i] = (0, 0, 255-(i*100/nPix))
