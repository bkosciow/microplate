from machine import Pin


class ButtonWorker:
    def __init__(self):
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
