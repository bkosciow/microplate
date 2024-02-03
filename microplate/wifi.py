import time

# 200: BEACON_TIMEOUT
# 201: NO_AP_FOUND
# 202: WRONG_PASSWORD
# 203: ASSOC_FAIL
# 204: HANDSHAKE_TIMEOUT
# 1000: IDLE
# 1001: CONNECTING
# 1010: GOT_IP

wlan = None


def wifi_connect(wifis):
    import network
    global wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(wifis[0][0], wifis[0][1])
        while not wlan.isconnected():
            print(wlan.status())
            time.sleep(1)
    print('network config:', wlan.ifconfig())

    return wlan
