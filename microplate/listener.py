from microplate.handler_base import Handler
from microplate.handler_base import DecryptNotFound
from microplate.message_factory import MessageFactory
import uasyncio
import sys


class Listener:
    def __init__(self, socket, buffer_size=2048):
        self.socket = socket
        self.buffer_size = buffer_size
        self.handlers = {}
        self.work = True
        self.ignore_missing_decoders = True

    def add_handler(self, name, *argv):
        if name not in self.handlers:
            self.handlers[name] = []
        for handler in argv:
            if not isinstance(handler, Handler):
                raise AttributeError('not a handler!')
            self.handlers[name].append(handler)

    def get_handler(self, name):
        return self.handlers[name]

    def has_handler(self, name):
        return name in self.handlers

    async def run(self):
        """server loop"""
        while self.work:
            try:
                data, address = self.socket.recvfrom(self.buffer_size)
                message = MessageFactory.create(data)
                if message and message.data:
                    self.serve_message(message)
                await uasyncio.sleep(0)
            except DecryptNotFound as e:
                if not self.ignore_missing_decoders:
                    print(str(e))
                await uasyncio.sleep(0)
            except OSError as e:
                # if e.errno == 11:
                await uasyncio.sleep(0)
            except Exception as e:
                print(str(e))
                sys.print_exception(e)
                await uasyncio.sleep(0)

    def serve_message(self, message):
        for handlers in self.handlers:
            for handler in self.handlers[handlers]:
                handler.handle(message)

    def stop(self):
        self.work = False
