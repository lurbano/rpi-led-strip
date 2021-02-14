import board
import neopixel
import time

nPix = 20
mag = 0.5  # brightness

pixels = neopixel.NeoPixel(board.D18, nPix, auto_write=False)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(nPix):
            pixel_index = (i * 256 // nPix) + j
            pixels[i] = wheel(pixel_index & 255, 0.5)
        pixels.show()
        time.sleep(wait)

def wheel(pos, mag):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    (r, g, b) = (int(r*mag), int(g*mag), int(b*mag))
    return (r, g, b)

while 1:
    rainbow_cycle(.001)
