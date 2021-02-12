import neopixel

class ledPixels:
    def __init__(self, nPix, ledPin):
        self.nPix = nPix
        self.ledPin = ledPin
        self.pixels = neopixel.NeoPixel(board.D18, nPix, auto_write=False)

    def clear(self):
        for i in range(self.nPix):
            self.pixels[i] = (0,0,0)
        self.pixels.show()
