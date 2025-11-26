import board
import busio
import time
from adafruit_mcp230xx.mcp23008 import MCP23008
from adafruit_character_lcd.character_lcd_i2c import Character_LCD_I2C

i2c = busio.I2C(board.GP1, board.GP0)  # SCL, SDA

mcp = MCP23008(i2c, address=0x20)

lcd_columns = 16
lcd_rows = 2

lcd = Character_LCD_I2C(i2c, lcd_columns, lcd_rows, mcp=mcp)

lcd.message = "Hello, World!"
time.sleep(2)

lcd.clear()
lcd.message = "IIC 1602 Ready"