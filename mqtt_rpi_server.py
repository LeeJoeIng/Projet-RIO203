#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import time
from datetime import datetime
import sys
import pandas as pd
from calculations.calcul_note import *

port = 1883
broker_address = "test.mosquitto.org"

#Tokens of devices (à modifier)
ACCESS_TOKEN1 = '71L19crdoHQQxnmvMq9Q'
ACCESS_TOKEN2 = 'RfYFWuSQrmtMvXFLOBJm'
ACCESS_TOKEN3 = 'RfYFWuSQrmtMvXFLOBJm'
ACCESS_TOKEN4 = 'F8lNcq13Z95uDl6idAFC'
ACCESS_TOKEN5 = 's3tAkxJqaixrBBo0ae5S'
ACCESS_TOKEN6 = 'FURtysDavzwGhPCmGI7Q'
ACCESS_TOKEN7 = 'NwxpOjNhhBtqQrgzTtFE'
ACCESS_TOKEN8 = 'LoRfm9w6DmefqMPJQNIw'

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
stop=[]

dataframe=pd.DataFrame({'lat':lat,
                        'long':long,
                        'seat_belt':seat_belt,
                        'speed':speed,
                        'acceleration':acc,
                        'capteur_dist':ultrasonic,
                        'Stop':stop})

# # # # # # # # # # # # # # # MQTT section # # # # # # # # # # # # # # # # # #
seat_belt=[1]*559
ultrasonic=[10]*559
stop=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

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
       payload1_int=json.loads(payload1)
       acc.append(float(payload1_int["Acceleration"]))
       print("Received message #1")
       mqtt_auth = { 'username': ACCESS_TOKEN1 }
       publish.single(mqtt_topic_TB, payload1, hostname = broker_thingsboard, auth = mqtt_auth)
       print("Please check LATEST TELEMETRY field of your device")
       print(payload1)

   if msg.topic == sub_topic2:
       global payload2
       payload2 = message
       payload2_int=json.loads(payload2)
       lat.append(float(payload2_int["Latitude"]))
       print("Received message #2")
       mqtt_auth = { 'username': ACCESS_TOKEN2 }
       publish.single(mqtt_topic_TB, payload2, hostname = broker_thingsboard, auth = mqtt_auth)
       print("Please check LATEST TELEMETRY field of your device")
       print(payload2)

   if msg.topic == sub_topic3:
       global payload3
       payload3=message
       payload3_int=json.loads(payload3)
       long.append(float(payload3_int["Longtitude"]))
       print("Received message #3")
       mqtt_auth = { 'username': ACCESS_TOKEN3 }
       publish.single(mqtt_topic_TB, payload3, hostname = broker_thingsboard, auth = mqtt_auth)
       print("Please check LATEST TELEMETRY field of your device")
       print(payload3)

   if msg.topic == sub_topic4:
       global payload4
       payload4=message
       payload4_int=json.loads(payload4)
       speed.append(float(payload4_int["Speed"]))
       print("Received message #4")
       mqtt_auth = { 'username': ACCESS_TOKEN2 }
       publish.single(mqtt_topic_TB, payload4, hostname = broker_thingsboard, auth = mqtt_auth)
       print("Please check LATEST TELEMETRY field of your device")
       print(payload4)

   if msg.topic == sub_topic5:
       global payload5
       payload5 = message
       if(payload5=="{\"Status\":Stop}"):

#         for i in range(len(speed)):
#           if (speed[i] <= 0) :
#             stop.append(1)
#           else :
#             stop.append(0)

         dataframe=pd.DataFrame({'lat':lat,'long':long,'seat_belt':seat_belt,'speed':speed,'acceleration':acc,'capteur_dist':ultrasonic, 'Stop':stop})
         print(dataframe)
         points = note(dataframe)
         print("Your result of this driving session is: " + str(points) +"!")
         publish.single(mqtt_topic_TB, "{\"Points\":" + str(points) + "}", hostname = broker_thingsboard, auth = { 'username': ACCESS_TOKEN8 })

         publish.single(mqtt_topic_TB, "{\"Acceleration\":0}", hostname = broker_thingsboard, auth = { 'username': ACCESS_TOKEN1 })
         publish.single(mqtt_topic_TB, "{\"Speed\":0}", hostname = broker_thingsboard, auth = { 'username': ACCESS_TOKEN4 })
         publish.single(mqtt_topic_TB, "{\"Seatbelt\":0}", hostname = broker_thingsboard, auth = { 'username': ACCESS_TOKEN6 })
         publish.single(mqtt_topic_TB, "{\"Ultrasonic\":0}", hostname = broker_thingsboard, auth = { 'username': ACCESS_TOKEN7 })

       else:
         publish.single(mqtt_topic_TB, "{\"Points\":-}", hostname = broker_thingsboard, auth = { 'username': ACCESS_TOKEN8 })

       print("Received message #5")
       mqtt_auth = { 'username': ACCESS_TOKEN2 }
       publish.single(mqtt_topic_TB, payload5, hostname = broker_thingsboard, auth = mqtt_auth)
       print("Please check LATEST TELEMETRY field of your device")
       print(payload5)

   if msg.topic == sub_topic6:
       global payload6
       payload6 = message
       payload6_int=json.loads(payload6)
       seat_belt.append(float(payload6_int["Seatbelt"]))
       print("Received message #6")
       mqtt_auth = { 'username': ACCESS_TOKEN6 }
       publish.single(mqtt_topic_TB, payload6, hostname = broker_thingsboard, auth = mqtt_auth)
       print("Please check LATEST TELEMETRY field of your device")
       print(payload6)

   if msg.topic == sub_topic7:
       global payload7
       payload7 = message
       payload7_int=json.loads(payload7)                         
       ultrasonic.append(float(payload7_int["Ultrasonic"]))
       print("Received message #7")
       mqtt_auth = { 'username': ACCESS_TOKEN7 }
       publish.single(mqtt_topic_TB, payload7, hostname = broker_thingsboard, auth = mqtt_auth)
       print("Please check LATEST TELEMETRY field of your device")
       print(payload7)

# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port, 60)
print(dataframe)
# Process network traffic and dispatch callbacks. This will also handle
# reconnecting.
client.loop_forever()
