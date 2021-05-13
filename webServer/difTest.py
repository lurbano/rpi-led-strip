import board
import neopixel
import time

from ledPixels import *

ledPix = ledPixels(20, board.D18)

ledPix.pixels[3] = (255, 0, 0)
ledPix.pixels.show()

for i in range(100):
    ledPix.diffuse()
    time.sleep(0.1)
