import time
import json
import board
import busio
import usb_hid

from adafruit_bus_device.i2c_device import I2CDevice
import adafruit_dotstar

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

from digitalio import DigitalInOut, Direction


"""
PimoroniKeypad
================================================================================
Provides functionality to load in config values, programmatically update the 
keypad, and enable the keypad to perform as a HID
"""

class PimoroniKeypad:
    """ An implementation of the Pimoroni Keypad using CircuitPython and adafruit """
    
    load_patterns = {
        'simple' : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        'diagonal' : [0, 4, 1, 8, 5, 2, 12, 9, 6, 3, 13, 10, 7, 14, 11, 15],
        'spiral' : [9, 5, 6, 10, 14, 13, 12, 8, 4, 0, 1, 2, 3, 7, 11, 15]
    }
    """ A dictionary of preconfigured load animation patterns mapped to the value from the configuration """

    keycode_dictionary = {
            'alt': Keycode.ALT,
            'application': Keycode.APPLICATION,
            'backslash': Keycode.BACKSLASH,
            'backspace': Keycode.BACKSPACE,
            'capsLock': Keycode.CAPS_LOCK,
            'comma': Keycode.COMMA,
            'command': Keycode.COMMAND,
            'control': Keycode.CONTROL,
            'delete': Keycode.DELETE,
            'downArrow': Keycode.DOWN_ARROW,
            'end': Keycode.END,
            'enter': Keycode.ENTER,
            'equals': Keycode.EQUALS,
            'escape': Keycode.ESCAPE,
            'f1': Keycode.F1,
            'f10': Keycode.F10,
            'f11': Keycode.F11,
            'f12': Keycode.F12,
            'f13': Keycode.F13,
            'f14': Keycode.F14,
            'f15': Keycode.F15,
            'f16': Keycode.F16,
            'f17': Keycode.F17,
            'f18': Keycode.F18,
            'f19': Keycode.F19,
            'f2': Keycode.F2,
            'f20': Keycode.F20,
            'f21': Keycode.F21,
            'f22': Keycode.F22,
            'f23': Keycode.F23,
            'f24': Keycode.F24,
            'f3': Keycode.F3,
            'f4': Keycode.F4,
            'f5': Keycode.F5,
            'f6': Keycode.F6,
            'f7': Keycode.F7,
            'f8': Keycode.F8,
            'f9': Keycode.F9,
            'forwardSlash': Keycode.FORWARD_SLASH,
            'four': Keycode.FOUR,
            'graveAccent': Keycode.GRAVE_ACCENT,
            'gui': Keycode.GUI,
            'home': Keycode.HOME,
            'insert': Keycode.INSERT,
            'keypadAsterisk': Keycode.KEYPAD_ASTERISK,
            'keypadBackslash': Keycode.KEYPAD_BACKSLASH,
            'numlock': Keycode.KEYPAD_NUMLOCK,
            'plus': Keycode.KEYPAD_PLUS,
            'leftAlt': Keycode.LEFT_ALT,
            'leftArrow': Keycode.LEFT_ARROW,
            'leftBracket': Keycode.LEFT_BRACKET,
            'leftControl': Keycode.LEFT_CONTROL,
            'leftGui': Keycode.LEFT_GUI,
            'leftShift': Keycode.LEFT_SHIFT,
            'minus': Keycode.MINUS,
            'option': Keycode.OPTION,
            'pageDown': Keycode.PAGE_DOWN,
            'pageUp': Keycode.PAGE_UP,
            'pause': Keycode.PAUSE,
            'period': Keycode.PERIOD,
            'pound': Keycode.POUND,
            'power': Keycode.POWER,
            'printScreen': Keycode.PRINT_SCREEN,
            'quote': Keycode.QUOTE,
            'return': Keycode.RETURN,
            'rightAlt': Keycode.RIGHT_ALT,
            'rightArrow': Keycode.RIGHT_ARROW,
            'rightBracket': Keycode.RIGHT_BRACKET,
            'rightControl': Keycode.RIGHT_CONTROL,
            'rightGui': Keycode.RIGHT_GUI,
            'rightShift': Keycode.RIGHT_SHIFT,
            'scrollLock': Keycode.SCROLL_LOCK,
            'semicolon': Keycode.SEMICOLON,
            'shift': Keycode.SHIFT,
            'space': Keycode.SPACE,
            'spacebar': Keycode.SPACEBAR,
            'tab': Keycode.TAB,
            'upArrow': Keycode.UP_ARROW,
            'windows': Keycode.WINDOWS,
            'a': Keycode.A,
            'b': Keycode.B,
            'c': Keycode.C,
            'd': Keycode.D,
            'e': Keycode.E,
            'f': Keycode.F,
            'g': Keycode.G,
            'h': Keycode.H,
            'i': Keycode.I,
            'j': Keycode.J,
            'k': Keycode.K,
            'l': Keycode.L,
            'm': Keycode.M,
            'n': Keycode.N,
            'o': Keycode.O,
            'p': Keycode.P,
            'q': Keycode.Q,
            'r': Keycode.R,
            's': Keycode.S,
            't': Keycode.T,
            'u': Keycode.U,
            'v': Keycode.V,
            'w': Keycode.W,
            'x': Keycode.X,
            'y': Keycode.Y,
            'z': Keycode.Z
        }
    """ A dictionary mapping values from the configuration to the corresponding keyboard keycode """
    
    def __init__(self):
        """ An implementation of the Pimoroni Keypad using CircuitPython and adafruit """

        # load data from config.json
        self.config = self.load_config()
        brightness = self.config['brightness']
        config_colour = self.config['colour'] 
        colour = RGB(config_colour['red'], config_colour['green'], config_colour['blue'])
             
        # Pull CS pin low to enable level shifter
        self._cs = DigitalInOut(board.GP17)
        self._cs.direction = Direction.OUTPUT
        self._cs.value = 0

        # Set up APA102 pixels
        self._num_pixels = 16
        self._pixels = adafruit_dotstar.DotStar(board.GP18, board.GP19, self._num_pixels, brightness=brightness, auto_write=True)

        # Set up I2C for IO expander (addr: 0x20)
        self._i2c = busio.I2C(board.GP5, board.GP4)
        self._device = I2CDevice(self._i2c, 0x20)

        # Set up the keyboard
        self._kbd = Keyboard(usb_hid.devices)
        self._layout = KeyboardLayoutUS(self._kbd)
        
        # Set up values
        self.keys = []
        self.default_colour = colour
        self.colour = colour        
        self.default_brightness = brightness
        self.brightness = brightness        
        self.is_toggled_on = False        
        self.toggled_key = None
        
        # Set up keys
        for row in range(4):
            for col in range(4):
                self.keys.append(KeypadKey(self, row, col, brightness=brightness))
        self.set_key_config()
        self.load()

    @property
    def config(self):
        """ The config file values represented as a dictionary """
        return self._config
    
    @config.setter
    def config(self, value):
        if isinstance(value, dict):
            self._config = value
        else:
            raise TypeError('config must be a dictionary')
        
    @config.deleter
    def config(self):
        raise AttributeError('Do not delete config')

    @property
    def keys(self):
        """ The list of keys that make up the kepad """
        return self._keys
    
    @keys.setter
    def keys(self, value):
        if isinstance(value, list):
            self._keys = value
        else:
            raise TypeError('keys must be a list array')
        
    @keys.deleter
    def keys(self):
        raise AttributeError('Do not delete keys')

    @property
    def default_colour(self):
        """ The default colour of the keypad, regardless of what the current brightness is set """
        return self._default_colour
    
    @default_colour.setter
    def default_colour(self, value):
        if isinstance(value, RGB):
            self._default_colour = value
        else:
            raise TypeError('default_colour must be an RGB object')
        
    @default_colour.deleter
    def default_colour(self):
        raise AttributeError('Do not delete default_colour')

    @property
    def colour(self):
        """ The colour of the keys of the board """
        return self._colour
    
    @colour.setter
    def colour(self, value):
        if isinstance(value, RGB):
            self._colour = value
            for key in self.keys:
                key.colour = value
            self.update()
        else:
            raise TypeError('colour must be an RGB object')
        
    @colour.deleter
    def colour(self):
        raise AttributeError('Do not delete colour')  

    @property
    def default_brightness(self):
        """ The default brightness of the board, regardless of what the current brightness is set """
        return self._default_brightness
    
    @default_brightness.setter
    def default_brightness(self, value):
        if isinstance(value, float):
           if 0 <= value <= 1:
               self._default_brightness = value
           else:
               raise ValueError('default_brightness must be between 0.0 and 1.0 inclusive')
        else:
           raise TypeError('default_brightness must be a float')
        
    @default_brightness.deleter
    def default_brightness(self):
        raise AttributeError('Do note delete default_brightness')

    @property
    def brightness(self):
        """ The current brightness of the keypad """
        return self._brightness
    
    @brightness.setter
    def brightness(self, value):
        if isinstance(value, float):
            if 0 <= value <= 1:
                self._brightness = value
                for key in self.keys:
                    key.brightness = value
                self.update()
            else:
                raise ValueError('brightness must be between 0.0 and 1.0 inclusive')
        else:
            raise TypeError('brightness must be a float')
        
    @brightness.deleter
    def brightness(self):
        raise AttributeError('Do note delete brightness')

    @property
    def is_toggled_on(self):
        """ If the current state of the board is toggled on or not """
        return self._is_toggled_on
    
    @is_toggled_on.setter
    def is_toggled_on(self, value):
        if isinstance(value, bool):
            self._is_toggled_on = value
        else:
            raise TypeError('is_toggled_on must be a boolean')
        
    @is_toggled_on.deleter
    def is_toggled_on(self):
        raise AttributeError('Do not delete, is_toggled_on should be false as a default value')

    @property
    def toggled_key(self):
        """ The coordinates of the key that is currently toggled on """
        return self._toggled_key
    
    @toggled_key.setter
    def toggled_key(self, value):
        if isinstance(value, tuple) or value is None:
            self._toggled_key = value
        else:
            raise TypeError('toggled_key must be a tuple')
        
    @toggled_key.deleter
    def toggled_key(self):
        raise AttributeError('Do not delete toggled_key')

    def load_config(self):
        """ Open config.json file and extract data """
        with open('config.json') as file:
            return json.load(file)

    def set_key_config(self):
        """ Populate keys with commands from configuration """
        config_object = self._config['config']            
        
        # Iterate through configured keys
        for button_object in config_object:
            key = self.get_key(button_object['x'], button_object['y'])
            colour = button_object['colour']
            key.master_colour = RGB(colour['red'], colour['green'], colour['blue'])
            key.is_programmed = True
            
            # Populate the key's commands
            for command_object in button_object['commands']:
                command = KeypadCommand()                 
                for action_object in command_object:
                    command.actions.append(KeypadAction(action_object['actionType'], action_object['action']))                    
                key.commands.append(command)            

    def load_pressed_keys(self):
        """ Reads and updates the current state of each key, and returns a list """
        with self._device:
            
            # Read from IO expander, 2 bytes (8 bits) correspond to the 16 buttons
            self._device.write(bytes([0x0]))
            result = bytearray(2)
            self._device.readinto(result)
            b = result[0] | result[1] << 8
            
            # Iterate each key and update
            for index, key in enumerate(self.keys):
                if not (1 << index) & b:                    
                    if key.is_pressed:
                        key.still_pressed = True
                    else:
                        key.still_pressed = False                        
                    key.is_pressed = True
                else:
                    key.still_pressed = False
                    key.is_pressed = False                    
            return self.keys

    def toggle_on(self, key, colour=None, brightness=None):
        """ Updates board to reflect the toggled, and programmed, keys """
        if colour is None:
            colour = self.default_colour
        if brightness is None:
            brightness = self.default_brightness        
        key.colour = colour
        key.brightness = brightness
        key.is_toggled_on = True
        
        self.is_toggled_on = True
        self.toggled_key = key.coordinates        
        
        # Update keys
        number_of_commands = len(key.commands)
        current_key_index = self.coordinates_to_index(key.x, key.y)
        if number_of_commands > current_key_index:
            number_of_commands += 1        
        self.keys[current_key_index].colour = key.master_colour 
        for key_index in range(16):
            if key_index != current_key_index:
                if key_index < number_of_commands:
                    self.keys[key_index].colour = key.master_colour
                else:
                    self.keys[key_index].colour = self.default_colour
        self.update()

    def run_command(self, key):
        """ Extracts and runs the command associated with given key's index """
        toggled_key_coordinates = self.toggled_key
        toggled_key = self.get_key(toggled_key_coordinates[0], toggled_key_coordinates[1])        
        current_key_index = key.index
        toggled_key_index = toggled_key.index        
        
        if current_key_index > toggled_key_index:
            current_key_index -= 1
        if current_key_index < len(toggled_key.commands):
            self.execute(toggled_key.commands[current_key_index])

    def execute(self, command):
        """ Executes the given command """
        for command_action in command.actions:
            
            if command_action.action_type == 'keyboardShortcut':
                if len(command_action.action) == 1:
                    self.enter_keyboard_shortcut(self.keycode_dictionary[command_action.action[0]])    
                elif len(command_action.action) == 2:
                    self.enter_keyboard_shortcut(self.keycode_dictionary[command_action.action[0]], self.keycode_dictionary[command_action.action[1]])
                elif len(command_action.action) == 3:
                    self.enter_keyboard_shortcut(self.keycode_dictionary[command_action.action[0]], self.keycode_dictionary[command_action.action[1]], self.keycode_dictionary[command_action.action[2]])                
            
            elif command_action.action_type == 'enterText':
               self.enter_text(command_action.action)

    def reset(self):
        """ Resets the board, including keys, to default values """
        self._colour = self.default_colour
        self._brightness = self.default_brightness
        self.is_toggled_on = False
        self.toggled_key = None
        for key in self.keys:
            key.colour = key.master_colour
            key.brightness = self.brightness
            key.is_toggled_on = False
        self.update()

    def clear(self):
        """ Clears the board, including keys, to blank values """
        self._colour = RGB(0, 0, 0)
        self._brightness = 0.5
        self.is_toggled_on = False
        self.toggled_key = None
        for key in self.keys:
            key.colour = RGB(0, 0, 0)
            key.brightness = 0.0
            key.is_toggled_on = False
        self.update()

    def get_key(self, x, y):
        """ Returns the key found at the given coordinates """
        key_index = self.coordinates_to_index(x, y)
        return self.keys[key_index]

    def coordinates_to_index(self, x, y):
        """ Takes a pair of coordinates and converts then to a single index value """
        return x * 4 + y

    def update(self):
        """ Takes the colour and brightness value of each key and updates the physical board """
        for key_index, key in enumerate(self.keys):
            self._pixels[key_index] = (key.pixel_tuple)

    def enter_keyboard_shortcut(self, input_one, input_two=None, input_three=None):
        """ Takes in input keycodes, and sends the commands """
        if input_two is not None and input_three is not None:
            self._kbd.send(input_one, input_two, input_three)            
        elif input_two is not None and input_three is None:
            self._kbd.send(input_one, input_two)            
        else:
            self._kbd.send(input_one)            
        time.sleep(1)

    def enter_text(self, input):
        """ Takes in text, and types it via the keyboard """
        self._layout.write(input)
        time.sleep(0.5)

    def load(self):
        """ Set up load animation from configuration """
        load_pattern = self.config['loadPattern']
        load_delay = self.config['loadPatternDelay']        
        if isinstance(load_pattern, str):
            self._pattern_load(self.default_colour, self.load_patterns[load_pattern], load_delay)
        else:
            self._pattern_load(self.default_colour, load_pattern, load_delay)

    def _pattern_load(self, colour, pattern, load_delay):
        """ Execute load pattern from given values """
        self.colour = RGB(0, 0, 0)
        self.default_colour = colour
        for key_index in pattern:
            self.keys[key_index].fade_to_colour(colour)
            time.sleep(load_delay)
        self.reset()


