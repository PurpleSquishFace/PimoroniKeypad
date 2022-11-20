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

The `config.json` file drives the customisations and behaviour of the device. The top level properties of the json object set the keypad itself, example below:

``` json
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
`brightness` | Float | The brightness of the keys on the keypad (between 0 and 1).
`colour` | Object | The colour of the keys on the keypad, represented as integer RGB values between 0 and 255.
`loadPattern` | Int Array or String | The order the keys are illuminated in when the keypad first loads, as an array of integers the correspond to the index of the keys (left to right, top to bottom, 0 to 15). Can also be a string to use one of the preset patterns:  *"simple"*, *"diagonal"*, *"spiral"*.
`loadPatternDelay`  | Float  | The amount of delay between each key illuminating during the load animation, in seconds.

The array of objects in the `config` property represent the keys on the device that have been programmed and their properties, example below:

``` json
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
`x` | Integer  | The x coordinate of the key (`0` to `3`, starting top left).
`y` | Integer | The y coordinate of the key (`0` to `3`, starting top left).
`colour` | Object | The colour of the key, represented as integer RGB values between `0` and `255`.

The array of object in the `commands` property represent the commands that each key executes when pressed. Each command object is an array of action objects, which are the individual actions that make up the command. The example below is one command object, made up of multiple actions:

``` json
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
`actionType` | String | The type of action to be performed, either keyboard key press(es) or text input. Represented as `keyboardShortcut` and `enterText` respectively.
`action` | String or String Array | The action performed, dependent on the action type - for the `keyboardShortcut` action type this is an array of keys that should be pressed together, for the `enterText` action type this is a string that is typed in.

Put simply, each programmed key is a different mode for the keypad, where the rest of the keys then perform a different action when pressed. Therefore, with sixteen keys the keypad can be programmed to peform up to 240 unique commands.

When a programmed key is pressed, each command configured is associated one-by-one to each key on the keypad, starting top left and moving left to right, top to bottom (skipping over the main programmed key).
By default keys without an associated command will become the colour set by the keypad, whereas the keys that do have an associated command will be the colour of the programmed set in the configuration.

## PymoroniKeypad

Basic usage of the class in python.

Import the `PimoroniKeypad` class from `pimoronikeypad` module.

``` python
from pimoronikeypad import PimoroniKeypad
```

Create a keypad object.

``` python
keypad = PimoroniKeypad()
```

### Display

The RGB class can be used to set the `colour` of the keypad keys.

``` python
# Don't forget to import the class
from pimoronikeypad import RGB

# Red
keypad.colour = RGB(255, 0, 0)

# Green
keypad.colour = RGB(0, 255, 0)

# Blue
keypad.colour = RGB(0, 0, 255)

# Yellow
keypad.colour = RGB(255, 255, 0)

# Purple
keypad.colour = RGB(128, 0, 128)

# White
keypad.colour = RGB(255, 255, 255)

# Black
keypad.colour = RGB(0, 0, 0)
```

The RGB class has a property and method that can be used.

``` python
colour = RGB(128, 0, 128)

# Passing a tuple of (red, green, blue) updates the colour
colour.value = (255, 128, 0)

# Displays (255, 128, 0)
print(colour.value)

# Prints:
# R: 255
# G: 128
# B: 0
colour.show()
```

The `brightness` property can be updated used to set the brightness of the keypad - it can be a value between `0` and `1`, where `1` is 100% brightness and `0` is 0% brightness. The default brightness is set at 25% as a value of `0.25`.

``` python
# Set brightness at 50%
keypad.brightness = 0.5
```

The following method resets the keypad back to the values set in the `config.json` file.

``` python
keypad.reset()
```

To ignore the configured values, and clear the keypad entirely, use the following method. It will set the `colour` of each key to black and the `brightness` to 0%. 

``` python
keypad.clear()
```

Any updates to the keypad that don't automatically trigger a refresh can be manually updated using this method.

``` python
keypad.update()
```

All the keys can be iterated through using the `keys` property.

``` python
# Print the coordinates of each key
for key in keypad.keys:
    print(key.coordinates)
```

A single key can be referenced by using the x, y coordinates.

``` python
# Get the key in position x = 2, y = 1
key = keypad.get_key(2, 1)
```

An individual key can have it's `colour` and `brightness` properties set.

``` python
# Set colour to red
key.colour = RGB(255, 0, 0)

# Set brightness to 100%
key.brightness = 1

# Update the keypad
keypad.update()
```

**Note**, when setting a key's properties, the keypad's `update()` method needs to be called to trigger the update on the keypad.

### Reading presses

Each key has two properties to provide functionality for reading key presses.

``` python
key = keypad.get_key(0, 0)

