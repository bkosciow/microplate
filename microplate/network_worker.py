from microplate.module import ModuleInterface
from microplate.wifi import wlan
from config import *
import microplate.wifi


class NetworkWorker(ModuleInterface):
    def __init__(self, tick=3000):
        super().__init__(None, tick)
        self.count = 0
        self.connecting = False

    def action(self):
        if self.connecting:
            return True
        if not wlan.isconnected():
            self.count += 1
        else:
            self.count = 0

        if self.count >= WIFI_TIMEOUT:
            self.connecting = True
            print("connection lost, reconnecting...")
            microplate.wifi.wifi_disconnect()
            microplate.wifi.wifi_connect()
            self.connecting = False
