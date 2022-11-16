from PimoroniKeypad import PimoroniKeypad

keypad = PimoroniKeypad()

while True:
        
    for key in keypad.load_pressed_keys():                
        if key.is_pressed and not key.still_pressed:
            
            if keypad.is_toggled_on and not key.is_toggled_on:
                keypad.run_command(key)
            
            elif key.is_toggled_on:
                keypad.clear()
                
            elif key.is_programmed:
                keypad.toggle_on(key, brightness=1.0)