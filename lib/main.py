from machine import I2C, Pin
from i2c_lcd import I2cLcd
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)
lcd.clear()
lcd.putstr("jeremy rajoeliarevony")