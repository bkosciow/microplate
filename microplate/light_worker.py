from microplate.module import ModuleInterface
from machine import Pin
from microplate.message import Message
from microplate.broadcast import broadcast

#
# def debug_callback(name, data):
#     print(name, data)
# light = LightSensor(PIN_LIGHT)
# light.callback = debug_callback
#


class LightWorker(ModuleInterface):
    def __init__(self, pin, tick=200, tick1=10000):
        super().__init__(Pin(pin, Pin.IN), tick)
        self.light = None
        self.add_action(tick1, self.send_action)

    def action(self):
        self.data = self.io.value()
        if self.light != self.data:
            self.send_message()
            self.light = self.data
            if self.callback:
                self.callback('action', self.data)

    def send_action(self):
        self.send_message()
        if self.callback:
            self.callback('send_action', self.data)

    def send_message(self):
        message = Message()
        message.set(
            {
                "event": "detect.light" if self.data == 0 else "detect.dark",
            }
        )
        broadcast(message)