"""
KeypadKey
================================================================================
Provides functionality to an individual key on a Pimoroni keypad
"""

class KeypadKey():
    """ A key found on a Pimoroni keypad """
    
    def __init__(self, keypad, x, y, colour=None, brightness=0.5, master_colour=None):
        """
        A key found on a Pimoroni keypad. Initialization sets the following properties:
        - x
        - y
        - keypad
        - colour
        - master_colour
        - brightness
        - is_toggled_on
        - is_pressed
        - still_pressed
        - is_programmed
        - commands
        """
        self.x = x
        self.y = y
        self.keypad = keypad
        self.colour = colour
        self.master_colour = colour
        self.brightness = brightness
        self.is_toggled_on = False
        self.is_pressed = False
        self.still_pressed = False
        self.is_programmed = False        
        self.commands = []

    @property
    def x(self):
        """ The x coordinate of the key """
        return self._x
    
    @x.setter
    def x(self, value):
        if isinstance(value, int):
            if 0 <= value <= 15:
                self._x = value
            else:
                raise ValueError('x must be an integer between 0 and 15 inclusive')
        else:
            raise TypeError('x must be an integer')
        
    @x.deleter
    def x(self):
        raise AttributeError('Do not delete x')

    @property
    def y(self):
        """ The y coordinate of the key """
        return self._y
    
    @y.setter
    def y(self, value):
        if isinstance(value, int):
            if 0 <= value <= 15:
                self._y = value
            else:
                raise ValueError('y must be an integer between 0 and 15 inclusive')
        else:
            raise TypeError('y must be an integer')
        
    @y.deleter
    def y(self):
        raise AttributeError('Do not delete y')

    @property
    def keypad(self):
        """ The keypad the key is attributed to """
        return self._keypad
    
    @keypad.setter
    def keypad(self, value):
        if isinstance(value, PimoroniKeypad):
            self._keypad = value
        else:
            raise TypeError('keypad must be a PimoroniKeypad object')
    
    @keypad.deleter
    def keypad(self):
        raise AttributeError('Do not delete keypad')

    @property
    def colour(self):
        """ The current colour of the key """
        return self._colour
    
    @colour.setter
    def colour(self, value):
        if isinstance(value, RGB) or value is None:            
            if value == None:
                self._colour = self.keypad.default_colour
            else:
                self._colour = value
        else:
            raise TypeError('colour must be an RGB object or None type')
        
    @colour.deleter
    def colour(self):
        raise AttributeError('Do not delete colour')

    @property
    def master_colour(self):
        """ The master colour of the key used with toggle behaviour """
        return self._master_colour
    
    @master_colour.setter
    def master_colour(self, value):
        if value is None:
            self._master_colour = self.colour
        elif isinstance(value, RGB):
            self._master_colour = value
        else:
            raise TypeError('colour must be an RGB object or None type')

    @master_colour.deleter
    def master_colour(self):
        raise AttributeError('Do not delete master_colour')

    @property
    def brightness(self):
        """ The brightness of the key"""
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        if isinstance(value, float):
           if 0 <= value <= 1:
               self._brightness = value
           else:
               raise ValueError('brightness must be between 0.0 and 1.0 inclusive')
        else:
           raise TypeError('brightness must be a float')

    @brightness.deleter
    def brightness(self):
        raise AttributeError('Do note delete brightness')

    @property
    def is_toggled_on(self):
        """ Whether the key is currently toggled on or not """
        return self._is_toggled_on

    @is_toggled_on.setter
    def is_toggled_on(self, value):
        if isinstance(value, bool):
            self._is_toggled_on = value
        else:
            raise TypeError('is_toggled_on must be a boolean')

    @is_toggled_on.deleter
    def is_toggled_on(self):
        raise AttributeError('Do not delete, is_toggled_on should be false as a default value')

    @property
    def is_pressed(self):
        """ Whether the key is currently pressed or not """
        return self._is_pressed
    
    @is_pressed.setter
    def is_pressed(self, value):
        if isinstance(value, bool):       
            self._is_pressed = value
        else:
            raise TypeError('is_pressed must be a boolean')

    @is_pressed.deleter
    def is_pressed(self):
        raise AttributeError('Do not delete, is_pressed should be false as a default value')

    @property
    def still_pressed(self):
        """ Whether the key remains pressed down since is_pressed was last updated """
        return self._still_pressed
    
    @still_pressed.setter
    def still_pressed(self, value):
        if isinstance(value, bool):
            self._still_pressed = value
        else:
            raise TypeError('still_pressed must be a boolean')
        
    @still_pressed.deleter
    def still_pressed(self):
        raise AttributeError('Do not delete, still_pressed should be false as a default value')

    @property
    def is_programmed(self):
        """ Whether the key has been programmed with commands from the configuration """
        return self._is_programmed
    
    @is_programmed.setter
    def is_programmed(self, value):
        if isinstance(value, bool):
            self._is_programmed = value
        else:
            raise TypeError('is_programmed must be a boolean')
        
    @is_programmed.deleter
    def is_programmed(self):
        raise AttributeError('Do not delete, is_programmed should be false as a default value')

    @property
    def commands(self):
        """ The programmed commands linked to the key """
        return self._commands
    
    @commands.setter
    def commands(self, value):
        if isinstance(value, list):
            self._commands = value
        else:
            raise TypeError('commands must be an list array')
    
    @commands.deleter
    def commands(self):
        raise AttributeError('Do not delete commands')

    @property
    def pixel_tuple(self):
        """ The colour and brightness values used to update the key on the keypad, represented as a tuple (red, green, blue, brightness) """
        return self.colour.red, self.colour.green, self.colour.blue, self.brightness

    @property    
    def coordinates(self):
        """ The coordinates of the key, represented as a tuple (x, y) """
        return self.x, self.y

    @property
    def index(self):
        """ The index of the key between 0-15, derived from the key's coordinates """
        return self.x * 4 + self.y
     
    def reset(self):
        """ Reset the key back to it's default values and updates the keypad """
        self.colour = self.keypad.default_colour
        self.brightness = self.keypad.default_brightness
        self.is_toggled_on = False
        self.keypad.update()

    def fade_to_colour(self, colour):
        """ Fades the colour of the key from the current colour to the given colour """
        current_colour = self.colour        
        for n in range(0, 100, 4):
            r = int(self._map(n, 0, 100, current_colour.red, colour.red))
            g = int(self._map(n, 0, 100, current_colour.green, colour.green))
            b = int(self._map(n, 0, 100, current_colour.blue, colour.blue))
            self.colour = RGB(r,g,b)
            self.keypad.update()

    def _map(self, value, in_min, in_max, out_min, out_max):
        """ Maps the given value between two sets of values and scales the result """
        return int((value-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)


"""
KeypadCommand
================================================================================
A class representing the commands assigned to a Pimoroni keypad key
"""

class KeypadCommand():
    """ The command linked to a Pimoroni keypad key """
    
    def __init__(self):
        """ 
        The command linked to a Pimoroni keypad key. Initialization sets following property:
        - actions
        """
        self.actions = []

    @property
    def actions(self):
        """ The list of actions that make up the command"""
        return self._actions
    
    @actions.setter
    def actions(self, value):
        if isinstance(value, list):
            self._actions = value
        else:
            raise TypeError('actions must be a list array')
        
    @actions.deleter
    def actions(self):
        raise AttributeError('Do not delete actions')


"""
KeypadAction
================================================================================
A class representing the actions that make up the command assigned to a 
Pimoroni keypad key
"""

class KeypadAction():
    """ An action that makes up the command linked with a Pimoroni keypad key """
    
    def __init__(self, action_type, action):
        """ An action that makes up the command linked with a Pimoroni keypad key. Initialization sets the following properties:
        - action_type
        - action
        """
        self.action_type = action_type
        self.action = action

    @property
    def action_type(self):
        """ The type of the action, either 'keyboardShortcut' or 'enterText' """
        return self._action_type
    
    @action_type.setter
    def action_type(self, value):
        if isinstance(value, str):
            self._action_type = value
        else:
            raise TypeError('action_type must be a string')
        
    @action_type.deleter
    def action_type(self):
        raise AttributeError('Do not delete action_type')

    @property
    def action(self):
        """ The actual action to be executed """
        return self._action
    
    @action.setter
    def action(self, value):
        if isinstance(value, str) or isinstance(value, list):
            self._action = value
        else:
            raise TypeError('action must be a string or list')
 
    @action.deleter
    def action(self):
        raise AttributeError('Do not delete action')


"""
RGB
================================================================================
A class to store RGB colour values
"""

class RGB():
    """ A colour represented as seperate red, blue, and green values """
    
    def __init__(self, R=None, G=None, B=None):
        """ A colour represented as seperate red, blue, and green values: Initialization sets the following properties:
        - red
        - green
        - blue
        """
        if R is None:
            R = 0
        if G is None:
            G = 0
        if B is None: 
            B = 0
        self.red = R
        self.green = G
        self.blue = B
    
    @property
    def value(self):
        """ The colour represented as a tuple (red, green, blue) """
        return self.red, self.green, self.blue

    @value.setter
    def value(self,R=None, G=None, B=None):
        if R is None:
            R = 0
        if G is None:
            G = 0
        if B is None: 
            B = 0
        self.red = R
        self.green = G
        self.blue = B 
    
    def show(self):
        """ Prints the red, green, and blue values of the colour """
        print("R:", self.red)
        print("G:", self.green)
        print("B:", self.blue)