import ubinascii
import json
import machine
from node_config import  *


class Message(object):
    protocol = "iot:1"
    node_id = None
    node_name = None
    encoders = []
    decoders = {}
    drop_unencrypted = False

    def __init__(self):
        self.data = None
        self.encoder = 0

    @classmethod
    def add_decoder(cls, decoder):
        cls.decoders[decoder.name] = decoder

    @classmethod
    def add_encoder(cls, encoder):
        cls.encoders.append(encoder)

    def _initialize_data(self):
        self.data = {
            'protocol': self.protocol,
            'node': self.node_name,
            'chip_id': self.node_id,
            'event': '',
            'parameters': {},
            'response': '',
            'targets': [
                'ALL'
            ]
        }

    def clear(self):
        self._initialize_data()

    def set(self, data):
        if self.data is None:
            self._initialize_data()

        for k, v in data.items():
            self.data[k] = v

    def encrypt(self):
        if len(self.encoders) > 0:
            self.encoders[self.encoder].encrypt(self)

    def decrypt(self):
        if len(self.data['event']) > 8 and self.data['event'][0:8] == "message.":
            if self.data['event'] in self.decoders:
                self.decoders[self.data['event']].decrypt(self)
            else:
                raise Exception("Decryptor %s not found".format(self.data['event']))
        else:
            if self.drop_unencrypted:
                if len(self.decoders) > 0:
                    self.data = None
                else:
                    raise Exception("Encryption required but decoders empty")

    def bytes(self):
        self.encrypt()
        return json.dumps(self.data).encode()

    def repr(self):
        return json.dumps(self.data)

    def __getitem__(self, item):
        return self.data[item]
