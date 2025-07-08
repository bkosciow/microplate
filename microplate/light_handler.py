from microplate.handler_base import Handler
from microplate.home_assistant import HomeAssistantHandler


class LightHandler(Handler, HomeAssistantHandler):
    def __init__(self, dht):
        super().__init__(dht)

    def handle(self, message):
        if message["event"] == "light.state":
            self.workers[0].send_message()

    def handle_mqtt(self, topic, msg):
        pass
