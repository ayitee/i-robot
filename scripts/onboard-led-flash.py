from machine import Pin
import time

led = Pin(25, Pin.OUT)   # onboard LED on GP25 for Pico
while True:
    led.toggle()
    time.sleep(0.5)
