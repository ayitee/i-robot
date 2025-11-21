from machine import Pin, PWM
from time import sleep

# --- BUZZER ---
buzzer = PWM(Pin(15))

# --- LED ---
led = Pin(25, Pin.OUT)

# --- BUTTONS (your new GPIO pins) ---
button_pins = [0, 4, 8, 12, 16, 20]
buttons = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in button_pins]

# --- FIRST 6 NOTES FROM YOUR tones DICT ---
tones = [
    262,  # C4
    294,  # D4
    330,  # E4
    349,  # F4
    392,  # G4
    440   # A4
]

# --- SOUND CONTROL ---
def play(freq):
    buzzer.freq(freq)
    buzzer.duty_u16(30000)
    led.on()

def stop():
    buzzer.duty_u16(0)
    led.off()

# --- MAIN LOOP ---
while True:
    played = False

    for i, btn in enumerate(buttons):
        if btn.value() == 0:     # Button pressed (active LOW)
            play(tones[i])
            played = True
            break

    if not played:
        stop()

    sleep(0.01)  # debounce