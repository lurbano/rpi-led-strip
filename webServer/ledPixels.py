# LED STRIP

import neopixel
import board
import time
import asyncio
import numpy as np

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def diffuse(T, k=0.1):
    n = len(T)
    Tnew = []
    for i in range(n):
        Tnew.append(0.0)

    Tnew[0] = T[0] + k * (T[1] - T[0])
    Tnew[n-1] = T[n-1] + k * (T[n-2] - T[n-1])
    for i in range(1, n-1):
        qin = -k * (T[i] - T[i-1])
        qout = k * (T[i+1] - T[i])
        Tnew[i] = T[i] + qin + qout
    return Tnew

def strToCol(str): #formatted like '255,0,255'
    color = str.strip()
    color = color.replace(" ","")
    color = color.split(",")
    r = float(color[0])
    g = float(color[1])
    b = float(color[2])
    color = (r, g, b)
    return color

class sinFunc:
    def __init__(self, freq=1.0, phase=0.0, offset=0.0, color=(100,0,0), speed=0.1):
        self.freq = freq
        self.phase = phase
        self.offset = offset
        self.color = color
        self.speed = speed
        self.currentPhase = phase


class ledPixels:
    def __init__(self, nPix, ledPin):
        #self.nPix = nPix
        self.ledPin = ledPin
        self.nPixSet(nPix)
        #self.pixels = neopixel.NeoPixel(board.D18, nPix, auto_write=False)
        self.interrupt = False
        self.brightness = 1.0 # from 0 to 1
        self.task = None


    def nPixSet(self, nPix):
        print("nPix ledPix:", nPix)
        self.nPix = nPix
        self.pixels = neopixel.NeoPixel(board.D18, nPix, auto_write=False)
        self.oldColors = []
        for i in range(nPix):
            self.oldColors.append((0,0,0))
        print("nPix Set")

    def initCodeColor(self):
        self.pixels[-1] = (0, 100, 0)
        self.pixels[-2] = (0, 0, 100)
        self.pixels.show()

    def light(self, n, col):
        self.pixels[n] = col
        self.pixels.show()

    def show(self):
        self.pixels.show()

    def superimpose(self, i, col):
        (r,g,b) = self.pixels[i]
        self.pixels[i] = (col[0]+r, col[1]+g, col[2]+b)


    def setOldColors(self, col=None):
        if col == None:
            for i in range(self.nPix):
                self.oldColors[i] = self.pixels[i]
        else:
            for i in range(self.nPix):
                self.oldColors[i] = col

    def setInterrupt(self):
        self.interrupt = True

    def clear(self):
        for i in range(self.nPix):
            self.pixels[i] = (0,0,0)
        self.pixels.show()
        self.setOldColors()

    def resetPix(self):
        for i in range(self.nPix):
            self.pixels[i] = (0,0,0)

    def reset(self):
        for i in range(self.nPix):
            self.pixels[i] = (0,0,0)

    def rainbow(self, n=1, speed=0.01):
        for i in range(n):
            if (self.interrupt):
                break
            self.rainbow_cycle(speed)
        self.setOldColors()

    async def aRainbow(self, n=1, speed=0.01):
        for i in range(n):
            print(f'start cycle {i}')
            await self.aRainbow_cycle(speed)
            print(f'end cycle {i}')
        print('done aRainbow')
        self.setOldColors()

    async def aRainbowForever(self, speed=0.01):
        while 1:
            await self.aRainbow_cycle(speed)

    async def aTimer(self, serv, m, s):
        timeLeft = int(m*60 + s)
        totTime = int(m*60 + s)
        print("Starting Timer: ", totTime)
        while timeLeft > 0:
            timeLeft -= 1
            nLights = int(self.nPix * timeLeft/totTime)
            self.twoColors(nLights, (0,255,0), (100,0,0))
            #print(timeLeft, nLights)
            m = timeLeft // 60
            s = timeLeft % 60
            serv.write_message({"info": "timer", "m":m, "s":s})
            await asyncio.sleep(1)
        print("Timer Done.")

    def twoColors(self, n, col1=(0,0,255), col2=(0,0,0)):
        for i in range(self.nPix):
            if i < n:
                self.pixels[i] = self.brighten(col1)
            else:
                self.pixels[i] = self.brighten(col2)
        self.pixels.show()

    def twoColorsTimestep(self, n, col1=(0,0,255), col2=(0,0,0), dt=0.1):
        for i in range(self.nPix):
            if i < n:
                self.pixels[i] = self.brighten(col1)
            else:
                self.pixels[i] = self.brighten(col2)
            time.sleep(0.1)
            self.pixels.show()

    def setColor(self, col):
        if col[0] == "#":
            col = hex_to_rgb(col)
        print("setting color to:", col)
        self.cancelTask()
        self.brightness = 1.0
        for i in range(self.nPix):
            self.pixels[i] = col
        self.pixels.show()
        self.setOldColors()

    def setBrightness(self, brightness):
        self.brightness = float(brightness) / 100.0
        b = self.brightness
        if self.task.done():
            print(f'brightness: {self.brightness}')
            print(self.oldColors[-1], self.pixels[-1])
            for i in range(self.nPix):
                c = self.oldColors[i]
                col = (int(c[0]*b), int(c[1]*b), int(c[2]*b))
                self.pixels[i] = col
            print(self.pixels[-1])
            self.pixels.show()

    def blue(self):
        for i in range(self.nPix):
            self.pixels[i] = (0,0,int(255*self.brightness))
        self.pixels.show()
        self.setOldColors((0,0,255))

    def scale(self, val):
        n = round(self.nPix * (val-self.scaleMin)/(self.scaleMax-self.scaleMin))

        if n < 0:
            n = 0
        if n > self.nPix:
            n = self.nPix

        for i in range(n):
            self.pixels[i] = self.scaleCol
        for i in range(n, self.nPix):
            self.pixels[i] = (0,0,0)
        self.pixels.show()
        self.setOldColors()

    def setupScale(self, minVal=0., maxVal=100., color=(0,100,0)):
        self.scaleMin = minVal
        self.scaleMax = maxVal
        self.scaleCol = color

    #UTILITY METHODS
    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.nPix):
                pixel_index = (i * 256 // self.nPix) + j
                self.pixels[i] = self.wheel(pixel_index & 255, 0.5)
            self.pixels.show()
            time.sleep(wait)

    async def aRainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.nPix):
                pixel_index = (i * 256 // self.nPix) + j
                self.pixels[i] = self.wheel(pixel_index & 255, 0.5)
            self.pixels.show()
            await asyncio.sleep(wait)


    def cancelTask(self):
        print("Canceling last task.")
        if self.task:
            self.task.cancel()

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

    def brighten(self, color):
        return (color[0]*self.brightness, color[1]*self.brightness, color[2]*self.brightness)

    def diffuse(self, k=0.1, nsteps=1, dt=0.0):
        # k is the diffusion coefficient
        #   higher coefficients mean faster diffusion
        # Uses explicit finite difference equation so
        #   instabilities may occur at high k values
        (r, g, b) = ([], [], [])
        (rSum, gSum, bSum) = (0,0,0)

        # initialize
        for i in range(self.nPix):
            r.append(self.pixels[i][0])
            g.append(self.pixels[i][1])
            b.append(self.pixels[i][2])
            rSum += r[-1]
            gSum += g[-1]
            bSum += b[-1]

        #print("sums:", rSum, gSum, bSum)

        for t in range(nsteps):
            r = diffuse(r, k=0.1)
            g = diffuse(g, k=0.1)
            b = diffuse(b, k=0.1)

            for i in range(self.nPix):
                self.pixels[i] = (r[i], g[i], b[i])

            self.pixels.show()
            time.sleep(dt)

    def normalDistribution(self, n, col=(255,0,0), sig=1.0):

        for i in range(self.nPix):
            #print(i, self.pixels[i])
            r_o = self.pixels[i][0]
            g_o = self.pixels[i][1]
            b_o = self.pixels[i][2]
            (r,g,b) = col

            d = (1/(sig*(2*np.pi)**0.5))*np.e**(-0.5*(np.abs(i-n)/sig)**2)

            r = min(r_o + d * r / 0.4, 255)
            g = min(g_o + d * g / 0.4, 255)
            b = min(b_o + d * b / 0.4, 255)
            self.pixels[i] = (r, g, b)
        #self.pixels.show()

    def sin(self, frequency, phase, col=(255,0,0), offset=0.0):
        if col[0] == "#":
            col = hex_to_rgb(col)
        for i in range(self.nPix):
            r_o = self.pixels[i][0]
            g_o = self.pixels[i][1]
            b_o = self.pixels[i][2]
            (r,g,b) = col

            f =  np.sin(frequency *((2*np.pi*i/self.nPix) - phase*np.pi)) + offset

            r = r_o + r * f
            r = min(max(0.0, r), 255) * self.brightness
            g = g_o + g * f
            g = min(max(0.0, g), 255) * self.brightness
            b = b_o + b * f
            b = min(max(0.0, b), 255) * self.brightness

            self.pixels[i] = (r, g, b)

    async def aSin(self, frequency, phase, col="#00ff00", offset=0.0, dt=0.0):
        if col[0] == "#":
            col = hex_to_rgb(col)
        print(f"making sin curve with: frequency = {frequency}, phase = {phase}, color = {col}, offset = {offset}, dt = {dt}")
        for i in range(self.nPix):
            r_o = self.pixels[i][0]
            g_o = self.pixels[i][1]
            b_o = self.pixels[i][2]
            (r,g,b) = col

            f =  np.sin(frequency *((2*np.pi*i/self.nPix) - phase*np.pi)) + offset

            r = r_o + r * f
            r = min(max(0.0, r), 255)
            g = g_o + g * f
            g = min(max(0.0, g), 255)
            b = b_o + b * f
            b = min(max(0.0, b), 255)

            self.pixels[i] = (r, g, b)
            self.pixels.show()
            await asyncio.sleep(dt)

    def threeSins(self, freq=1, speed = 0.002, dt=0.001, ncycles=10):
        sins = []
        sins.append(sinFunc(freq, 0, 0, (0,0,255), speed))
        sins.append(sinFunc(freq, 0, 0, (0,255,0), 1.2*speed))
        sins.append(sinFunc(freq, 0, 0, (255,0,0), 1.4*speed))
        direction = 1.0

        print(f'nsteps: {2*np.pi/dt}')
        ct = 0

        while True:
            for i in np.arange(0, ncycles*2*np.pi, dt):
                ct += 1
                self.resetPix()
                for s in sins:
                    s.currentPhase += s.speed * direction
                    self.sin(s.freq, s.currentPhase, s.color, s.offset)
                self.pixels.show()
                time.sleep(dt)
                # if (ct%100 == 0):
                #     print(i)

            direction *= -1.0
