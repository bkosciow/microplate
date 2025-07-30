#
# displays data on lcd and broadcasts it
# callbacks displays data
# setting tick1 for constructor starts


from config import *
import microplate.core as core

from microplate.light_worker import LightWorker
from microplate.hcs_sr501_worker import MoveWorker
from microplate.dht11_worker import DHT11Worker
from microplate.relay_worker import RelayWorker
from microplate.relay_hanlder import RelayHandler
from microplate.dht11_handler import Dht11Handler
from microplate.light_handler import LightHandler
from microplate.hcs_sr501_handler import MoveHandler
from microplate.button_worker import ButtonWorker
# from microplate.debug_handler import DebugHandler
from microplate.network_worker import NetworkWorker
from microplate.button_handler import ButtonHandler
from microplate.hd44780_worker import HD44780Worker


print("booting")

# button callback
def click_callback(pin):
    print("pin : ", pin)
    s = relay_worker.get_statuses()
    lcd_worker.write(str(pin), 0, 3)
    if pin == BTN_A:
        if s[0] == 1:
            relay_worker.disable(0)
        else:
            relay_worker.enable(0)

# dht callback
def dht_callback(action, value):
    lcd_worker.write(str(value[0]), 5, 0)
    lcd_worker.write(str(value[1]), 15, 0)


def light_callback(action, value):
    lcd_worker.write('light' if value == 0 else ' dark', 15, 1)


def move_callback(action, value):
    lcd_worker.write('     ' if value == 0 else 'ALARM', 15, 3)


def relay_callback(action, value):
    lcd_worker.write('O' if value[0] == 0 else '*', 0, 1)


# workers
net = NetworkWorker()

# setting tick1 enables broadcasting oin change and each n microseconds
lcd_worker = HD44780Worker(tick1=10000)
light = LightWorker(PIN_LIGHT)
light.callback = light_callback
pir = MoveWorker(PIN_PIR)
pir.callback = move_callback
dht = DHT11Worker(PIN_DHT, 3000)
dht.callback = dht_callback
relay_worker = RelayWorker(RELAY)
relay_worker.callback = relay_callback

btns = ButtonWorker()
btns.add_button(BTN_A, 400, click_callback)
btns.add_button(BTN_B, 400, click_callback)

core.add_worker(btns)
core.add_worker(light)
core.add_worker(pir)
core.add_worker(dht)
core.add_worker(net)
core.add_worker(relay_worker)
core.add_worker(lcd_worker)

# handlers
core.add_handler("relay", RelayHandler(relay_worker))
core.add_handler("dht11", Dht11Handler(dht))
core.add_handler("light", LightHandler(light))
core.add_handler("move", MoveHandler(pir))
core.add_handler('button', ButtonHandler(btns))


lcd_worker.write("Temp", 0, 0)
lcd_worker.write("Humi", 10, 0)
lcd_worker.write("?", 0, 1)
# main loop
core.start()
