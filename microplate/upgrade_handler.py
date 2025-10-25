from microplate.handler_base import Handler
import json
import time
import machine


class UpgradeHandler(Handler):
    def __init__(self,):
        super().__init__()

    def handle(self, message):
        if message['event'] == "system.userspace.upgrade":
            print(message['parameters'])
            with open("/.upgrade.json", 'w') as f:
                json.dump(message['parameters'], f)
            time.sleep(3)
            print("Rebooting for the upgrade")
            machine.reset()

