#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime
import sys

port = 1883
broker_address = "test.mosquitto.org"

# receive messages on these topics
sub_topic1 = "rio203/accelerationFromJSON"

# # # # # # # # # # # # # # # MQTT section # # # # # # # # # # # # # # # # # #
def on_connect(client, userdata, flags, rc):
   print("Connected with result code " + str(rc))
   client.subscribe(sub_topic1)

def on_message(client, userdata, msg):
   message = msg.payload
   message = ''.join(map(chr,message))
   print(msg.topic + " " + message)

   if msg.topic == sub_topic1:
       global payload1
       payload1 = message
       print("Received message #1")
       print(payload1)

# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port, 60)

# Process network traffic and dispatch callbacks. This will also handle
# reconnecting.
client.loop_forever()
