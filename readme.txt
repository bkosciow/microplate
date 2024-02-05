Boilerplate for Micropython

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
node_config.py - config only for this device, like node-mane



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

