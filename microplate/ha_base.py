from node_config import *
from config import *


class HABase:
    ha = None
    def __init__(self):
        self.ha_idx = 0
        self.ha_component = {}
        self.base_topic =  f"{HA_BASE_TOPIC}/{NODE_NAME}"
        self.base_id = f"{HA_BASE_TOPIC}-{NODE_NAME}"

    def get_ha_definition(self):
        return self.ha_component

    def get_topic(self):
        first_key = next(iter(self.ha_component))
        return self.ha_component[first_key]['state_topic']

    def publish(self, value, topic = None):
        if not self.ha:
            return
        if topic is None:
            topic = self.get_topic()

        self.ha.publish(topic, value, True)
