from machine import I2C
import time


class CharLcdDriver :
    def __init__(self, addr, bus=0, sda=21, scl=22):
        self.bus = I2C(bus, scl=scl, sda=sda)
        self.addr = addr
        self.mode = 4
        self.pins = {
            'RS': 0,
            'E': 2,
            'E2': None,
            'DB4': 4,
            'DB5': 5,
            'DB6': 6,
            'DB7': 7,
            'RW': 1,
            'BT': 3,
        }

        self.char_buffer = None
        self.initialized = False

    def init(self):
        """recalculate pins to values"""
        if self.initialized:
            return
        pins = {}
        for k in self.pins:
            if self.pins[k] is not None:
                pins[k] = int(pow(2, self.pins[k]))
        self.pins = pins
        self.initialized = True

    def get_line_address(self, idx):
        return [
            0x80,
            0xC0,
            0x94,
            0xD4
        ][idx]

    def shutdown(self):
        pass

    def cmd(self, char, enable=0):
        if self.mode == 8:
            self.prepare_send((char << 4) & 0xF0, enable)
        else:
            self.prepare_send(char & 0xF0, enable)
            self.prepare_send((char << 4) & 0xF0, enable)

    def shutdown(self):
        pass

    def prepare_send(self, char, enable=0):
        self.char_buffer = char | self.pins['BT']
        self.send(enable)

    def send(self, enable=0):
        if enable == 0:
            pin = self.pins['E']
        elif enable == 1:
            pin = self.pins['E2']

        if pin is None:
            raise IndexError("Wrong enable index")
        self.write(self.char_buffer | pin)
        time.sleep(0.005)
        self.write(self.char_buffer & (0xFF - pin))

    def write(self, char, enable=0):
        self.bus.writeto(
            self.addr,
            bytearray([char])
        )

    def char(self, char, enable=0):
        char = ord(char)
        if self.mode == 8:
            self.prepare_send(self.pins['RS'] | (char & 0x0F), enable)
        else:
            self.prepare_send((char & 0xF0) | self.pins['RS'], enable)
            self.prepare_send(((char << 4) & 0xF0) | self.pins['RS'], enable)

    def set_mode(self, mode):
        self.mode = mode
