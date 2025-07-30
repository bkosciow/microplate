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

class HD44780Worker(ModuleInterface, HABase):
    def __init__(self, scl=22, sda=21, addr=None, tick=500, tick1=None):
        HABase.__init__(self)
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
        self.broadcast_change = False
        self.dirty = True
        self.ha_component[f"{self.base_id}-lcd{self.ha_idx}"] = {
            'p': 'text',
            'mode': 'text',
            'unique_id': f"{self.base_id}-lcd{self.ha_idx}",
            'state_topic': f"{self.base_topic}/lcd{self.ha_idx}/state",
            'command_topic': f"{self.base_topic}/lcd{self.ha_idx}/command",
        }
        if tick1 is not None:
            self.broadcast_change = True
            self.add_action(tick1, self.send_action)

    def action(self):
        self.io.flush()
        if self.dirty and self.broadcast_change:
            self.dirty = False
            self.send_message()

    def write(self, content, pos_x=None, pos_y=None):
        self.io.write(content, pos_x, pos_y)
        self.dirty = True

    def write_array(self, lines):
        pass

    def send_action(self):
        self.send_message()

    def send_message(self):
        message = Message()
        message.set(
            {
                "event": "lcd.content",
                "parameters": self.io.screen
            }
        )
        broadcast(message)
        self.publish("\n".join(self.io.screen))
