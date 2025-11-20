# Getting started — Raspberry Pi Pico with Thonny + MicroPython

Short step-by-step guide to flash MicroPython and run code on a Raspberry Pi Pico using Thonny.

## Requirements
- Raspberry Pi Pico (or Pico W)
- USB A/C-to-microB cable (data-capable)
- Desktop OS: Windows / macOS / Linux
- Thonny IDE (latest)

## Install Thonny
- Windows / macOS: download and install from https://thonny.org
- Linux: install from your distro packages or `pip3 install thonny` / snap if available

## Flash MicroPython firmware
Method A — automatic (recommended)
1. Open Thonny.
2. Tools → Options → Interpreter.
3. Select "MicroPython (Raspberry Pi Pico)" and click "Install or update firmware". Follow prompts.

Method B — manual
1. Put Pico into bootloader: hold BOOTSEL button while plugging the Pico into USB. It appears as a mass-storage device.
2. Download the latest `rp2-pico-*.uf2` from the MicroPython downloads page.
3. Drag-and-drop the `.uf2` file onto the Pico drive. Pico will reboot with MicroPython.

## Configure Thonny to use the Pico
1. In Thonny: Tools → Options → Interpreter.
2. Choose "MicroPython (Raspberry Pi Pico)".
3. Select the correct port if needed (Thonny usually auto-detects).
4. Open the REPL (bottom panel shows >>>).

## First program — blink the onboard LED
Write this in the editor:
```python
from machine import Pin
import time

led = Pin(25, Pin.OUT)   # onboard LED on GP25 for Pico
while True:
    led.toggle()
    time.sleep(0.5)
```
- Click "Run" (or Ctrl+R).
- To make it run automatically on boot: File → Save as... → Raspberry Pi Pico → save as `main.py`.

## Working with files and REPL
- Use the Files pane to upload, download, delete files on the device.
- REPL is interactive: type Python commands and see immediate results.
- To stop a running program: press the stop button in Thonny or press the Pico RUN button (if available).

## Adding libraries
- Pico has no network by default — copy pure-Python module files (`.py`) to the Pico via Thonny Files view.
- For compiled modules or packages, build them for rp2 or use prebuilt UF2/firmware that includes them.

## Tips & troubleshooting
- If Pico not detected: try a different USB cable (many are charge-only), different port, or hold BOOTSEL while plugging in.
- If Thonny shows unknown firmware, reinstall MicroPython firmware via Thonny or manual UF2.
- To enter the bootloader later: hold BOOTSEL and plug in or press BOOTSEL then reset.
- Use safe stopping: open REPL and press Ctrl+C to interrupt long-running loops.

## Next steps
- Explore GPIO, ADC, PWM, I2C, SPI with `machine` module.
- Try examples: reading a sensor, driving a servo, controlling LEDs/NeoPixels.
- If using Pico W, learn to use the `network`/`socket` modules for Wi‑Fi features.

That's it — Pico + Thonny + MicroPython ready for development.