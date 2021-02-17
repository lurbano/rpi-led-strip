# RPi-led-strip
* Instructions for setting up a headless raspberry pi to control a NeoPixel (WS281x) LED strip.
* Lensyl Urbano
* https://montessorimuddle.org

 # References for this project:
  RGB: https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel
       https://thepihut.com/blogs/raspberry-pi-tutorials/using-neopixels-with-the-raspberry-pi

 # Install OS
 A: Make the image on the SD card:
 (make image using Raspberry Pi Imager: https://www.raspberrypi.org/software/)

 ## Setup ssh, wifi, and usb connection
 Working on the boot directory of the SD Card
 1) [copy] or create empty file "ssh" from raspberry-pi_setup directory to boot directory
     Filename: ssh

 2) [edit] or create file for wifi connection and copy to boot directory of Pi:
     File name: wpa_supplicant.conf
     Change: networkName and yourPassword

   ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
   update_config=1

   network={
     ssid="networkName"
     psk="yourPassword"
   }

 3) [copy] over or update files on the SD Card for usb connection (https://learn.adafruit.com/turning-your-raspberry-pi-zero-into-a-usb-gadget/ethernet-gadget)
 a) "config.txt": Add 'dtoverlay=dwc2' as the last line.
 b) "cmdline.txt": Add ' modules-load=dwc2,g_ether' after 'rootwait' (e.g. 'rootwait modules-load=dwc2,g_ether').


 # Connect to pi

 B: Plug Pi into Laptop USB then once pi has booted up:
     Login with (putty):
       PuTTY Host/IP: raspberrypi.local
       Port: 22
       Username: pi
       Password: raspberry

     OR (command line):
       > ssh pi@raspberrypi.local

     NOTE: you may have to remove the ~/.ssh/known_hosts file if you find yourself logging in to the wrong pi.

 ## update pi
 > sudo apt-get update

 > sudo apt-get upgrade

 ## REBOOT pi
 > sudo reboot

 ## Install neopixel and rpi_ws281x

 > sudo pip3 install adafruit-circuitpython-neopixel

 > sudo pip3 install rpi_ws281x


 ## [OPTIONAL] test program (test.py)
 If you'd like to test the setup you can create this python file and run it, however, there the test programs are in this repository which you can download individually, or use when you install this repository as described in a following section.
 * test files can be found in ~/rpi-led-strip/pyLED

    import board
    import neopixel

    npix = 20
    pixels = neopixel.NeoPixel(board.D18, 20)
    pixels[-1] = (0,10,0)


 ### to run the test program
 > sudo python3 test.py


 ### [SKIP] to set the program to run on startup.
 Ref: https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup/all
 > sudo nano /etc/rc.local

and add the following line (change your filename and path) before the 'exit 0' line to run the 'clear.py' program in your home directory:
> sudo python3 /home/pi/clear.py &


# Installing this software: rpi-led-strip
From your home directory clone the github repository.
> git clone https://github.com/lurbano/rpi-led-strip.git

# Attaching the LED strip
Using a WS281x strip that has three contacts for input voltage (Vin), controller signal (D0), and ground (GND):
* Vin connects to any 5V pin,
* DO connects to GPIO 18 by default (set in server.py as variable: ledPin)
* GND connects any ground pin


# Running with Tornado Webserver

Setting up the tornado server used for Websockets
> sudo pip3 install tornado

## Starting server
Go to the folder ~/rpi-led-strip/webServer/ and run the command
> sudo python3 server.py

This assumes 20 pixels. To set a different number of pixels add the -n option (43 pixels in this example):
> sudo python3 server.py -n 43

[optional] You can override the default number of pixels by changing on about line 24 of rpi-led-strip/webServer/server.py the number on the line below (the default is 20):
> nPix = 20

## The webpage
The webpage will be at the pi's ip address (which should be printed to the screen when you start the server) and on port 8040 so if your ip address is 192.168.1.234 use:
> http://192.168.1.234:8040

## Starting up on boot
** IMPORTANT **: the directory with the files needs to be in the pi home directory (e.g. /home/pi/rpi-led-strip) with this setup. You can change this but be sure to put the full path to the commands
from: https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup

Edit /etc/rc.local (the easy way)
> sudo nano /etc/rc.local

ADD THE LINE (before 'exit 0' ). TO SET THE NUMBER OF PIXELS CHANGE THE -n 20 OPTION TO YOUR NUMBER.

> sudo /usr/bin/python3 /home/pi/rpi-led-strip/webServer/server.py -n 20 2> /home/pi/rpi-led-strip/error.log &

[optional] This second line allows you to use the physical switch (if it is installed) to clear the led strip:
> sudo python3 /home/pi/rpi-led-strip/pyLED/clearSwitch.py &

[optional] I like to have the first pixel light up on booting the Pi as an indicator that the Pi is booted so I usually also include (these also use the -n option for the number of pixels):
```
sudo python3 /home/pi/rpi-led-strip/pyLED/clear.py -n 20 &
sudo python3 /home/pi/rpi-led-strip/pyLED/startup.py &
```


Save and then restart the Pi from the command line:
> sudo reboot


## If you need to kill the server (and it's the only thing running with python3)
* https://unix.stackexchange.com/questions/104821/how-to-terminate-a-background-process
> pgrep -a python3
* this will give you the process id, the name line of the command, and a number 'nnn'. Find the one that has 'python3 server.py'. To kill use:
> sudo kill nnn


## Refs:
* OLED: http://codelectron.com/setup-oled-display-raspberry-pi-python/
* https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi/usage



# [EXAMPLE] Adding things to be controlled by the webpage
Say you want to add a button that makes the LED's blue

## Add button to webpage:
webServer/templates/index.html around line 24
```<input type="button" id="blueButton" value="Blue">
```

## Add javascript
to listen for when someone clicks the blueButton:
webserver/static/ws-client.js near bottom of file
```
$("#blueButton").click(function(){
   var msg = '{"what": "blueButton"}';
   ws.send(msg);
});
```

Here we're sending the dict {"what": "blueButton"} to the server.

## Have the server act
It has to figure out what to do when it gets the message: msg = {"what": "blueButton"} in webserver/server.py around line 76. Here it cancels anything already going on (ledPix.cancelTask) and calls the method .blue() from the ledPix instance of the ledPixels class (you'll most often need to add your own method (see next step)).
```
      if msg["what"] == "blueButton":
        print("blue LEDs ")
        ledPix.cancelTask()
        ledPix.blue()
```
## Code method
If needed, add code to the ledPixels class (in webserver/ledPixels.py file) to do what you want it to do (ledPix is an instance of this class).
```
def blue(self):
      for i in range(self.nPix):
          self.pixels[i] = (0,0,200)
          self.pixels.show()
```
# Troubleshooting

## Not all lights are being controlled
The code defaults to 20 LEDs so if some of the lights are not being controlled then
