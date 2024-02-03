from microplate.module import ModuleInterface
from microplate.wifi import wlan


class NetworkWorker(ModuleInterface):
    def __init__(self, tick=3000):
        super().__init__(None, tick)

    def action(self):
        print("wlan status: ", wlan.status())
