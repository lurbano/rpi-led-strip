import board
import neopixel

npix = 20

pixels = neopixel.NeoPixel(board.D18, npix)

pixels[2] = (10,0,0)

for i in range(0, npix,2):
	pixels[i] = (i*100/npix, 0, 255-(i*100/npix))
