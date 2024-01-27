from config import *

socket = None


def broadcast(message):
    socket.sendto(message.bytes(), ADDRESS)
