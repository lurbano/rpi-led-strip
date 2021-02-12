# RPi-led-strip
 Instructions for setting up a headless raspberry pi to control a NeoPixel (WS281x) LED strip.


 # References:
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


 ## test program (test.py)

    import board
    import neopixel

    npix = 20
    pixels = neopixel.NeoPixel(board.D18, 20)
    pixels[-1] = (0,10,0)


 ## to run the test program
 > sudo python3 test.py


 ## to set the program to run on startup.
 Ref: https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup/all
 > sudo nano /etc/rc.local

and add the following line (change your filename and path) before the 'exit 0' line to run the 'clear.py' program in your home directory:
> sudo python3 /home/pi/clear.py &


# Running with Tornado Webserver

Setting up the tornado server used for Websockets
> sudo pip3 install tornado

at is used to schedule commands by our software, but needs to be installed
> sudo apt-get install at

## Starting server
Go to the folder rpi-led-strip/webServer/ and run the command
> sudo python3 server.py

## Starting up on boot
** IMPORTANT **: the directory with the files needs to be in the pi home directory (e.g. /home/pi/rpi-led-strip) with this setup. You can change this but be sure to put the full path to the commands
### set up to start server automatically on startup
from: https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup

Edit /etc/rc.local (the easy way)
> sudo nano /etc/rc.local

ADD THE LINES (before 'exit 0' ):

> sudo /usr/bin/python3 /home/pi/rpi-led-strip/webServer/server.py 2> /home/pi/error.log &


## If you need to kill the server (and it's the only thing running with python3)
* https://unix.stackexchange.com/questions/104821/how-to-terminate-a-background-process
> pgrep -a python3
* this will give you the process id, a number 'nnn'. Use the one that has 'python3 server.py'. To kill use:
> sudo kill nnn


## Refs:
* OLED: http://codelectron.com/setup-oled-display-raspberry-pi-python/
* https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi/usage



# Adding things to be controlled by the webpage
Say you want to add a button that makes the LED's blue

## Add button to webpage: webServer/templates/index.html around line 24
> <input type="button" id="blueButton" value="Blue">

## Add javascript to act when someone clicks the blueButton: webserver/static/ws-client.js near bottom of file
> $("#blueButton").click(function(){
>    var msg = '{"what": "blueButton"}';
>    ws.send(msg);
> });

Here we're sending the dict {"what": "blueButton"} to the server.

## Have the server figure out what to do when it gets the message: msg = {"what": "blueButton"} in webserver/server.py around line 76.
> if msg["what"] == "blueButton":
>   print("blue LEDs ")
>   ledPix.blue()

## If needed, add code to the ledPixels class (in webserver/ledPixels.py file) to do what you want it to do (ledPix is an instance of this class).
> def blue(self):
>       for i in range(self.nPix):
>           self.pixels[i] = (0,0,200)
>           self.pixels.show()




#[IN TESTING]

# Webserver
install apache webserver and php
> sudo apt install apache2 -y
> sudo apt install php libapache2-mod-php -y

put web files in the folder
> /var/www/html/

Use browser to go to ip address eg:
> http://192.168.1.115/test.html


## Running python files using php. You'll need to add to your /etc/sudoers file the line:
> www-data ALL=(ALL) NOPASSWD: ALL

 Note: this is somewhat insecure, but I'm using this because we're only set up to use on our local network.
