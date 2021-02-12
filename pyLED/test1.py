import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 20)

pixels[2] = (10,0,0)
