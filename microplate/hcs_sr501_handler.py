from microplate.handler_base import Handler
from microplate.home_assistant import HomeAssistantHandler


class MoveHandler(Handler, HomeAssistantHandler):
    def __init__(self, dht):
        super().__init__(dht)

    def handle(self, message):
        if message["event"] == "pir.move":
            self.workers[0].send_message()

    def handle_mqtt(self, topic, msg):
        pass
