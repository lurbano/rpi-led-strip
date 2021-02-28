#! /usr/bin/python3

# From: https://www.hackster.io/dataplicity/control-raspberry-pi-gpios-with-websockets-af3d0c

import os.path
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import tornado.gen
import RPi.GPIO as GPIO
import time
import subprocess
import json
import sys
import argparse
import asyncio
#from numpy import arange, mean
import numpy as np
#from oledU import *


# LED STRIP (1/3)

from ledPixels import *

nPix = 20
ledPin = board.D18

# get number of pixels from the command line
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--nPix", help = "Number of pixels")
args = parser.parse_args()

if args.nPix:
	try:
		nPix = int(args.nPix)
	except:
		print("using default (20) pixels: -nPix 20")


#Initialize neopixels
ledPix = ledPixels(nPix, ledPin)
# def initPixels(nPix, ledPin = board.D18):
# 	ledPix = ledPixels(nPix, ledPin)
# 	return ledPix
#
# ledPix = initPixels(nPix, ledPin)

# LED STRIP (END)


#oled = oledU(128,32)

#Tornado Folder Paths
settings = dict(
	template_path = os.path.join(os.path.dirname(__file__), "templates"),
	static_path = os.path.join(os.path.dirname(__file__), "static")
	)

#pyPath = '/home/pi/rpi-led-strip/pyLED/'

#Tonado server port
PORT = 8040

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		print ("[HTTP](MainHandler) User Connected.")
		self.render("index.html")


class WSHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		print ('[WS] Connection was opened.')
		self.write_message('{"who": "server", "info": "on"}')
		#self.oled = oledU(128,32)


	async def on_message(self, message):
		print ('[WS] Incoming on_message:', message)
		try:
			msg = json.loads(message)
			if msg["what"] == "server":
				if msg["opts"] == "off":
					sys.exit("Stopping server")

			# LED STRIP (2/3)

			if msg["what"] == "nPix":
				print("Reset Number of Pixels")
				ledPix.cancelTask()
				print("a")
				n = int(msg["n"])
				print('b')
				ledPix = ledPixels(n, ledPin)
				ledPix.initCodeColor()

			if msg["what"] == "clearButton":
				print("Clearing LEDs ")
				ledPix.cancelTask()
				ledPix.clear()
				self.write_message({"info":"cleared"})

			if msg["what"] == "rainbowButton":
				print("rainbow LEDs ")
				ledPix.cancelTask()
				n = int(msg["ct"])
				s = float(msg["speed"])
				task = asyncio.create_task(ledPix.aRainbow(n, s))
				ledPix.task = task

			if msg["what"] == "rainbowForever":
				print("rainbow LEDs (forever) infinite loop")
				ledPix.cancelTask()
				s = float(msg["speed"])
				task = asyncio.create_task(ledPix.aRainbowForever(s))
				ledPix.task = task

			if msg["what"] == "setColor":
				ledPix.cancelTask()
				col = msg["color"]
				ledPix.setColor(col)

			if msg["what"] == "setBrightness":
				bright = msg["brightness"]
				ledPix.setBrightness(bright)

			if msg["what"] == "interruptButton":
				ledPix.cancelTask()

			if msg["what"] == "blueButton":
				print("blue LEDs ")
				ledPix.cancelTask()
				ledPix.blue()

			# LED STRIP (END)

			# TIMER
			if msg["what"] == "timer":
				ledPix.cancelTask()
				m = float(msg["minutes"])
				s = float(msg["seconds"])
				task = asyncio.create_task(ledPix.aTimer(self, m, s))
				ledPix.task = task
			# TIMER (END)

			if msg["what"] == "restart":
				ledPix.clear()
				subprocess.Popen('sleep 5 ; sudo python3 '+os.path.join(os.path.dirname(__file__), "server.py" + f' -n {nPix}'), shell=True)
				main_loop.stop()

			if msg["what"] == "reboot":
				ledPix.clear()
				subprocess.Popen('sleep 5 ; sudo reboot', shell=True)
				main_loop.stop()



		except Exception as e:
			print(e)
			print("Exception: Error with data recieved by server")
			print(message)


	def on_close(self):
		print ('[WS] Connection was closed.')


async def measure():
	print("measuring")



application = tornado.web.Application([
  (r'/', MainHandler),
  (r'/ws', WSHandler),
  ], **settings)


if __name__ == "__main__":
	try:
		http_server = tornado.httpserver.HTTPServer(application)
		http_server.listen(PORT)
		print("hello")
		main_loop = tornado.ioloop.IOLoop.instance()

		print ("Tornado Server started")

		# LED STRIP (3/3)

		ledPix.initCodeColor()
		# ledPix.pixels[-1] = (0, 100, 0)
		# ledPix.pixels[-2] = (0, 0, 100)
		# ledPix.pixels.show()

		# LED STRIP (END)

		# get ip address
		cmd = "hostname -I | cut -d\' \' -f1"
		IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
		print('IP: '+ IP +":" + str(PORT))
		#oled.write('IP: '+ IP, 3)
		cmd = 'iwgetid | sed \'s/.*://\' | sed \'s/"//g\''
		wifi = subprocess.check_output(cmd, shell=True).decode("utf-8")
		#oled.write(wifi, 2)
		print(wifi)

		main_loop.start()




	except:
		print ("Exception triggered - Tornado Server stopped.")
		ledPixels.clear()

#End of Program
