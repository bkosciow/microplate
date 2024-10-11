from microplate.module import ModuleInterface
from machine import Pin
import dht
from microplate.message import Message
from microplate.broadcast import broadcast

#
# temp = DHT11(PIN_DHT, 3000)
#


class DHT11Worker(ModuleInterface):
    def __init__(self, pin, tick=2000):
        super().__init__(dht.DHT11(Pin(pin)), tick)

    def action(self):
        self.io.measure()
        self.send_message()
        if self.callback:
            self.callback('action', self.value())

    def send_message(self):
        message = Message()
        message.set(
            {
                "event": "dht.status",
                "parameters": {"temp": self.io.temperature(), "humi": self.io.humidity()},
            }
        )
        broadcast(message)

    def value(self):
        return [self.io.temperature(), self.io.humidity()]
