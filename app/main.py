import machine, neopixel
import time, config
import urandom
import uos

# Number of LEDs
n = config.settings.get('numleds', 1)

# Pin where NeoPixels are connected
pin = config.settings.get('neopixel_pin', 5)

# Create a NeoPixel object
np = neopixel.NeoPixel(machine.Pin(pin), n)

# Setup the button
BUTTON_PIN = config.settings.get('button_pin', 13)
button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

# Define effects
def solid_color(np, color):
    for i in range(n):
        np[i] = color
    np.write()

def blink(np, color, delay):
    for i in range(n):
        np[i] = color
    np.write()
    time.sleep_ms(delay)
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()
    time.sleep_ms(delay)

def fade(np, color, steps, delay):
    for step in range(steps):
        for i in range(n):
            np[i] = (int(color[0] * step / steps), int(color[1] * step / steps), int(color[2] * step / steps))
        np.write()
        time.sleep_ms(delay)
    for step in range(steps, 0, -1):
        for i in range(n):
            np[i] = (int(color[0] * step / steps), int(color[1] * step / steps), int(color[2] * step / steps))
        np.write()
        time.sleep_ms(delay)

def candle_effect(np, base_color, flicker_intensity=30, delay=50):
    r, g, b = base_color
    for i in range(n):
        flicker_r = urandom.getrandbits(8) % flicker_intensity
        flicker_g = urandom.getrandbits(8) % flicker_intensity
        flicker_b = urandom.getrandbits(8) % flicker_intensity
        np[i] = (max(0, r - flicker_r), max(0, g - flicker_g), max(0, b - flicker_b))
    np.write()
    time.sleep_ms(delay)

def snow_effect(np, colors, delay=500):
    for i in range(n):
        color = colors[urandom.getrandbits(1)]
        np[i] = color
    np.write()
    time.sleep_ms(delay)

def wheel(pos):
    # Generate rainbow colors across 0-255 positions.
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

def rainbow(np, delay=20):
    for j in range(256):
        for i in range(n):
            np[i] = wheel(j & 255)
        np.write()
        time.sleep_ms(delay)

# Function to read the current effect from a file
def read_effect_from_file(filename):
    try:
        with open(filename, 'r') as file:
            return int(file.read())
    except:
        return 0  # Default to effect 0 if file doesn't exist or error occurs

# Function to write the current effect to a file
def write_effect_to_file(filename, effect):
    try:
        with open(filename, 'w') as file:
            file.write(str(effect))
    except:
        pass  # Fail silently if unable to write

# File to store the current effect
effect_file = 'current_effect.txt'

# Read the current effect from file, or default to 0
current_effect = read_effect_from_file(effect_file)

# Global variables
current_effect = read_effect_from_file(effect_file)
debounce_time_ms = 200  # Debounce time in milliseconds

# Last time the button was pressed
last_button_press_time = 0

# Button press detection with debounce
def button_pressed(pin):
    global current_effect, last_button_press_time
    current_time = time.ticks_ms()

    if time.ticks_diff(current_time, last_button_press_time) > debounce_time_ms:
        current_effect = (current_effect + 1) % 23  # Total number of effects
        write_effect_to_file(effect_file, current_effect)  # Save the new effect
        last_button_press_time = current_time

button.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_pressed)

def mainloop():
    # Main loop
    while True:
        if current_effect == 0:
            solid_color(np, (255, 0, 0))  # Example color: Red
        elif current_effect == 1:
            solid_color(np, (0, 255, 0))  #
        elif current_effect == 2:
            solid_color(np, (0, 0, 255))  #
        elif current_effect == 3:
            solid_color(np, (255, 255, 0))  #
        elif current_effect == 4:
            solid_color(np, (0, 255, 255))  #
        elif current_effect == 5:
            solid_color(np, (255, 0, 255))  #
        elif current_effect == 6:
            solid_color(np, (255, 255, 255))  #
            
        elif current_effect == 7:
            blink(np, (255, 0, 0), 500)  # Example color: Red
        elif current_effect == 8:
            blink(np, (0, 255, 0), 500)  #
        elif current_effect == 9:
            blink(np, (0, 0, 255), 500)  #
        elif current_effect == 10:
            blink(np, (255, 255, 0), 500)  #
        elif current_effect == 11:
            blink(np, (0, 255, 255), 500)  #
        elif current_effect == 12:
            blink(np, (255, 0, 255), 500)  #
        elif current_effect == 13:
            blink(np, (255, 255, 255), 500)  #
        
        elif current_effect == 14:
            fade(np, (255, 0, 0), 10, 50)  # Example color: Red
        elif current_effect == 15:
            fade(np, (0, 255, 0), 10, 50)  #
        elif current_effect == 16:
            fade(np, (0, 0, 255), 10, 50)  #
        elif current_effect == 17:
            fade(np, (255, 255, 0), 10, 50)  #
        elif current_effect == 18:
            fade(np, (0, 255, 255), 10, 50)  #
        elif current_effect == 19:
            fade(np, (255, 0, 255), 10, 50)  #
        elif current_effect == 20:
            fade(np, (255, 255, 255), 10, 50)  #
            
            
        elif current_effect == 21:
            candle_effect(np, (147, 255, 41), flicker_intensity=30, delay=50)
        elif current_effect == 22:
            snow_effect(np, [(0, 0, 255), (255, 255, 255)], delay=500)
        elif current_effect == 23:
            rainbow(np, delay=20)

mainloop()
