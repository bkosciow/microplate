from microplate.handler_base import Handler
from machine import Pin
from microplate.message import Message
from microplate.broadcast import broadcast
from node_config import *
from config import *
from microplate.ha_base import HABase

class RelayHandler(Handler, HABase):
    ha_idx = 0
    ha_component = {
        'p': 'switch',
        'unique_id': f"home-{NODE_NAME}-power0",
        'state_topic': f"{HA_BASE_TOPIC}/{NODE_NAME}/power{ha_idx}/state",
        'command_topic': f"{HA_BASE_TOPIC}/power{ha_idx}/command",
        'payload_on': '1',
        'payload_off': '0',
        "value_template": "{{ value_json[0] }}",
        "command_template": "[0, {{ value }}]",
    }

    def __init__(self, relays):
        super().__init__()
        self.relays = []
        for channel, item in enumerate(relays):
            self.relays.append({
                'pin': Pin(item['pin'], Pin.OUT, Pin.PULL_UP),
                'enable': 0 if item['enabled'] == 0 else 1,
                'disable': 1 if item['enabled'] == 0 else 0,
                'current': item['default']
            })
            self.toggle(channel, item['default'])

    def toggle(self, channel, state):
        if channel < len(self.relays):
            self.relays[channel]["pin"].value(state)
            self.relays[channel]["current"] = state
            self.broadcast()

    def disable(self, channel):
        if channel < len(self.relays):
            self.toggle(channel, self.relays[channel]["disable"])

    def enable(self, channel):
        if channel < len(self.relays):
            self.toggle(channel, self.relays[channel]["enable"])

    def broadcast(self):
        ret = []
        for item in self.relays:
            state = item["pin"].value()
            if state == item["enable"]:
                state = 1
            else:
                state = 0
            ret.append(state)
        message = Message()
        message.set(
            {
                "event": "channel.status",
                "parameters": ret

            }
        )
        broadcast(message)

    def handle(self, message):
        if 'channel' in message['parameters']:
            channel = int(message['parameters']['channel'])
            if message['event'] == "channel.off":
                self.disable(channel)
            if message['event'] == "channel.on":
                self.enable(channel)
            self.broadcast()

        if message['event'] == 'channel.states':
            self.broadcast()
