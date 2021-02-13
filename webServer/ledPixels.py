import neopixel
import board
import time

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


class ledPixels:
    def __init__(self, nPix, ledPin):
        self.nPix = nPix
        self.ledPin = ledPin
        self.pixels = neopixel.NeoPixel(board.D18, nPix, auto_write=False)
        self.interrupt = False
        self.brightness = 1.0 # from 0 to 1
        self.oldColors = []
        for i in range(nPix):
            self.oldColors.append((0,0,0))

    def setOldColors(self, col=None):
        if col == None:
            for i in range(nPix):
                self.oldColors[i] = self.pixels[i]
        else:
            for i in range(nPix):
                self.oldColors[i] = col

    def clear(self):
        for i in range(self.nPix):
            self.pixels[i] = (0,0,0)
        self.pixels.show()
        self.setOldColors()

    def rainbow(self, n=1, speed=0.01):
        for i in range(n):
            self.rainbow_cycle(speed)
        self.setOldColors()

    def setColor(self, col):
        if col[0] == "#":
            col = hex_to_rgb(col)
        print("setting color to:", col)
        self.brightness = 1.0
        for i in range(self.nPix):
            self.pixels[i] = col
        self.pixels.show()
        self.setOldColors()

    def setBrightness(self, brightness):
        self.brightness = float(brightness) / 100.0
        b = self.brightness
        print(f'brightness: {self.brightness}')
        for i in range(self.nPix):
            c = self.oldColors[i]
            col = (c[0]*b, c[1]*b, c[2]*b)
            self.pixels[i] = col
        self.pixels.show()

    def blue(self):
        for i in range(self.nPix):
            self.pixels[i] = (0,0,int(255*self.brightness))
            self.pixels.show()
        self.setOldColors((0,0,255))

    #UTILITY METHODS
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
        mag = self.brightness
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
