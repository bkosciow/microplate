from machine import Pin
from microplate.ha_base import HABase


class ButtonWorker(HABase):
    def __init__(self):
        HABase.__init__(self)
        self.btns = []

    def add_button(self, pin, tick, callback):
        self.btns.append({
            'id': pin, 'pin': Pin(pin, Pin.IN, Pin.PULL_UP), 'tick': tick, 'counter': 0, 'callback': callback
        })

    def tick(self, dt):
        for item in self.btns:
            if item["pin"].value() == 0:
                item["counter"] += dt
                if item["counter"] >= item["tick"]:
                    item["counter"] = 0
                    item["callback"](item["id"])

    def click(self, idx):
        if idx < len(self.btns):
            item = self.btns[idx]
            item["callback"](item["id"])

    def get_ha_definition(self):
        for i in range(0, len(self.btns)):
            self.ha_component[f"{self.base_id}-button{self.ha_idx+i}"] = {
                'p': 'button',
                'unique_id': f"{self.base_id}-button{self.ha_idx+i}",
                'command_topic': f"{self.base_topic}/button{self.ha_idx}/command",
                'payload_on': '1',
                "command_template": "["+str(i)+"]",
            }

        return self.ha_component