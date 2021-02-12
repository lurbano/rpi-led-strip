#! /usr/bin/python
# From: https://www.hackster.io/dataplicity/control-raspberry-pi-gpios-with-websockets-af3d0c

import os.path
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import tornado.gen
import RPi.GPIO as GPIO
import board
import neopixel
import time
import subprocess
import json
import sys
#from numpy import arange, mean
import numpy as np

#from ledController import *
from ledPixels import *
#from oledU import *

nPix = 20
ledPin = board.D18


#Initialize neopixels
ledPix = ledPixels(nPix, ledPin)
#pixels = neopixel.NeoPixel(board.D18, nPix, auto_write=False)

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
				# for i in range(nPix):
				# 	pixels[i] = (0,0,0)
				# pixels.show()
				self.write_message{"info":"cleared"}

			if msg["what"] == "rainbow":
				print("Clearing LEDs ")
				for i in range(nPix):
					pixels[i] = (0,0,0)
				pixels.show()
				self.write_message{"info":"cleared"}


            # if msg["what"] == "dist":
            #   dSensor = uSonicDistance()
            #   if msg['opts'] == "check":
            #       # get measurement
            #       #d = dSensor.measure(returnType='json')
            #       data = dSensor.measure()
            #       #print(d)
            #       d = {
            #               "sensor" : 'HC-SRO4',
            #               "info" : msg['opts'],
            #               'measurement': 'distance',
            #               'units': "cm",
            #               "data": data,
            #               }
			#
            #       # send message back to client
            #       self.write_message(d)
			#
            #       # write measurement to the OLED
            #       oled.write(str(data) + " " + d["units"])
			#
            #   elif msg['opts'] == "check_multipulse":
            #       # get measurement
            #       #d = dSensor.measure(returnType='json')
            #       print("multipulsing")
            #       data = dSensor.multipulse()
			#
            #       d = {
            #               "sensor" : 'HC-SRO4',
            #               "info" : msg['opts'],
            #               'measurement': 'distance',
            #               'units': "cm",
            #               "data": data,
            #               }
			#
            #       # send message back to client
            #       self.write_message(d)
			#
            #       # write measurement to the OLED
            #       oled.write(str(data) + " " + d["units"])
			#
            #   elif msg['opts'] == 'log' or msg['opts'] == 'log_feed':
            #       print ('Logging')
            #       GPIO.output(measureLedPin, True)
			#
            #       #print ('[WS] Incoming message:', message)
            #       dt = float(msg['info']['dt'])
            #       tt = float(msg['info']['tt'])
            #       print (f"dt={dt}, t={tt}")
			#
            #       data = []
            #       t0 = time.time()
            #       for i in np.arange(0.0, tt+dt, dt):
            #           nxt = tornado.gen.sleep(dt)
            #           (t, d) = await dSensor.async_measure(returnType='tdt')
            #           t = t - t0
            #           #print(f"t={t},d={d}")
            #           #txt = "{:.3} sec | {:.3f}".format(i, d)
            #           #print(txt)
            #           #oled.write(txt)
            #           data.append([t,d])
            #           if (msg['opts'] == 'log_feed'):
            #               d_feed = {"sensor" : 'HC-SRO4',
            #                         "info": msg['opts'],
            #                         "t": t,
            #                         "d": d}
            #               #print(d_feed)
            #               self.write_message(d_feed)
            #           await nxt
			#
            #       GPIO.output(measureLedPin, False)
			#
            #       if (msg['opts'] == 'log'):
            #           d = {
            #                   "sensor" : 'HC-SRO4',
            #                   "info" : msg['opts'],
            #                   'measurement': 'distance',
            #                   'units': "cm",
            #                   "data": data,
            #                   }
			#
            #           # send message back to client
            #           self.write_message(d)
			#
            #       print('Done logging')
			#
            #   else:
            #       print("Error with data recieved by server (in dist)")
            #       print("Error data: " + message)
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
		print('IP: '+ IP)
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
