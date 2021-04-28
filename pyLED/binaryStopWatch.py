import board
import neopixel
import time

nPix = 20
pixels = neopixel.NeoPixel(board.D18, nPix)


class ledStopwatch:

	def __init__(self, nPix):
		self.nPix = nPix

	def run(self, startTime):
		self.t = startTime
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
		print(s)
		for i in range(len(s)):
			if s[i] == "1":
				pixels[i] = (0,200,0)
			else:
				pixels[i] = (100,0,0)

	def turnOff(self):
		for i in range(nPix):
			pixels[i] = (0,0,0)


binTimer = ledStopwatch(20)
binTimer.run(20)
# s = ""
# while s != "q":
# 	s = input("Enter binary Sequence:")
# 	binTimer.lightString(s)
