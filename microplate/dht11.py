from microplate.module import ModuleInterface
from machine import Pin
import dht
from microplate.message import Message


class DHT11(ModuleInterface):
    def __init__(self, pin, tick=2000):
      super().__init__(dht.DHT11(Pin(pin)), tick)
        
    def action(self):
        self.io.measure()
        message = Message()
        message.set(
          {
              "event": "dht.status",
              "parameters": {"temp": self.io.temperature(), "humi": self.io.humidity()},
          }
        )
        self.broadcast(message)
        if self.callback:
            self.callback('action', self.value())
      
    def value(self):
        return [self.io.temperature(), self.io.humidity()]
