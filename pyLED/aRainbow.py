import board
import neopixel
import time
import asyncio

npix = 43
mag = 0.5  # brightness

pixels = neopixel.NeoPixel(board.D18, npix, auto_write=False)

async def rainbow_cycle(wait):
    for j in range(255):
        for i in range(npix):
            pixel_index = (i * 256 // npix) + j
            pixels[i] = wheel(pixel_index & 255, 0.5)
        pixels.show()
        await asyncio.sleep(wait)

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

async def infiniteRainbow():
    while 1:
        await rainbow_cycle(.001)

async def stopper(task):
    val = input("Press 'x' to stop:" )
    await asyncio.sleep(0.1)
    if (val == 'x'):
        task.cancel()


async def mainRainbow():
    task = asyncio.create_task(infiniteRainbow())
    #await asyncio.sleep(1)

    await stopper(task)


asyncio.run(mainRainbow())
