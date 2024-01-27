from microplate.handler_base import Handler


class LightHandler(Handler):
    def __init__(self, dht):
        super().__init__(dht)

    def handle(self, message):
        if message["event"] == "light.state":
            self.workers[0].send_message()
