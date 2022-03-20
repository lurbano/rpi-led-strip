# RPi-led-strip
Instructions for setting up a headless Raspberry Pi Zero. Projects for controlling things like sensors and LED strips with a local server are based off of this.
* Lensyl Urbano
* https://montessorimuddle.org

# Install OS
## Create image on the SD card:
 (make image using Raspberry Pi Imager: https://www.raspberrypi.org/software/)

## Setup ssh, wifi, and usb connection
 Working in the /boot directory of the newly created SD Card:

### 1) File: ssh
[copy] or create empty file ***ssh*** on SD Card's boot directory
* Filename: *ssh*


### 2) File: wpa_supplicant.conf
[edit] or create file for wifi connection and copy to boot directory of Pi:
* File name: *wpa_supplicant.conf*
* Change: `networkName` and `yourPassword`

The file should look like:

*wpa_supplicant.conf*
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
 ssid="networkName"
 psk="yourPassword"
}
```

### 3) [Semi-Optional] Changing the hostname
This is makes it easier to connect, because you don't have to remember the ip address (see below). You have to edit two files `/etc/hostname` and `/etc/hosts`. Replace the default hostname `raspberrypi` in both files.

Detailed instructions: https://thepihut.com/blogs/raspberry-pi-tutorials/19668676-renaming-your-raspberry-pi-the-hostname

If I change the name of my pi to "***makerspace***" I can access it by logging in to ***pi@makerspace.local***
'''ssh pi@makerspace.local'''

Using the local hostname does not seem to work on phones for some reason right now (3/20/22), however, I usually find it easier to set up the local name, log in using a laptop, and find the ip address using the ***ifconfig*** command


### 4) [Optional] USB connection (Buggy right now (3/20/22) I usually skip.)
[copy] over or update files on the SD Card for usb connection (https://learn.adafruit.com/turning-your-raspberry-pi-zero-into-a-usb-gadget/ethernet-gadget)

File: ***config.txt***:
* Add `dtoverlay=dwc2` as the last line.
 ```
dtoverlay=dwc2
```

File: ***cmdline.txt***:
* Insert:
``` modules-load=dwc2,g_ether``` after `rootwait`
* It should look something like: ( `rootwait modules-load=dwc2,g_ether`).

The SD Card should now be ready for the Pi.

# Set up Pi
Plug the SD Card into the Pi.

## Connect to Pi

Plug Pi into Laptop USB then once pi has booted up:

*Option 1: Windows*: Login with (putty: https://www.putty.org/):
* PuTTY Host/IP: raspberrypi.local
* Port: 22
* Username: pi
* Password: raspberry

*Option 2: Mac or Linux*: use Terminal app, which is built in, for the command line:
```console
ssh pi@raspberrypi.local
```

*NOTE: Troubleshooting*: you may have to remove the **~/.ssh/known_hosts** file if you find yourself logging in to the wrong pi or unable to connect.
```console
rm .ssh/known_hosts
```

## [Optional] Other ways to connect:
You can connect using the pi's IP address if you're logged into the pi, or using an IP address scanner (I've used *Fing* on my Android device).

### Find the local IP address (optional)
You may want to find the IP address of the pi to log in with instead of using pi@raspberrypi.local. When you are ssh'd into the pi. This is particularly useful if you have multiple pi's on the network. Run the command:
```console
ifconfig
```
There will be a section of the output labeled `wlan` that has a couple lines that look like this:
```bash
wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.4.76  netmask 255.255.0.0  broadcast 192.168.255.255
```
In this case the IP address is 192.168.4.76 and you can log in using:
```console
ssh pi@192.168.4.76
```


# update Pi
Once you're logged into the Pi update using the following commands:
 ```console
sudo apt-get update
sudo apt-get upgrade
```

## REBOOT pi
 ```console
sudo reboot
```
