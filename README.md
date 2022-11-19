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

4. Copy the [code.py](https://github.com/PurpleSquishFace/PimoroniKeypad/blob/main/code.py) file into the root folder of your device.

5. Create a config.json file and add it into the root folder of your device.

# Usage

The code is usable straight out of the box, once a config.json file has been created. However, custom logic can be achieved by interfacing with the library.

## config.json
---

The config.json file drives the customisations and behaviour of the device. The top level properties of the json object set the board itself, example below:

```json
{
    "brightness": 0.25,
    "colour": {             
      "red": 150,
      "green": 150,
      "blue": 150
    },
    "loadPattern": [ 0, 2, 5, 7, 8, 10, 13, 15, 1, 3, 4, 6, 9, 11, 12, 14 ],
    "loadPatternDelay": 0.01,
    "config": [...]
  }
```

Property | Data Type | Description
--- | --- | ---
brightness | Float | The brightness of the keys on the board (between 0 and 1).
colour | Object | The colour of the keys on the board, represented as integer RGB values between 0 and 255.
loadPattern | Int Array or String | The order the keys are illuminated in when the board first loads, as an array of integers the correspond to the index of the keys (left to right, top to bottom, 0 to 15). Can also be a string to use one of the preset patterns:  *"simple"*, *"diagonal"*, *"spiral"*.
loadPatternDelay  | Float  | The amount of delay between each key illuminating during the load animation, in seconds.

The array of objects in the *config* property represent the keys on the device that have been programmed and their properties, example below:

```json
{
    "x": 0,
    "y": 0,
    "colour": {
        "red": 255,
        "green": 0,
        "blue": 0
    },
    "commands": [...]
}
```
Property | DataType | Description
--- | --- | ---
x | Integer  | The x coordinate of the key (0 to 3, starting top left).
y | Integer | The y coordinate of the key (0 to 3, starting top left).
colour | Object | The colour of the key, represented as integer RGB values between 0 and 255.

The array of object in the *commands* property represent the commands that each key executes when pressed. Each command object is an array of action objects, which are the individual actions that make up the command. The example below is one command object, made up of multiple actions:

```json
[
    {
        "actionType": "keyboardShortcut",
        "action": [
            "windows"
        ]
    },
    {
        "actionType": "enterText",
        "action": "chrome"
    },
    {
        "actionType": "keyboardShortcut",
        "action": [
            "enter"
        ]
    },
    {
        "actionType": "enterText",
        "action": "https://giphy.com/explore/cat"
    },
    {
        "actionType": "keyboardShortcut",
        "action": [
            "enter"
        ]
    }
],
```
Property | DataType | Description
--- | --- | ---
actionType | String | The type of action to be performed, either keyboard key press(es) or text input. Represented as *"keyboardShortcut"* and *"enterText"* respectively.
action | String or String Array | The action performed, dependent on the action type - for the *keyboardShortcut* action type this is an array of keys that should be pressed together, for the *enterText* action typee this is a string that is typed in.

Put simply, each programmed key is a different mode for the board, where the rest of the keys then perform a different action when pressed. Therefore, with sixteen keys the board can be programmed to peform up to 240 unique commands.

When a programmed key is pressed, each command configured is associated one-by-one to each key on the board, starting top left and moving left to right, top to bottom (skipping over the main programmed key).
By default keys without an associated command will become the colour set by the board, whereas the keys that do have an associated command will be the colour of the programmed  set in the configuration.

# Credits

As always, software is built on the shoulders of giants - the following have provided the inspriration or the building blocks used to create this library:
-  [sandyjmacdonald](https://gist.github.com/sandyjmacdonald) -  Produced the [Emergency cat GIF macro example](https://gist.github.com/sandyjmacdonald/b465377dc11a8c83a8c40d1c9b990a90).
- [martinohanlon](https://github.com/martinohanlon) - Created a widely used [example of a class to control the Pimoroni RGB Keypad](https://github.com/martinohanlon/pico-rgbkeypad).
- [kevinmcaleer](https://github.com/kevinmcaleer) - Creates very informative [YouTube videos](https://www.youtube.com/playlist?list=PLU9tksFlQRipG1Lql5Gs3sYnMDEvRySa-) on the Raspbery Pi Pico, including with the Pimoroni RGB Keypad where the [RGB class and mapping function both originated](https://github.com/kevinmcaleer/pico-RGB-Keypad).
- [dottxado](https://github.com/dottxado) - Created another [example of a class to conrol the Pimoroni RGB Keypad](https://github.com/dottxado/pico-macro-pad), specifically using CircuitPython and adafruit.
