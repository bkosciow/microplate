Boilerplate for Micropython for IoT devices

[read more]
https://koscis.wordpress.com/tag/microplate/


[the same but LUA]
https://koscis.wordpress.com/tag/nodemcu-boilerplate/
https://github.com/bkosciow/nodemcu_boilerplate


Uses the concept of nodes - each device in the network is a node

Node has:
workers - broadcast some data in messages
handlers - react to messages

message is a json network packet, encrypted or not

they are two config files:
config.py - common things like network credential
node_config.py - config only for this device, like node name and id


Works with custom IoT protocol or Home Assistant
- to disable custom IoT set USE_IOT_BROADCAST to False
- HomeAssistant - WiP

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

