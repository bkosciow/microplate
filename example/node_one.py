from config import *
import microplate.core as core

from microplate.light_worker import LightWorker
from microplate.hcs_sr501_worker import MoveWorker
from microplate.dht11_worker import DHT11Worker
from microplate.relay_hanlder import RelayHandler
from microplate.dht11_handler import Dht11Handler
from microplate.light_handler import LightHandler
from microplate.hcs_sr501_handler import MoveHandler
# from microplate.button_worker import ButtonWorker
# from microplate.debug_handler import DebugHandler
from microplate.network_worker import NetworkWorker

print("booting")


def debug_callback(name, data):
    pass
    print(name, data)


def click_callback(pin):
    print("pin : ", pin)


light = LightWorker(PIN_LIGHT)
light.callback = debug_callback
pir = MoveWorker(PIN_PIR)
temp = DHT11Worker(PIN_DHT, 3000)
# btns = ButtonWorker()
# btns.add_button(BTN_A, 400, click_callback)
net = NetworkWorker()

# core.add_worker(btns)
core.add_worker(light)
core.add_worker(pir)
core.add_worker(temp)
core.add_worker(net)

core.add_handler("relay", RelayHandler(RELAY))
core.add_handler("dht11", Dht11Handler(temp))
core.add_handler("light", LightHandler(light))
core.add_handler("move", MoveHandler(pir))
# core.add_handler("debug", DebugHandler())

core.start()
