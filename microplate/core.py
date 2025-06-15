from config import *
from node_config import *
from microplate.module import ModuleInterface
import time
import uasyncio

listener = None
home_assistant = None

if WIFI is not None:
    print("Initializing network")
    import microplate.wifi
    import socket

    microplate.wifi.wifi_connect()

    if USE_IOT_BROADCAST:
        print("Initializing IoTv1")
        from microplate.message import Message
        from microplate.listener import Listener
        from microplate.message_aes_sha1 import Cryptor
        import microplate.broadcast as broadcast
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
    else:
        print ("IoT protocol not initialized")

    if USE_HA:
        print("Initializing MQTT")
        from microplate.home_assistant import HomeAssistant
        home_assistant = HomeAssistant()

else:
    print("No network required")


workers = []

def add_handler(name, handler):
    if USE_IOT_BROADCAST:
        listener.add_handler(name, handler)
    else:
        print("Listener is not enabled")
    if USE_HA:
        home_assistant.add_handler(name, handler)


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
    if USE_HA:
        discovery_packet = home_assistant.discovery_packet()
        print(discovery_packet)
    l.run_forever()

l = uasyncio.get_event_loop()
l.create_task(main())
if USE_IOT_BROADCAST:
    l.create_task(listener.run())

