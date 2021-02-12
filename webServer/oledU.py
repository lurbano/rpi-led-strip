import time
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

class oledU:

    def __init__(self, width=128, height=32):

        # Create the I2C interface.
        self.i2c = busio.I2C(SCL, SDA)

        self.width = width
        self.height = height

        self.line_height = 8

        # Create the SSD1306 OLED class.
        # The first two parameters are the pixel width and pixel height.  Change these
        # to the right size for your display!
        self.disp = adafruit_ssd1306.SSD1306_I2C(self.width, self.height, self.i2c)

        # Clear display.
        self.disp.fill(0)
        self.disp.show()

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        self.image = Image.new('1', (self.width, self.height))

        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)

        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

        # Draw some shapes.
        # First define some constants to allow easy resizing of shapes.
        self.padding = -2
        self.top = self.padding
        self.bottom = self.height-self.padding
        # Move left to right keeping track of the current x position for drawing shapes.
        self.x = 0

        # Load default font.
        self.font = ImageFont.load_default()

    def clear(self):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

    def clear_line(self, line=1):
        y = (line-1)*self.line_height
        self.draw.rectangle((0, self.line_top(line), self.width, self.line_height), outline=0, fill=0)

    def write(self, text, line=1):
        self.clear_line(line)
        y = (line-1)*self.line_height
        self.draw.text((self.x, self.line_top(line)), text, font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.show()

    async def async_write(self, text, line=1):
        self.clear_line(line)
        y = (line-1)*self.line_height
        self.draw.text((self.x, self.line_top(line)), text, font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.show()

    def line_top(self, line):
        ltop = self.top
        if line == 1:
            ltop += 0
        elif line == 2:
            ltop += 12
        elif line == 3:
            ltop += 22
        return ltop
