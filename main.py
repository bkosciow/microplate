from microplate.light import LightSensor
from microplate.hcs_sr501 import MoveSensor
from microplate.dht11 import DHT11
from microplate.message import Message
from microplate.module import ModuleInterface
import time
import socket
import microplate.wifi
from config import *
from node_config import *
import uasyncio

Message.node_name = NODE_NAME
microplate.wifi.wifi_connect(WIFI)

print("booting")

ip_address = '0.0.0.0'
port = 5053
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.setblocking(False)
s.bind((ip_address, port))

ModuleInterface.socket = s


def debug_callback(name, data):
    print(name, data)


light = LightSensor(PIN_LIGHT)
light.callback = debug_callback

pir = MoveSensor(PIN_PIR)
temp = DHT11(PIN_DHT, 10000)

def callback(data, addr):
    pass
    # print(data)


async def receive(socket):
    while True:
        try:
            data, addr = socket.recvfrom(1024)
            callback(data, addr)
        except OSError as e:
            if e.errno == 11:
                pass
        await uasyncio.sleep(0)


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
l.create_task(receive(s))

l.run_forever()

