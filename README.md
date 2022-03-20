# RPi-led-strip
Instructions for setting up a headless Raspberry Pi Zero to control a NeoPixel (WS281x) LED strip. The LED strip can be controlled through a tornado webserver.

This procedure has only been tested on the Pi Zero. It does not work on the B+, and I don't know about other Pi versions.
* Lensyl Urbano
* https://montessorimuddle.org

* Exercises for learning to control the LED strip with programming can be found at
** https://soriki.com/rpi-led-strip/exercises/


# Set up Raspberry Pi

[Set up instructions](PI_SETUP.md)
* Use these [instructions](PI_SETUP.md) to install the operating system on your Pi and allow it to connect to your local network.


# Install LED specific software: neopixel and rpi_ws281x
When you are logged in to the pi, to be able to control the led strip run the commands in your terminal. (The second may be unnecessary).

 ```console
sudo pip3 install adafruit-circuitpython-neopixel
sudo pip3 install rpi_ws281x
```

# Attaching the LED strip [HARDWARE]
Using a WS281x strip that has three contacts for input voltage (Vin), controller signal (D0), and ground (GND):
* Vin connects to any 5V pin,
* DO connects to GPIO 18 by default (set in server.py as variable: ledPin)
* GND connects any ground pin


# Installing this software: rpi-led-strip
From your home directory clone the github repository.
```console
git clone https://github.com/lurbano/rpi-led-strip.git
```

This includes python programs to run the led strip in the folder ***rpi-led-strip/pyLED***, as well as the programs to run the server (see below).

## [OPTIONAL] test program (test.py)
 If you'd like to test the setup you can create this python file and run it, however, there the test programs are in this repository which you can download individually, or use when you install this repository as described in a following section.
 * NOTE: test files can be found in ~/rpi-led-strip/pyLED

*rpi-led-strip/pyLed/test1.py*
```.py
import board
import neopixel

npix = 20
pixels = neopixel.NeoPixel(board.D18, 20)
pixels[-1] = (0,10,0)
```

To go to this directory use the `cd` command (if neeeded):
```console
cd rip-led-strip/pyLED
```

To run the test program use `sudo` (neopixel needs sudo to work) and `python3`:
 ```console
sudo python3 test1.py
```



# Setting up Server (Tornado)

You don't need to set up the server if you just want to log in to the Pi and run programs from the command line. The server allows you to control the LED strip using a web page.

## Install Tornado Webserver

Setting up the tornado server used for Websockets:
```console
sudo pip3 install tornado
```

## Starting server
Go to the folder *~/rpi-led-strip/webServer/* and run the command
```console
sudo python3 server.py
```

This assumes 20 pixels. To set a different number of pixels add the `-n` option (43 pixels in this example):
```console
sudo python3 server.py -n 43
```

[OPTIONAL] You can override the default number of pixels by changing on about line 24 of rpi-led-strip/webServer/server.py the number on the line below (the default is 20):
```.py
nPix = 20
```

### The webpage
The webpage will be at the pi's ip address (which should be printed to the screen when you start the server) and on port 8040 so if your ip address is 192.168.1.234, open up your browser and go to:
> http://192.168.1.234:8040

### Starting up on boot
** IMPORTANT **: the directory with the files needs to be in the pi home directory (e.g. */home/pi/rpi-led-strip*) with this setup. You can change this but be sure to put the full path to the commands. (From: https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup)

EDIT */etc/rc.local* (the easy way)
```console
sudo nano /etc/rc.local
```

ADD THE LINE (before `exit 0` ). TO SET THE NUMBER OF PIXELS CHANGE THE -n 20 OPTION TO YOUR NUMBER.

```
sudo /usr/bin/python3 /home/pi/rpi-led-strip/webServer/server.py -n 20 2> /home/pi/rpi-led-strip/error.log &
```

[OPTIONAL] I like to have the first pixel light up on booting the Pi as an indicator that the Pi is booted so I usually also include (these also use the -n option for the number of pixels). Insert these lines before the command to start the server:
```
sudo python3 /home/pi/rpi-led-strip/pyLED/clear.py -n 20 &
sudo python3 /home/pi/rpi-led-strip/pyLED/startup.py &
```

[OPTIONAL] This line allows you to use the physical switch (if it is installed) to clear the led strip:
```
sudo python3 /home/pi/rpi-led-strip/pyLED/clearSwitch.py &
```

Save and exit (Ctrl-S and Ctrl-X) and then restart the Pi from the command line:
```console
sudo reboot
```


## If you need to kill the server
* https://unix.stackexchange.com/questions/104821/how-to-terminate-a-background-process
```console
pgrep -a python3
```
* this will give you the process id, the name line of the command, and a number 'nnn'. Find the one that has 'python3 server.py'. To kill use:
```console
sudo kill nnn
```



# [EXAMPLE] Adding things to be controlled by the webpage
Say you want to add a button that makes the LED's blue

## Add button to webpage:
*webServer/templates/index.html* around line 24
```HTML
<input type="button" id="blueButton" value="Blue">
```

## Add javascript
to listen for when someone clicks the blueButton:
*webserver/static/ws-client.js* near bottom of file
```js
$("#blueButton").click(function(){
   var msg = '{"what": "blueButton"}';
   ws.send(msg);
});
```

Here we're sending the dict {"what": "blueButton"} to the server.

## Have the server act
It has to figure out what to do when it gets the message: msg = {"what": "blueButton"} in *webserver/server.py* around line 76. Here it cancels anything already going on (ledPix.cancelTask) and calls the method .blue() from the ledPix instance of the ledPixels class (you'll most often need to add your own method (see next step)).
```.py
      if msg["what"] == "blueButton":
        print("blue LEDs ")
        ledPix.cancelTask()
        ledPix.blue()
```
## Code method
If needed, add code to the ledPixels class (in webserver/ledPixels.py file) to do what you want it to do (ledPix is an instance of this class).
```.py
def blue(self):
      for i in range(self.nPix):
          self.pixels[i] = (0,0,200)
          self.pixels.show()
```

# Refs:
OLED:
* http://codelectron.com/setup-oled-display-raspberry-pi-python/
* https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi/usage

RGB:
* https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel
* https://thepihut.com/blogs/raspberry-pi-tutorials/using-neopixels-with-the-raspberry-pi

# Troubleshooting

## Not all lights are being controlled
The code defaults to 20 LEDs so if some of the lights are not being controlled then
