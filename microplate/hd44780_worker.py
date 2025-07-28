from microplate.module import ModuleInterface
from machine import I2C
from microplate.charlcd_i2c_driver import CharLcdDriver
from microplate.charlcd_buffered import CharLCD
from microplate.message import Message
from microplate.broadcast import broadcast
from microplate.ha_base import HABase

#
# lcd_worker = HD44780Worker()
# lcd_worker.write(str(value[0]), 5, 0)
#

class HD44780Worker(ModuleInterface):
    def __init__(self, scl=22, sda=21, addr=None, tick=500):
        i2c = I2C(0, scl=scl, sda=sda)
        if addr is None:
            devices = i2c.scan()
            addr = devices[0]
        ModuleInterface.__init__(
            self,
            CharLCD(20, 4, CharLcdDriver(addr), 0, 0),
            tick
        )
        self.io.init()

    def action(self):
        self.io.flush()

    def write(self, content, pos_x=None, pos_y=None):
        self.io.write(content, pos_x, pos_y)

    def write_array(self, lines):
        pass
