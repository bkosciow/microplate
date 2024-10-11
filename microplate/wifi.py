import time
from config import *

# 200: BEACON_TIMEOUT
# 201: NO_AP_FOUND
# 202: WRONG_PASSWORD
# 203: ASSOC_FAIL
# 204: HANDSHAKE_TIMEOUT
# 1000: IDLE
# 1001: CONNECTING
# 1010: GOT_IP

wlan = None
idx = 0


def wifi_disconnect():
    if wlan:
        wlan.disconnect()


def wifi_connect():
    import network
    global wlan
    global idx
    tick = 0
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print('connecting to network', WIFI[idx][0], '...')
        wlan.connect(WIFI[idx][0], WIFI[idx][1])
        while not wlan.isconnected():
            time.sleep(1)
            tick += 1
            if tick >= WIFI_TIMEOUT:
                idx += 1
                tick = 0
                if idx == len(WIFI):
                    idx = 0

                print('connecting to network ', WIFI[idx][0], ' ...')
                wlan.disconnect()
                wlan.connect(WIFI[idx][0], WIFI[idx][1])

    print('network config:', wlan.ifconfig())

    return wlan
