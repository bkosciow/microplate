
def wifi_connect(wifis):
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(wifis[0][0], wifis[0][1])
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
