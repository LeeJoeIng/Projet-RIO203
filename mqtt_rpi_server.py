#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import time
from datetime import datetime
import sys
import pandas as pd
port = 1883
broker_address = "test.mosquitto.org"

#Tokens of devices (à modifier)
ACCESS_TOKEN1 = 'RfYFWuSQrmtMvXFLOBJm'
mqtt_topic_TB = "v1/devices/me/telemetry"
broker_thingsboard = "localhost"

# receive messages on these topics
sub_topic1 = "rio203/accelerationFromJSON"
sub_topic2 = "rio203/latitudeFromJSON"
sub_topic3 = "rio203/longitudeFromJSON"
sub_topic4 = "rio203/speedFromJSON"
sub_topic5 = "rio203/status"
sub_topic6 = "rio203/seatbelt"
sub_topic7 = "rio203/ultrasonic"
speed=[]
lat=[]
long=[]
seat_belt=[]
acc=[]
ultrasonic=[]
# # # # # # # # # # # # # # # MQTT section # # # # # # # # # # # # # # # # # #
def on_connect(client, userdata, flags, rc):
   print("Connected with result code " + str(rc))
   client.subscribe(sub_topic1)
   client.subscribe(sub_topic2)
   client.subscribe(sub_topic3)
   client.subscribe(sub_topic4)
   client.subscribe(sub_topic5)
   client.subscribe(sub_topic6)
   client.subscribe(sub_topic7)

def on_message(client, userdata, msg):
   message = msg.payload
   message = ''.join(map(chr,message))
   print(msg.topic + " " + message)
   
   if msg.topic == sub_topic1:
       global payload1
       payload1 = message
       payload1=json.loads(payload1)
       acc.append(payload1["Acceleration"])
       print("Received message #1")
       print(payload1)

   if msg.topic == sub_topic2:
       global payload2
       payload2 = message
       payload2=json.loads(payload2)
       lat.append(payload2["Latitude"])
       print("Received message #2")
       mqtt_auth = { 'username': ACCESS_TOKEN1 }
       publish.single(mqtt_topic_TB, payload2, hostname = broker_thingsboard, auth = mqtt_auth)
       print("Please check LATEST TELEMETRY field of your device")
       print(payload2)

   if msg.topic == sub_topic3:
       global payload3
       payload3=message
       payload3=json.loads(payload3)
       long.append(payload3["Longitude"])
       print("Received message #3")
       mqtt_auth = { 'username': ACCESS_TOKEN1 }
       publish.single(mqtt_topic_TB, payload3, hostname = broker_thingsboard, auth = mqtt_auth)
       print("Please check LATEST TELEMETRY field of your device")
       print(payload3)

   if msg.topic == sub_topic4:
       global payload4
       payload4=message
       payload4=json.loads(payload4)
       speed.append(payload2["Speed"])
       print("Received message #4")
       mqtt_auth = { 'username': ACCESS_TOKEN1 }
       publish.single(mqtt_topic_TB, payload4, hostname = broker_thingsboard, auth = mqtt_auth)
       print("Please check LATEST TELEMETRY field of your device")
       print(payload4)

   if msg.topic == sub_topic5:
       global payload5
       payload5 = message
       print("Received message #5")
       mqtt_auth = { 'username': ACCESS_TOKEN1 }
       publish.single(mqtt_topic_TB, payload5, hostname = broker_thingsboard, auth = mqtt_auth)
       print("Please check LATEST TELEMETRY field of your device")
       print(payload5)

   if msg.topic == sub_topic6:
       global payload6
       payload6 = message
       payload6=json.loads(payload6)
       seat_belt.append(payload6["SeatBelt"])
       print("Received message #6")
       mqtt_auth = { 'username': ACCESS_TOKEN1 }
       publish.single(mqtt_topic_TB, payload6, hostname = broker_thingsboard, auth = mqtt_auth)
       print("Please check LATEST TELEMETRY field of your device")
       print(payload6)

   if msg.topic == sub_topic7:
       global payload7
       payload7 = message
       payload7=json.loads(payload7)                         
       ultrasonic.append(payload7["Ultrasonic"])
       print("Received message #7")
       mqtt_auth = { 'username': ACCESS_TOKEN1 }
       publish.single(mqtt_topic_TB, payload7, hostname = broker_thingsboard, auth = mqtt_auth)
       print("Please check LATEST TELEMETRY field of your device")
       print(payload7)
   
dataframe=pd.DataFrame({'lat':lat,
                        'long':long,
                        'seat_belt':seat_belt,
                        'speed':speed,
                        'acc':acc,
                        'distance':ultrasonic})
print(dataframe)                       
# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port, 60)

# Process network traffic and dispatch callbacks. This will also handle
# reconnecting.
client.loop_forever()
