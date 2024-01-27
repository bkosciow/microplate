import binascii
import json
import cryptolib
import hashlib
from os import urandom
try:
    import hmac
except:
    import mip
    mip.install("hmac")
    import hmac


class Cryptor:
    name = "message.aessha1"
    algorithm = 2

    def __init__(self, staticiv, ivkey, datakey, passphrase):
        self.staticiv = staticiv
        self.ivkey = ivkey
        self.datakey = datakey
        self.passphrase = passphrase

    def encrypt(self, message):
        msg = json.dumps(message.data)
        msg_pad = _pad(16, msg)
        iv = urandom(32)
        iv = binascii.hexlify(iv)[:16]
        iv_suite = cryptolib.aes(self.ivkey.encode(), self.algorithm, self.staticiv.encode())
        encrypted_iv = iv_suite.encrypt(iv)

        data_suite = cryptolib.aes(self.datakey.encode(), self.algorithm, iv)
        encrypted_data = data_suite.encrypt(msg_pad.encode())

        fullmessage = iv.decode('utf8') + msg
        _hmac = hmac.new(self.passphrase.encode(), fullmessage.encode(), hashlib.sha1)
        computed_hash = _hmac.hexdigest()

        message.set({
            'event': self.name,
            'parameters': [
                binascii.hexlify(encrypted_iv).decode('utf8'),
                binascii.hexlify(encrypted_data).decode('utf8'),
                computed_hash
            ],
            'response': ''
        })

    def decrypt(self, message):
        encrypted_iv = binascii.unhexlify(message.data['parameters'][0])
        encrypted_data = binascii.unhexlify(message.data['parameters'][1])
        _hash = message.data['parameters'][2]

        iv_suite = cryptolib.aes(self.ivkey.encode(), self.algorithm, self.staticiv.encode())
        iv = iv_suite.decrypt(encrypted_iv)
        data_suite = cryptolib.aes(self.datakey.encode(), self.algorithm, iv)
        data = data_suite.decrypt(encrypted_data).strip(b'\x00').decode('utf8')
        fullmessage = iv.decode('utf8') + data
        _hmac = hmac.new(self.passphrase.encode(), fullmessage.encode(), hashlib.sha1)
        computed_hash = _hmac.hexdigest()
        if computed_hash != _hash:
            raise Exception(computed_hash + "  " + _hash)

        msg = json.loads(data)
        message.clear()
        message.set(msg)


def _pad(l, s):
    return s + (l - len(s) % l) * chr(00)
