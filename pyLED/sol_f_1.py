import board
import neopixel
import time

nPix = 20
pixels = neopixel.NeoPixel(board.D18, nPix)

def turnOff(n):
	for i in range(n):
		pixels[i] = (0,0,0)

def turnOn(n):
	for i in range(n):
		pixels[i] = (0,200,0)

turnOn(5)
time.sleep(2)
turnOn(10)
time.sleep(2)
turnOn(15)
time.sleep(2)
turnOff(15)
turnOn(3)
