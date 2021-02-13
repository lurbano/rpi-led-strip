#! /usr/bin/python
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
#from numpy import arange, mean
import numpy as np

#from ledController import *
from ledPixels import *
#from oledU import *

nPix = 43
ledPin = board.D18


#Initialize neopixels
ledPix = ledPixels(nPix, ledPin)

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

			if msg["what"] == "clearButton":
				print("Clearing LEDs ")
				ledPix.clear()
				self.write_message({"info":"cleared"})

			if msg["what"] == "rainbowButton":
				print("rainbow LEDs ")
				try:
					n = int(msg["ct"])
					s = float(msg["speed"])
					ledPix.rainbow(n, s)
				except:
					ledPix.rainbow()

			if msg["what"] == "setColor":
				col = msg["color"]
				ledPix.setColor(col)

			if msg["what"] == "restart":
				ledPix.clear()
				subprocess.Popen('sleep 5 ; sudo python3 '+os.path.join(os.path.dirname(__file__), "server.py"), shell=True)
				main_loop.stop()

			if msg["what"] == "blueButton":
				print("blue LEDs ")
				ledPix.blue()


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
		ledPix.pixels[-1] = (0, 100, 0)
		ledPix.pixels[-2] = (0, 0, 100)
		ledPix.pixels.show()

		# get ip address
		cmd = "hostname -I | cut -d\' \' -f1"
		IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
		print('IP: '+ IP +":" + PORT)
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
