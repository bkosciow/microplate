from config import *
from node_config import *
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json

ha = None

class HomeAssistant:
    def __init__(self):
        self.client_id = ubinascii.hexlify(machine.unique_id())
        self.client = MQTTClient(NODE_ID, MQTT_SERVER, user=MQTT_USER, password=MQTT_PWD, port=MQTT_PORT)
        self.client.set_callback(self.callback)
        self.client.connect()
        self.objects = []
        global ha
        ha = self
        self.name2topic = {}

    def add_worker(self):
        pass

    def add(self, _class):
        definitions = _class.get_ha_definition()
        # if not name in self.objects:
        #     self.objects[name] = []
        self.objects.append(_class)

        for _id in definitions:
            if "command_topic" in definitions[_id]:
                print("sub to:", definitions[_id]["command_topic"])
                self.client.subscribe(definitions[_id]["command_topic"])

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
        for item in self.objects:
            cmp = item.get_ha_definition()
            packet['cmps'].update(cmp)
        # for name in self.objects:
        #     for item in self.objects[name]:
        #         cmp = item.get_ha_definition()
        #         packet['cmps'].update(cmp)

        self.publish(f"{HA_BASE_DISCOVERY_TOPIC}/{NODE_NAME}/config", packet, True)
        return packet

    def publish(self, topic, packet, persist):
        if isinstance(packet, dict) or isinstance(packet, list):
            packet = json.dumps(packet)

        print("sending to: ", topic)
        self.client.publish(topic, packet, retain=persist)

    def callback(self, topic, msg):
        print(topic, msg)
