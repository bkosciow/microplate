from microplate.module import ModuleInterface
from machine import Pin
import dht
from microplate.message import Message
from microplate.broadcast import broadcast
from microplate.ha_base import HABase

#
# temp = DHT11(PIN_DHT, 3000)
#


class DHT11Worker(ModuleInterface, HABase):
    def __init__(self, pin, tick=10000):
        ModuleInterface.__init__(self,dht.DHT11(Pin(pin)), tick)
        HABase.__init__(self)
        self.ha_component[f"{self.base_id}-temperature{self.ha_idx}"] = {
            'p': 'sensor',
            'device_class': 'temperature',
            'unit_of_measurement': "°C",
            'value_template': "{{ value_json.temp }}",
            'unique_id': f"{self.base_id}-temperature{self.ha_idx}",
            'state_topic': f"{self.base_topic}/temperature{self.ha_idx}/state",
        }
        self.ha_component[f"{self.base_id}-humidity{self.ha_idx}"] = {
            'p': 'sensor',
            'device_class': 'humidity',
            'unit_of_measurement': "%",
            'value_template': "{{ value_json.humi }}",
            'unique_id': f"{self.base_id}-humidity{self.ha_idx}",
            'state_topic': f"{self.base_topic}/temperature{self.ha_idx}/state",
        }

    def action(self):
        self.io.measure()
        self.send_message()
        if self.callback:
            self.callback('action', self.value())

    def send_message(self):
        ret = {"temp": self.io.temperature(), "humi": self.io.humidity()}
        message = Message()
        message.set(
            {
                "event": "dht.status",
                "parameters": ret,
            }
        )
        broadcast(message)
        self.publish(ret)

    def value(self):
        return [self.io.temperature(), self.io.humidity()]
