# Contactless Music Box

These are building instructions along with sample software to build a small music player that interacts with contactless NFC tags.

## Hardware

* **Raspberry Pi** I used the Raspberry Pi 3 Model A+ because the form factor matches the little amplifier board, the price is great and the computing power is more than suficient.
* **An RPi amplifier / sound card** based on the premium HifiBerry Amp https://www.hifiberry.com/shop/boards/hifiberry-amp2/ . Lower cost alternatives are available, e.g. "RPI HiFi AMP HAT TAS5713 Amplifier Audio Module 25W Class-D Power Sound Card Expansion Board for Raspberry Pi 4 3 B+ Pi Zero Nichicon Capacitor" The main point is that the board has an amplifier with an output power and resistance that matches your intended speakers and that supports the I2S serial interface to connect to the Raspi. Or at least works with the Hifiberry driver, independent of how it connects over serial. (Wow, there is an amp now in the Pi Zero form factor! https://www.hifiberry.com/shop/boards/miniamp/)
* A passive **speaker**, e.g. a 4 Ohm 20 W satellite speaker from a surround system.
+ An **NFC tag reader** module, e.g the red PN532 board.
