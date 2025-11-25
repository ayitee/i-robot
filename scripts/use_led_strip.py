import time
import board
import neopixel

# --- CONFIG ---
NUM_LEDS = 8
PIN = board.GP0     # <-- change to your data pin

pixels = neopixel.NeoPixel(PIN, NUM_LEDS, brightness=0.3, auto_write=False)

# Convert wheel position (0-255) to RGB
def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

# Main moving rainbow
offset = 0
while True:
    for i in range(NUM_LEDS):
        pixel_index = (i * 256 // NUM_LEDS) + offset
        pixels[i] = wheel(pixel_index & 255)
    pixels.show()
    offset = (offset + 1) % 256
    time.sleep(0.01)   # lower = smoother