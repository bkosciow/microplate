from config import *
from node_config import *
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
import uasyncio
from microplate.ha_base import HABase


class HomeAssistantHandler:
    def handle_mqtt(self, topic, message):
        raise Exception("define handle_mqtt")

    def get_dict(self, data):
        return json.loads(data)

class HomeAssistant:
    def __init__(self):
        self.work = True
        self.client_id = ubinascii.hexlify(machine.unique_id())
        self.client = MQTTClient(NODE_ID, MQTT_SERVER, user=MQTT_USER, password=MQTT_PWD, port=MQTT_PORT)
        self.client.set_callback(self.callback)
        self.client.connect()
        self.handlers = {}

    def add_handler(self, handler):
        if not isinstance(handler, HomeAssistantHandler):
            print("handler ",handler," skipping HA")
            return
        if not isinstance(handler.workers[0], HABase):
            print("handler OK but worker is not ",handler," skipping HA")
            return
        definitions = handler.workers[0].get_ha_definition()
        for _id in definitions:
            if "command_topic" in definitions[_id]:
                topic = definitions[_id]["command_topic"]
                if not topic in self.handlers:
                    self.handlers[topic] = []
                if handler not in self.handlers[topic]:
                    print("sub to:", topic)
                    self.handlers[topic].append(handler)
                    self.client.subscribe(topic)

    def discovery_packet(self):
        packet = {
            'dev': {
                'ids': NODE_ID,
                'name': f"{NODE_NAME} ({NODE_ID})",
                'mf': 'kosci'
            },
            'o': {
                'name': NODE_NAME,
            },
            'cmps': {},
            'qos': 2
        }
        for topic in self.handlers:
            for handler in self.handlers[topic]:
                cmp = handler.workers[0].get_ha_definition()
                packet['cmps'].update(cmp)

        self.publish(f"{HA_BASE_DISCOVERY_TOPIC}/{NODE_NAME}/config", packet, True)
        return packet

    def publish(self, topic, packet, persist):
        if isinstance(packet, dict) or isinstance(packet, list):
            packet = json.dumps(packet)

        print("sending to: ", topic)
        self.client.publish(topic, packet, retain=persist)

    def callback(self, topic, msg):
        topic = topic.decode('utf8')
        msg = msg.decode('utf8')
        # print("callback", topic, msg)
        if topic in self.handlers:
            for handler in self.handlers[topic]:
                handler.handle_mqtt(topic, msg)

    async def run(self):
        while self.work:
            self.client.check_msg()
            await uasyncio.sleep(0)
