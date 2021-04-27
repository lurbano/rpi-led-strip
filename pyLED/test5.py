import board
import neopixel
import time

nPix = 20
pixels = neopixel.NeoPixel(board.D18, nPix)

def turnOff(n):
	for i in range(n):
		pixels[i] = (0,0,0)

for i in range(0, nPix, 2):
	pixels[i] = (0, 0, 255)

#time.sleep(2)
#turnOff(nPix)
