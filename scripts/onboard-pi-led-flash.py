import machine #library for hardware; allows us to access pins

import time #for delays

redLed = machine.Pin(2, machine.Pin.OUT) #initialize GPIO 1 as output for red LED

while (1): #infinite loop; runs until manually stopped

    redLed.toggle() #if LED is on, turn off. Else, turn on.

    time.sleep(.5) #pause for 1/2 second
