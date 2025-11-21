from machine import Pin, PWM
from machine import ADC
import time

buzzer = PWM(Pin(15))
pot_pin = 26
pot = ADC(pot_pin)

while True:
    pot_value = pot.read_u16()
    volt = round((3.3/65535)*pot_value,2)
    percent = int(pot_value/65535*100)
    print("Volt: "+str(volt)+" | Read value: "+str(pot_value)+" | percent: "+str(percent)+"%")
    time.sleep(0.1)
    buzzer.freq(percent*100)
    buzzer.duty_u16(3000)

buzzer.duty_u16(0)