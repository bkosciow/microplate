from config import *
from node_config import *
import microplate.wifi

microplate.wifi.wifi_connect(WIFI)

from microplate.light_worker import LightWorker
from microplate.hcs_sr501_worker import MoveWorker
from microplate.dht11_worker import DHT11Worker
from microplate.message import Message
from microplate.module import ModuleInterface
from microplate.message_aes_sha1 import Cryptor
from microplate.listener import Listener
from microplate.relay_hanlder import RelayHandler
from microplate.dht11_handler import Dht11Handler
from microplate.light_handler import LightHandler
from microplate.hcs_sr501_handler import MoveHandler
from microplate.button_worker import ButtonWorker
import time
import socket
import uasyncio
import microplate.broadcast as broadcast

Message.node_name = NODE_NAME
Message.add_decoder(Cryptor(STATICIV, IVKEY, DATAKEY, PASSPHRASE))
Message.add_encoder(Cryptor(STATICIV, IVKEY, DATAKEY, PASSPHRASE))

print("booting")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.setblocking(False)
s.bind((BROADCAST_IP, PORT))

ModuleInterface.socket = s
broadcast.socket = s

def debug_callback(name, data):
    pass
    print(name, data)


def click_callback(pin):
    print("pin : ", pin)

light = LightWorker(PIN_LIGHT)
light.callback = debug_callback

pir = MoveWorker(PIN_PIR)
temp = DHT11Worker(PIN_DHT, 3000)

btns = ButtonWorker()
btns.add_button(BTN_A, 400, click_callback)

listener = Listener(s)
listener.add_handler("relay", RelayHandler(RELAY))
listener.add_handler("dht11", Dht11Handler(temp))
listener.add_handler("light", LightHandler(light))
listener.add_handler("move", MoveHandler(pir))


async def main(socket):
    print("starting main loop")
    while True:
        start = time.ticks_ms()

        light.tick(TICK)
        pir.tick(TICK)
        temp.tick(TICK)
        btns.tick(TICK)

        calculated_tick = TICK - time.ticks_diff(time.ticks_ms(), start)
        if calculated_tick < 0.0:
            calculated_tick = 0
        await uasyncio.sleep_ms(calculated_tick)


l = uasyncio.get_event_loop()
l.create_task(main(s))
l.create_task(listener.run())

l.run_forever()
