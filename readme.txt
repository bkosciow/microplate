Boilerplate for Micropython for IoT devices
Works with Home Assistant via MQTT


[read more]
https://koscis.wordpress.com/project/microplate-how-to-use/
https://koscis.wordpress.com/tag/microplate/


[the same but LUA]
https://koscis.wordpress.com/tag/nodemcu-boilerplate/
https://github.com/bkosciow/nodemcu_boilerplate


Uses the concept of nodes - each device in the network is a node

Node has:
workers - broadcast some data in messages
handlers - react to messages

message is a json network packet, encrypted or not

there are two config files:
config.py - common things like network credential
node_config.py - config only for this device, like node name and id


Works with custom IoT protocol or Home Assistant
- to disable custom IoT set USE_IOT_BROADCAST to False
- HomeAssistant - integration via MQTT


Home Assistant config (config.py):

# set False to disable HA
USE_HA = True
HA_BASE_DISCOVERY_TOPIC = "homeassistant/device"
HA_BASE_TOPIC = "home"
MQTT_SERVER = "192.168.1.40"
MQTT_PORT = 1883
MQTT_USER = "login"
MQTT_PWD = "pass"


[workers]
dht11
light
pir
buttons
network

[handlers]
relay
dht11
pir
light
button

