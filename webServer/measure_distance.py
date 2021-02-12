#! /usr/bin/python3
# From: https://www.hackster.io/dataplicity/control-raspberry-pi-gpios-with-websockets-af3d0c
from gpiozero import LED, Button
from signal import pause

from distance_sensor import *
from oledU import *


dSensor = uSonicDistance()
oled = oledU(128,32)

def measure_distance():
    data = dSensor.measure()
    oled.write(str(data)+" cm")
    print("Button Data: "+ str(data))
    return data


led = LED(26)
button = Button(18)

button.when_pressed = measure_distance

pause()
