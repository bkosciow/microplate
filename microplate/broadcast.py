from config import *

socket = None


def broadcast(message):
    if socket is None:
        print("No Network configured, socket is None")
        return

    try:
        socket.sendto(message.bytes(), ADDRESS)
    except OSError as e:
        if e.errno == 118:
            print("Network down?")
