import neopixel
import board
import time

class ledPixels:
    def __init__(self, nPix, ledPin):
        self.nPix = nPix
        self.ledPin = ledPin
        self.pixels = neopixel.NeoPixel(board.D18, nPix, auto_write=False)

    def clear(self):
        for i in range(self.nPix):
            self.pixels[i] = (0,0,0)
        self.pixels.show()

    def rainbow(self, n=1):
        for i in range(n):
            self.rainbow_cycle(0.01)

    def blue(self):
        for i in range(self.nPix):
            self.pixels[i] = (0,0,200)

    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.nPix):
                pixel_index = (i * 256 // self.nPix) + j
                self.pixels[i] = self.wheel(pixel_index & 255, 0.5)
            self.pixels.show()
            time.sleep(wait)

    def wheel(self, pos, mag=0.5):
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
