from microplate.handler_base import Handler
from microplate.home_assistant import HomeAssistantHandler


class ButtonHandler(Handler, HomeAssistantHandler):
    def __init__(self, dht):
        super().__init__(dht)

    def handle(self, message):
        pass

    def handle_mqtt(self, topic, msg):
        msg = self.get_dict(msg)
        self.workers[0].click(msg[0])
