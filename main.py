from config import *
from node_config import *
import microplate.wifi

microplate.wifi.wifi_connect(WIFI)

from microplate.light import LightSensor
from microplate.hcs_sr501 import MoveSensor
from microplate.dht11 import DHT11
from microplate.message import Message
from microplate.module import ModuleInterface
from microplate.message_aes_sha1 import Cryptor
from microplate.listener import Listener
import time
import socket
import uasyncio

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

listener = Listener(s)


from machine import Pin
p = Pin(19, Pin.PULL_UP)
p.value(0)

p = Pin(18, Pin.PULL_UP)
p.value(0)

def debug_callback(name, data):
    pass
    print(name, data)


light = LightSensor(PIN_LIGHT)
light.callback = debug_callback

pir = MoveSensor(PIN_PIR)
temp = DHT11(PIN_DHT, 10000)

# message = Message()
# message.set({
#     'event': 'dht.status',
#     'parameters': {"humi": 35, "temp": 22},
#     'targets': ['ALL']
# })
# s.sendto(message.bytes(), ADDRESS)

async def main(socket):
    print("starting main loop")
    while True:
        start = time.ticks_ms()

        light.tick(TICK)
        pir.tick(TICK)
        temp.tick(TICK)

        calculated_tick = TICK - time.ticks_diff(time.ticks_ms(), start)
        if calculated_tick < 0.0:
            calculated_tick = 0
        await uasyncio.sleep_ms(calculated_tick)


l = uasyncio.get_event_loop()
l.create_task(main(s))
l.create_task(listener.run())

l.run_forever()
