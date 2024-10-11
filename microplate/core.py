from config import *
from node_config import *
import microplate.wifi
import socket

microplate.wifi.wifi_connect()

from microplate.message import Message
from microplate.module import ModuleInterface
from microplate.message_aes_sha1 import Cryptor
import microplate.broadcast as broadcast
from microplate.listener import Listener
import time
import uasyncio

Message.node_name = NODE_NAME
Message.add_decoder(Cryptor(STATICIV, IVKEY, DATAKEY, PASSPHRASE))
Message.add_encoder(Cryptor(STATICIV, IVKEY, DATAKEY, PASSPHRASE))

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((BROADCAST_IP, PORT))
s.setblocking(False)

ModuleInterface.socket = s
broadcast.socket = s

listener = Listener(s)

workers = []


def add_handler(name, handler):
    listener.add_handler(name, handler)


def add_worker(worker):
    workers.append(worker)


async def main():
    print("starting workers loop")
    while True:
        start = time.ticks_ms()
        for item in workers:
            try:
                item.tick(TICK)
            except Exception as e:
                print(type(item), str(e))

        calculated_tick = TICK - time.ticks_diff(time.ticks_ms(), start)
        if calculated_tick < 0.0:
            calculated_tick = 0
        await uasyncio.sleep_ms(calculated_tick)


def start():
    l.run_forever()


l = uasyncio.get_event_loop()
l.create_task(main())
l.create_task(listener.run())

