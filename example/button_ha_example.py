from config import *
import microplate.core as core

from microplate.button_worker import ButtonWorker
from microplate.network_worker import NetworkWorker
from microplate.button_handler import ButtonHandler

print("booting")

def click_callback(pin):
    print("pin : ", pin)
    s = relay_worker.get_statuses()
    if pin == BTN_A:
        if s[0] == 1:
            relay_worker.disable(0)
        else:
            relay_worker.enable(0)
    #
    # if pin == BTN_B:
    #     if s[1] == 1:
    #         relay_worker.disable(0)
    #     else:
    #         relay_worker.enable(0)

net = NetworkWorker()

btns = ButtonWorker()
btns.add_button(BTN_A, 400, click_callback)
btns.add_button(BTN_B, 400, click_callback)


core.add_worker(btns)
core.add_worker(net)

core.add_handler('button', ButtonHandler(btns))

core.start()
