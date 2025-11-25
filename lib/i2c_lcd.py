from machine import I2C
import time

class I2cLcd:
    def __init__(self, i2c, addr, num_lines, num_columns):
        self.i2c = i2c
        self.addr = addr
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.backlight = 0x08
        self.PCF_RS = 0x01
        self.PCF_EN = 0x04
        time.sleep(0.05)
        self.hal_write_command(0x33)
        self.hal_write_command(0x32)
        self.hal_write_command(0x28)
        self.hal_write_command(0x0C)
        self.hal_write_command(0x06)
        self.clear()

    def hal_write_command(self, cmd):
        self.hal_write_byte(cmd, 0)

    def hal_write_data(self, data):
        self.hal_write_byte(data, self.PCF_RS)

    def hal_write_byte(self, data, mode):
        high = mode | (data & 0xF0)
        low = mode | ((data << 4) & 0xF0)
        self.hal_write(high)
        self.hal_write(low)

    def hal_write(self, data):
        self.i2c.writeto(self.addr, bytes([data | self.backlight | self.PCF_EN]))
        self.i2c.writeto(self.addr, bytes([data | self.backlight]))
        time.sleep_us(50)

    def clear(self):
        self.hal_write_command(0x01)
        time.sleep(0.002)

    def move_to(self, col, row):
        row_offsets = [0x00, 0x40, 0x14, 0x54]
        self.hal_write_command(0x80 | (col + row_offsets[row]))

    def putstr(self, string):
        for c in string:
            self.hal_write_data(ord(c))

