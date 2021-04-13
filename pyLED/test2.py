import board
import neopixel

nPix = 20

pixels = neopixel.NeoPixel(board.D18, nPix)

for i in range(0, nPix, 2):
	pixels[i] = (0, 0, 255)
