import board
import neopixel

from ledPixels import *

ledPix = ledPixels(20, board.D18)

ledPix.pixels[3] = (255, 0, 0)
ledPix.pixels.show()
