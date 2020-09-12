"""
Tracker for activity.
"""

import time
import board
import random
import digitalio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

import button

displayio.release_displays()

i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

messages_yay = [
    "Nice!",
    "Good job!",
    "Great!",
    "Way to go!",
    "Fantastic!",
    "Wonderful!",
]
messages_nay = [
    "Next time!",
    "It's okay.",
    "You'll get it.",
    "Keep trying!",
]
n_yay = 0
n_nay = 0
ping_mode = 0
ping_x, ping_y = 0, 0

button_a = button.Button(board.D9, digitalio.Pull.UP)
button_b = button.Button(board.D6, digitalio.Pull.UP)
button_c = button.Button(board.D5, digitalio.Pull.UP)

# Make the display context
splash = displayio.Group(max_size=10)
display.show(splash)

# Fill with white
color_bitmap = displayio.Bitmap(128, 32, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(118, 24, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=4)
splash.append(inner_sprite)

# Draw moving rectangle
ping_bitmap = displayio.Bitmap(5, 4, 1)
ping_palette = displayio.Palette(1)
ping_palette[0] = 0x000000  # Black
ping_sprite = displayio.TileGrid(ping_bitmap, pixel_shader=ping_palette, x=0, y=0)
splash.append(ping_sprite)

# Draw a label
text = "The YAY Tracker"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=15, y=15)
splash.append(text_area)

# Blackout sprite
blackout_bitmap = displayio.Bitmap(128, 32, 1)
blackout_palette = displayio.Palette(1)
blackout_palette[0] = 0x000000  # Black
blackout = displayio.TileGrid(blackout_bitmap, pixel_shader=blackout_palette, x=0, y=0)

in_blackout = False
start_time = time.monotonic()

while True:
    # Check for user interaction
    button_a.update()
    button_b.update()
    button_c.update()

    if not in_blackout and ((time.monotonic() - start_time) > 10):
        splash.append(blackout)
        in_blackout = True

    if button_a.just_pressed():
        if in_blackout:
            splash.pop()
            in_blackout = False
            start_time = time.monotonic()
        n_yay += 1
        message_index = random.randrange(0, len(messages_yay))
        message = messages_yay[message_index]
        splash[-1] = label.Label(terminalio.FONT, text=message, color=0xFFFF00, x=15, y=15)

    if button_b.just_pressed():
        if in_blackout:
            splash.pop()
            in_blackout = False
            start_time = time.monotonic()
        message = "Yays: " + str(n_yay) + "  Nays: " + str(n_nay)
        splash[-1] = label.Label(terminalio.FONT, text=message, color=0xFFFF00, x=15, y=15)

    if button_c.just_pressed():
        if in_blackout:
            splash.pop()
            in_blackout = False
            start_time = time.monotonic()
        n_nay += 1
        message_index = random.randrange(0, len(messages_nay))
        message = messages_nay[message_index]
        splash[-1] = label.Label(terminalio.FONT, text=message, color=0xFFFF00, x=15, y=15)

    # Move the ping sprite
    if ping_mode == 0:
        ping_x += 1
        if ping_x >= 128 - 5:
            ping_mode += 1
    elif ping_mode == 1:
        ping_y += 1
        if ping_y >= 32 - 4:
            ping_mode += 1
    elif ping_mode == 2:
        ping_x -= 1
        if ping_x <= 0:
            ping_mode += 1
    elif ping_mode == 3:
        ping_y -= 1
        if ping_y <= 0:
            ping_mode += 1
    else:
        print("whoops - check ping mode...")
    ping_mode %= 4

    ping_sprite = displayio.TileGrid(ping_bitmap, pixel_shader=ping_palette, x=ping_x, y=ping_y)
    splash[-2] = ping_sprite

    time.sleep(0.05)
