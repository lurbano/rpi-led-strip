To set up the pi to automatically connect to your wifi network, you'll have to plug the SD card into your computer and add a file with your wifi information.

* Create a new file named "wpa_supplicant.conf". It should look like this (note: you need to use a plain-text editing program like Atom so you don't end up with hidden text and characters):

*wpa_supplicant.conf*
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
 ssid="networkName"
 psk="yourPassword"
}

* Change: `networkName` and `yourPassword`. You can add other networks by duplicating the last four lines.

* Copy this file to the boot directory of Pi:
