from microplate.handler_base import Handler
from microplate.home_assistant import HomeAssistantHandler

class HD44780Handler(Handler, HomeAssistantHandler):
    def __init__(self, dev):
        super().__init__(dev)

    def handle(self, message):
        if message["event"] == "lcd.set_text":
            if 'clear' in message['parameters'] and message['parameters']['clear']:
                self.workers[0].io.buffer_clear()
            if 'xy' in message['parameters']:
                self.workers[0].io.set_xy(message['parameters']['xy'][0], message['parameters']['xy'][1])
            if 'text' in message['parameters']:
                self.workers[0].io.stream(message['parameters']['text'])

    def handle_mqtt(self, topic, msg):
        self.workers[0].io.buffer_clear()
        self.workers[0].io.set_xy(0,0)
        self.workers[0].io.stream(msg)
