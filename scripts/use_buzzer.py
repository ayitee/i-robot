import time
import board
import pwmio

# ---- BUZZER on GP22 (variable frequency ENABLED!) ----
buzzer = pwmio.PWMOut(
    board.GP22,
    duty_cycle=0,
    frequency=440,
    variable_frequency=True  # <-- REQUIRED to change pitch
)

# ---- NOTES ----
NOTE_C4  = 262
NOTE_D4  = 294
NOTE_E4  = 330
NOTE_F4  = 349
NOTE_G4  = 392
NOTE_A4  = 440
NOTE_B4  = 494
NOTE_C5  = 523

# ---- SIMPLE MELODY ----
melody = [
    NOTE_C4, NOTE_D4, NOTE_E4, NOTE_C4,
    NOTE_C4, NOTE_D4, NOTE_E4, NOTE_C4,
    NOTE_E4, NOTE_F4, NOTE_G4,
    NOTE_E4, NOTE_F4, NOTE_G4,
]

durations = [
    0.2, 0.2, 0.2, 0.2,
    0.2, 0.2, 0.2, 0.2,
    0.2, 0.2, 0.4,
    0.2, 0.2, 0.4,
]

# ---- PLAY MELODY ----
for i, note in enumerate(melody):
    buzzer.frequency = note
    buzzer.duty_cycle = 32768  # 50% volume
    time.sleep(durations[i])
    buzzer.duty_cycle = 0
    time.sleep(0.05)

# turn off
buzzer.duty_cycle = 0