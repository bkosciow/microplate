Boilerplate for Micropython

Uses the concept of nodes - each device in network is a node

Node has:
workers - broadcast some data in messages
handlers - react to messages

message is a json network packet, encrypted or not

they are two cconfig files:
config.py - common things like network credential
node_config.py - config only for this device, like node-mane


