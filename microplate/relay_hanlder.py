from microplate.handler_base import Handler
from node_config import *
from config import *


class RelayHandler(Handler):
    def __init__(self, relays):
        super().__init__(relays)

    def handle(self, message):
        if 'channel' in message['parameters']:
            channel = int(message['parameters']['channel'])
            if message['event'] == "channel.off":
                self.workers[0].disable(channel)
            if message['event'] == "channel.on":
                self.workers[0].enable(channel)
            self.workers[0].send_message()

        if message['event'] == 'channel.states':
            self.workers[0].send_message()
