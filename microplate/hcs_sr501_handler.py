from microplate.handler_base import Handler


class MoveHandler(Handler):
    def __init__(self, dht):
        super().__init__(dht)

    def handle(self, message):
        if message["event"] == "pir.move":
            self.workers[0].send_message()
