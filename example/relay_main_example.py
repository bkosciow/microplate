from config import *
import microplate.core as core

from microplate.relay_worker import RelayWorker
from microplate.relay_hanlder import RelayHandler
from microplate.button_worker import ButtonWorker
# from microplate.debug_handler import DebugHandler
from microplate.network_worker import NetworkWorker

print("booting")

relay_worker = RelayWorker(RELAY)
r = RelayHandler(relay_worker)

# callback for buttons to toggle relays
def click_callback(pin):
    rr = r.workers[0].relays[0]
    r.workers[0].toggle(0, not rr['current'])

# worker for buttons
btns = ButtonWorker()
btns.add_button(BTN_A, 400, click_callback)

# network keep alive
net = NetworkWorker()

# add workers to core
core.add_worker(relay_worker)
core.add_worker(btns)
core.add_worker(net)

# ad handler to core
core.add_handler("relay", r)

# start core
core.start()
