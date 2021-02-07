import  RPi.GPIO as GPIO
import time
import subprocess

switchPin = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(switchPin, GPIO.IN,pull_up_down=GPIO.PUD_UP)

while True:
   inputValue = GPIO.input(switchPin)
   if (inputValue == False):
       print("Button press ")
       subprocess.run(['sudo', 'python3', '/home/pi/clear.py'])
   time.sleep(0.3)
