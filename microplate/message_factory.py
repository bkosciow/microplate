import json
from microplate.message import Message


class MessageFactory(object):
    @classmethod
    def create(cls, data=None):
        if data is None:
            return Message()
        else:
            return cls._decode(data)

    @classmethod
    def _decode(cls, message):
        try:
            message = json.loads(message)

            if not cls._validate_message(message):
                return None
            msg = Message()
            msg.set(message)
            msg.decrypt()

            return msg
        except ValueError:
            print(message)
            raise

    @classmethod
    def _validate_message(cls, message):
        if 'protocol' not in message or 'targets' not in message or \
                type(message['targets']) is not list:
            return False

        if message['protocol'] != Message.protocol:
            return False

        if Message.node_name not in message['targets'] and 'ALL' not in message['targets']:
            return False

        return True
