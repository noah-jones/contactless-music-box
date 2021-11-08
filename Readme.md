# Contactless Music Box

These are building instructions along with sample software to build a small music player that interacts with contactless NFC tags.

## Hardware

* **Raspberry Pi** I used the Raspberry Pi 3 Model A+ because the form factor matches the little amplifier board, the price is great and the computing power is more than suficient.
* **An RPi amplifier / sound card** based on the premium HifiBerry Amp https://www.hifiberry.com/shop/boards/hifiberry-amp2/ . Lower cost alternatives are available, e.g. "RPI HiFi AMP HAT TAS5713 Amplifier Audio Module 25W Class-D Power Sound Card Expansion Board for Raspberry Pi 4 3 B+ Pi Zero Nichicon Capacitor" The main point is that the board has an amplifier with an output power and resistance that matches your intended speakers and that supports the I2S serial interface to connect to the Raspi. Or at least works with the Hifiberry driver, independent of how it connects over serial. (Wow, there is an amp now in the Pi Zero form factor! https://www.hifiberry.com/shop/boards/miniamp/)
* A passive **speaker**, e.g. a 4 Ohm 20 W satellite speaker from a surround system.
* An **NFC tag reader** module, e.g the red PN532 board.
* A 12V, 2A power supply, depending on your audio board
* SD card
* contactless tags, e.g. mifare ultralight, "NFC Tag Sticker (10 Stück) NTAG215 - 540 Byte Speicher", 27mm diameter self-adhesive

The idea is that this combination of hardware can run continuously without consumin much power and without outputting static noise through the speakers. If your raspberry pi has an audio jack, you might want to hook that up to an active speaker, even a bluetooth one, but I found that always emit too much static noise even when not playing.

### Connecting the devices

The contactless module is connected to pins 8 and 10 (UART TX + RX) on the raspberry pi as well as 5V or 3V3 depending on your module and ground. The hifiberry audio card is plugged like a shield on top of the raspberry pi and by that connects to SPI.

## Software

* Raspbian OS on the raspberry pi.
* python3
* libnfc
* mplayer
* youtube-dl for loading audio from various sources on the fly
* python module nfcpy

In this concept you load an NDEF https type record with a downloadable sound or video URL onto an NFC (e.g.

### Installation instructions

Install the dependencies.

On raspberry pi, the UART pins are usually configured to be already in use for the TTY serial terminal. Disable that by typing `raspi-config` and following the menu. But leave the serial hardware enabled. After this step and a reboot, the `/dev/ttyS0` device appears.

To enable the audio hardware, you need to load an additional driver. To do that, edit the `/boot/config.txt` file to include this

```
#dtparam=audio=on
dtoverlay=hifiberry-amp
```

Set the audio volume with `alsamixer`

Make and chown a new directory for storing the loaded audio files in `/var/lib/youtube`

Now to make this so it runs automatically on each boot, install the systemd service from the `contactless.service` file. It specifically references the path of the main program file, e.g. `/home/pi/app.py`


### Extra steps

if you want to use the additional remote control functionality for Onkyo / Denon / Pioneer AV Receivers, install `pip3 install onkyo-eiscp`.
