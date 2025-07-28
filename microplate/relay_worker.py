from microplate.module import ModuleInterface
from machine import Pin
from microplate.message import Message
from microplate.broadcast import broadcast
from microplate.ha_base import HABase



class RelayWorker(ModuleInterface, HABase):
    def __init__(self, relays, tick=7000):
        ModuleInterface.__init__(self,None, tick)
        HABase.__init__(self)
        self.relays = []
        self.initialized = False
        for channel, item in enumerate(relays):
            self.relays.append({
                'pin': Pin(item['pin'], Pin.OUT, Pin.PULL_UP),
                'enable': 0 if item['enabled'] == 0 else 1,
                'disable': 1 if item['enabled'] == 0 else 0,
                'current': item['default']
            })
            self.toggle(channel, item['default'])
        self.initialized = True

    def action(self):
        self.send_message()
        if self.callback:
            self.callback('action', self.get_statuses())

    def get_statuses(self):
        ret = []
        for item in self.relays:
            state = item["pin"].value()
            if state == item["enable"]:
                state = 1
            else:
                state = 0
            ret.append(state)

        return ret

    def send_message(self):
        if not self.initialized:
            return
        ret = self.get_statuses()
        message = Message()
        message.set(
            {
                "event": "channel.status",
                "parameters": ret

            }
        )
        broadcast(message)
        self.publish(ret)

    def toggle(self, channel, state):
        if channel < len(self.relays):
            self.relays[channel]["pin"].value(state)
            self.relays[channel]["current"] = state
            self.send_message()
            if self.callback:
                self.callback('send_action', self.get_statuses())

    def disable(self, channel):
        if channel < len(self.relays):
            self.toggle(channel, self.relays[channel]["disable"])

    def enable(self, channel):
        if channel < len(self.relays):
            self.toggle(channel, self.relays[channel]["enable"])

    def get_ha_definition(self):
        for i in range(0, len(self.relays)):
            self.ha_component[f"{self.base_id}-power{self.ha_idx+i}"] = {
                'p': 'switch',
                'unique_id': f"{self.base_id}-power{self.ha_idx+i}",
                'state_topic': f"{self.base_topic}/power{self.ha_idx}/state",
                'command_topic': f"{self.base_topic}/power{self.ha_idx}/command",
                'payload_on': '1',
                'payload_off': '0',
                "value_template": "{{ value_json["+str(i)+"] }}",
                "command_template": "["+str(i)+", {{ value }}]",
            }

        return self.ha_component