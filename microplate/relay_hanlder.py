from microplate.handler_base import Handler
from microplate.home_assistant import HomeAssistantHandler


class RelayHandler(Handler, HomeAssistantHandler):
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

    def handle_mqtt(self, topic, msg):
        msg = self.get_dict(msg)
        if msg[1] == 1:
            self.workers[0].enable(msg[0])
        else:
            self.workers[0].disable(msg[0])
