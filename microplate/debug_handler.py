from microplate.handler_base import Handler


class DebugHandler(Handler):
    def __init__(self,):
        super().__init__()

    def handle(self, message):
        print(message.data)

