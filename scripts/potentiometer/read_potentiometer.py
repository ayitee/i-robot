from machine import ADC
import time

pot_pin = 26
pot = ADC(pot_pin)

while True:
    pot_value = pot.read_u16()
    volt = round((3.3/65535)*pot_value,2)
    percent = int(pot_value/65535*100)
    print("Volt: "+str(volt)+" | Read value: "+str(pot_value)+" | percent: "+str(percent)+"%")
    time.sleep(1)