# Returns whether the key is pressed as a boolean
pressed = key.is_pressed

# Returns whether the key has remained pressed since the last check as a boolean
still_pressed = key.still_pressed
```

The following method performs the key status check on each key on the keypad.

``` python
keypad.load_pressed_keys()
```

This can be used to check, in conjunction with a single key object, a key for a press.

``` python
key = keypad.get_key(0, 0)

# If the key hasn't been pressed, then pressed is false
pressed = key.is_pressed

# Press down the key, then call the method
keypad.load_pressed_keys()

# The is_pressed property will now be true
pressed = key.is_pressed
```

The `load_pressed_keys()` method returns the keypad's `keys` property, and can be used with a loop to check all keys. Using a continuous loop with this, the keypad can be constantly checked for a pressed key.

``` python
while True:        
    for key in keypad.load_pressed_keys():
        if key.is_pressed:
            print('key', key.coordinates, 'is pressed')
```

### Executing commands

The following property of a key determines if the key has been programmed.

``` python
key = keypad.get_key(0, 0)

if key.is_programmed:
    print('Key has been programmed')
```

Knowing this means the following method can be called. This will put the keypad and key into a `toggled_on` mode. The keypad will be updated so that the keys will reflect the amount of commands configured, as well as which key has been toggled.

``` python
key = keypad.get_key(0, 0)

# Toggling on the keypad and key
keypad.toggle_on(key)

# The method can take parameters to change the key when pressed
keypad.toggle_on(key, brightness=1.0)
keypad.toggle_on(key, colour=RGB(0, 255, 0))
keypad.toggle_on(key, colour=RGB(128, 0, 128), brightness=0.75)
```

While the keypad is in a toggled mode, calling the following method will run a configured command.

``` python
key = keypad.get_key(0, 1)

# Run the command associated with the index of the given key
keypad.run_command(key)
```

Combining the above methods and properties, the following example (from `code.py`) can be used to listen to key presses, toggle between modes, and execute commands.

``` python
from pimoronikeypad import PimoroniKeypad, RGB

keypad = PimoroniKeypad()

while True:
        
    for key in keypad.load_pressed_keys():

        # The still_pressed property checks that the key isn't
        # still pressed from the last iteration, preventing multiple
        # calls per single key press             
        if key.is_pressed and not key.still_pressed:
            
            if keypad.is_toggled_on and not key.is_toggled_on:
                keypad.run_command(key)
            
            elif key.is_toggled_on:
                keypad.reset()
                
            elif key.is_programmed:
                keypad.toggle_on(key, brightness=1.0)
```

Commands can be programmatically created and executed without being specifically linked to a key by the configuration set up. The keypad methods that execute the commands can be called directly.

The following takes a given string and types it as if it were typed in using the keyboard.

``` python
keypad = PimoroniKeypad()

keypad.enter_text('Hello world!')
```

The following method can take up to three keyboard keys, and enter them as if they were pressed at the same time on the keyboard.

``` python
# The keycode class by adafruit will need to be imported
from adafruit_hid.keycode import Keycode

keypad = PimoroniKeypad()

# Press the enter key
keypad.enter_keyboard_shortcut(Keycode.ENTER)

# Press the shortcut Ctrl, S - commonly used to save a document
keypad.enter_keyboard_shortcut(Keycode.LEFT_CONTROL, Keycode.S)

# Press the shortcut Ctrl, Shift, Escape - opens Task Manager on Windows
keypad.enter_keyboard_shortcut(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.ESCAPE)
```

# Credits

As always, software is built on the shoulders of giants - the following have provided the inspriration or the building blocks used to create this library:
-  [sandyjmacdonald](https://gist.github.com/sandyjmacdonald) -  Produced the [Emergency cat GIF macro example](https://gist.github.com/sandyjmacdonald/b465377dc11a8c83a8c40d1c9b990a90).
- [martinohanlon](https://github.com/martinohanlon) - Created a widely used [example of a class to control the Pimoroni RGB Keypad](https://github.com/martinohanlon/pico-rgbkeypad).
- [kevinmcaleer](https://github.com/kevinmcaleer) - Creates very informative [YouTube videos](https://www.youtube.com/playlist?list=PLU9tksFlQRipG1Lql5Gs3sYnMDEvRySa-) on the Raspbery Pi Pico, including with the Pimoroni RGB Keypad where the [RGB class and mapping function both originated](https://github.com/kevinmcaleer/pico-RGB-Keypad).
- [dottxado](https://github.com/dottxado) - Created another [example of a class to conrol the Pimoroni RGB Keypad](https://github.com/dottxado/pico-macro-pad), specifically using CircuitPython and adafruit.
