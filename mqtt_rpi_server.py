import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import os
import json
import time
from datetime import datetime
import sys

#Tokens of devices (à modifier)
ACCESS_TOKEN1 = 'LoRfm9w6DmefqMPJQNIw'
ACCESS_TOKEN2 = 's3tAkxJqaixrBBo0ae5S'
ACCESS_TOKEN3 = 'WK4sEyaEyPUG3nH0IfEP'
ACCESS_TOKEN4 = 'NwxpOjNhhBtqQrgzTtFE'
ACCESS_TOKEN5 = 'F8lNcq13Z95uDl6idAFC'
ACCESS_TOKEN6 = 'pHaaYN1iqnrYvUpGyTbt'
ACCESS_TOKEN7 = 'vmWsSYMqGg8AGCiamhM9'
ACCESS_TOKEN8 = '71L19crdoHQQxnmvMq9Q'
ACCESS_TOKEN9 = 'FURtysDavzwGhPCmGI7Q'

mqtt_topic_TB = "v1/devices/me/telemetry"

#broker rpiserver - thingsboard
broker_thingsboard = "localhost"

#data listening port
port = 1883

#broker rpiserver - rpicar
#broker_address = "137.194.218.9"
broker_address = "test.mosquitto.org"

# receive messages on these topics
sub_topic1 = "sensor/temperature"
sub_topic2 = "sensor/humidity"
sub_topic3 = "sensor/pressure"
sub_topic4 = "sensor/water"
sub_topic5 = "sensor/light"
sub_topic6 = "sensor/wind"
sub_topic7 = "sensor/tire"
sub_topic8 = "sensor/vitesse"
sub_topic9 = "sensor/fire"

# # # # # # # # # # # # # # # MQTT section # # # # # # # # # # # # # # # # # #

# when connecting to mqtt do this;
# The callback for when the client receives a CONNACK response from the server.
# Subscribing in on_connect() means that if we lose the connection and
# reconnect then subscriptions will be renewed.
def on_connect(client, userdata, flags, rc):
   print("Connected with result code " + str(rc))
   client.subscribe(sub_topic1)
   client.subscribe(sub_topic2)
   client.subscribe(sub_topic3)
   client.subscribe(sub_topic4)
   client.subscribe(sub_topic5)
   client.subscribe(sub_topic6)
   client.subscribe(sub_topic7)
   client.subscribe(sub_topic8)
   client.subscribe(sub_topic9)

# when receiving a mqtt message do this;
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
   message = msg.payload
   message = ''.join(map(chr,message))
   print(msg.topic + " " + message)

   if msg.topic == sub_topic1:
       global payload1
       payload1 = message
       print("Received message #1")
       mqtt_auth = { 'username': ACCESS_TOKEN1 }
       publish.single(mqtt_topic_TB, payload1, hostname = broker_thingsboard, auth = mqtt_auth)
       print("Please check LATEST TELEMETRY field of your device")

   if msg.topic == sub_topic2:
       global payload2
       payload2 = message
       print("Received message #2")
       mqtt_auth = { 'username': ACCESS_TOKEN2 }
       publish.single(mqtt_topic_TB, payload2, hostname = broker_thingsboard, auth = mqtt_auth)
       print("Please check LATEST TELEMETRY field of your device")
       print(payload2);

   if msg.topic == sub_topic3:
       global payload3
       payload3 = message
       print("Received message #3")
       mqtt_auth = { 'username': ACCESS_TOKEN3 }
       publish.single(mqtt_topic_TB, payload3, hostname = broker_thingsboard, auth = mqtt_auth)
       print("Please check LATEST TELEMETRY field of your device")
       print(payload3);

   if msg.topic == sub_topic4:
       global payload4
       payload4 = message
       print("Received message #4")
       mqtt_auth = { 'username': ACCESS_TOKEN4 }
       publish.single(mqtt_topic_TB, payload4, hostname = broker_thingsboard, auth = mqtt_auth)
       print("Please check LATEST TELEMETRY field of your device")
       print(payload4);

   if msg.topic == sub_topic5:
       global payload5
       payload5 = message
       print("Received message #5")
       mqtt_auth = { 'username': ACCESS_TOKEN5 }
       publish.single(mqtt_topic_TB, payload5, hostname = broker_thingsboard, auth = mqtt_auth)
       print("Please check LATEST TELEMETRY field of your device")
       print(payload5);

   if msg.topic == sub_topic6:
       global payload6
       payload6 = message
       print("Received message #6")
       mqtt_auth = { 'username': ACCESS_TOKEN6 }
       publish.single(mqtt_topic_TB, payload6, hostname = broker_thingsboard, auth = mqtt_auth)
       print("Please check LATEST TELEMETRY field of your device")
       print(payload6);

   if msg.topic == sub_topic7:
       global payload7
       payload7 = message
       print("Received message #7")
       mqtt_auth = { 'username': ACCESS_TOKEN7 }
       publish.single(mqtt_topic_TB, payload7, hostname = broker_thingsboard, auth = mqtt_auth)
       print("Please check LATEST TELEMETRY field of your device")
       print(payload7);

   if msg.topic == sub_topic8:
       global payload8
       payload8 = message
       print("Received message #8")
       mqtt_auth = { 'username': ACCESS_TOKEN8 }
       publish.single(mqtt_topic_TB, payload8, hostname = broker_thingsboard, auth = mqtt_auth)
       print("Please check LATEST TELEMETRY field of your device")
       print(payload8);

   if msg.topic == sub_topic9:
       global payload9
       payload9 = message
       print("Received message #9")
       mqtt_auth = { 'username': ACCESS_TOKEN9 }
       publish.single(mqtt_topic_TB, payload9, hostname = broker_thingsboard, auth = mqtt_auth)
       print("Please check LATEST TELEMETRY field of your device")
       print(payload9);
# create function for callback
def on_publish(client,userdata,result):
    print("data published to thingsboard \n")
    pass

# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port, 60)

# Process network traffic and dispatch callbacks. This will also handle
# reconnecting.
client.loop_forever()
