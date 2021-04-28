import board
import neopixel
import time

nPix = 20
pixels = neopixel.NeoPixel(board.D18, nPix)


class ledStopwatch:

	def __init__(self, startTime):
		self.t = startTime

	def run(self):
		for i in range(self.t, -1, -1):
			s = self.decimalToBinary(i)
			self.lightString(s)
			time.sleep(1)
			self.turnOff()

	def decimalToBinary(self, decimalNumber):
		binaryString = ""
		while decimalNumber >= 1:
			binaryString += str(decimalNumber % 2)
			decimalNumber = decimalNumber // 2
		binaryString = binaryString[::-1]
		return binaryString

	def lightString(self, s):
		for i in range(len(s)):
			if s[i] == "1":
				pixels[i] = (0,200,200)
				
	def turnOff(self):
		for i in range(n):
			pixels[i] = (0,0,0)


binTimer = ledStopwatch(10)
binTimer.run()
