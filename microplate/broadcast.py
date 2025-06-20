from config import *

socket = None


def broadcast(message):
    if USE_IOT_BROADCAST:
        try:
            socket.sendto(message.bytes(), ADDRESS)
        except OSError as e:
            if e.errno == 118:
                print("Network down?")
