from microplate.handler_base import Handler
from microplate.home_assistant import HomeAssistantHandler

class HD44780Handler(Handler, HomeAssistantHandler):
    def __init__(self, dev):
        super().__init__(dev)

    def handle(self, message):
        if message["event"] == "lcd.set_content":
            print(message)

    def handle_mqtt(self, topic, msg):
        self.workers[0].io.buffer_clear()
        self.workers[0].io.set_xy(0,0)
        self.workers[0].io.stream(msg)
