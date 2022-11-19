# PimoroniKeypad

This repository provides the code to create a powerful little human input device (HID) that can be configured perform a huge number of commands. It utilises the [Raspberry Pi Pico](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html) combined with the [Pimoroni RGB Keypad](https://shop.pimoroni.com/products/pico-rgb-keypad-base), provding simple device to interact with.

The device runs using [CircuitPython](https://circuitpython.org/board/raspberry_pi_pico/), and makes use of a number of [adafruit](https://learn.adafruit.com/) libraries to control the microcontroller.

<p align="center">
<img src="https://user-images.githubusercontent.com/48553563/202858752-d25ebd8f-e695-4c09-8769-c22fd0902bfd.jpg" alt="pimoroniRBGkeypad" width="300"/>
</p>

# Installation

There are several steps to get started: 

1. Ensure your device has been loaded with CircuitPython. You can follow [this](https://learn.adafruit.com/welcome-to-circuitpython) guide to do this.

2. Add the following libraries onto the device:
    - adafruit_hid
    - adafruit_bus_device
    - adafruit_dotstar

    You can do this manually with the instructions [here](https://learn.adafruit.com/pico-four-key-macropad/installing-libraries), install them using commands from [pypi](https://pypi.org/), or through the [Manage Packages](https://github.com/thonny/thonny/wiki/InstallingPackages) tool in [Thonny](https://thonny.org/).

3. Copy the [pimoronikeypad](https://github.com/PurpleSquishFace/PimoroniKeypad/tree/main/pimoronikeypad) folder into the lib folder on your device.

4. Copy the [code.py](https://github.com/PurpleSquishFace/PimoroniKeypad/blob/main/Python/code.py) file into the root folder of your device.

5. Create a config.json file and add it into the root folder of your device.

# Credits

As always, software is built on the shoulders of giants - the following have provided the inspriration or the building blocks used to create this library:
-  [sandyjmacdonald](https://gist.github.com/sandyjmacdonald) -  Produced the [Emergency cat GIF macro example](https://gist.github.com/sandyjmacdonald/b465377dc11a8c83a8c40d1c9b990a90).
- [martinohanlon](https://github.com/martinohanlon) - Created a widely used [example of a class to control the Pimoroni RGB Keypad](https://github.com/martinohanlon/pico-rgbkeypad).
- [kevinmcaleer](https://github.com/kevinmcaleer) - Creates very informative [YouTube videos](https://www.youtube.com/playlist?list=PLU9tksFlQRipG1Lql5Gs3sYnMDEvRySa-) on the Raspbery Pi Pico, including with the Pimoroni RGB Keypad where the [RGB class and mapping function both originated](https://github.com/kevinmcaleer/pico-RGB-Keypad).
- [dottxado](https://github.com/dottxado) - Created another [example of a class to conrol the Pimoroni RGB Keypad](https://github.com/dottxado/pico-macro-pad), specifically using CircuitPython and adafruit.
