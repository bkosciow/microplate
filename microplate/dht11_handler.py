from microplate.handler_base import Handler


class Dht11Handler(Handler):
    def __init__(self, dht):
        super().__init__(dht)

    def handle(self, message):
        if message["event"] == "dht.readings":
            self.workers[0].send_message()
