import paho.mqtt.client as mqtt
import os
import json
import time
from datetime import datetime

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

# initialise payload
payload1 = "{\"Temperature\":1}"
payload2 = "{\"Humidity\":2}"
payload3 = "{\"Pressure\":3}"
payload4 = "{\"Water\":4}"
payload5 = "{\"Light\":5}"
payload6 = "{\"Wind\":6}"
payload7 = "{\"Tire\":7}"
payload8 = "{\"Vitesse\":8}"
payload9 = "{\"Fire\":9}"

#broker rpiserver - thingsboard
broker_thingsboard = "localhost"

#data listening port
port = 1883

# # # # # # # # # # # # # # # MQTT section # # # # # # # # # # # # # # # # # #

# when connecting to mqtt do this;
# The callback for when the client receives a CONNACK response from the server.
# Subscribing in on_connect() means that if we lose the connection and
# reconnect then subscriptions will be renewed.

def on_publish(client,userdata,result):
    print("data published to thingsboard \n")
    pass

clientTB1 = mqtt.Client()
clientTB1.on_publish = on_publish
clientTB1.username_pw_set(ACCESS_TOKEN1)
clientTB1.connect(broker_thingsboard, port, 60)

clientTB2 = mqtt.Client()
clientTB2.on_publish = on_publish
clientTB2.username_pw_set(ACCESS_TOKEN2)
clientTB2.connect(broker_thingsboard, port, 60)

clientTB3 = mqtt.Client()
clientTB3.on_publish = on_publish
clientTB3.username_pw_set(ACCESS_TOKEN3)
clientTB3.connect(broker_thingsboard, port, 60)

clientTB4 = mqtt.Client()
clientTB4.on_publish = on_publish
clientTB4.username_pw_set(ACCESS_TOKEN4)
clientTB4.connect(broker_thingsboard, port, 60)

clientTB5 = mqtt.Client()
clientTB5.on_publish = on_publish
clientTB5.username_pw_set(ACCESS_TOKEN5)
clientTB5.connect(broker_thingsboard, port, 60)

clientTB6 = mqtt.Client()
clientTB6.on_publish = on_publish
clientTB6.username_pw_set(ACCESS_TOKEN6)
clientTB6.connect(broker_thingsboard, port, 60)

clientTB7 = mqtt.Client()
clientTB7.on_publish = on_publish
clientTB7.username_pw_set(ACCESS_TOKEN7)
clientTB7.connect(broker_thingsboard, port, 60)

clientTB8 = mqtt.Client()
clientTB8.on_publish = on_publish
clientTB8.username_pw_set(ACCESS_TOKEN8)
clientTB8.connect(broker_thingsboard, port, 60)

clientTB9 = mqtt.Client()
clientTB9.on_publish = on_publish
clientTB9.username_pw_set(ACCESS_TOKEN9)
clientTB9.connect(broker_thingsboard, port, 60)

while True:
   ret1 = clientTB1.publish("v1/devices/me/telemetry",payload1) #topic-v1/devices/me/telemetry
   print("Please check LATEST TELEMETRY field of your device")
   print(payload1);

   ret2 = clientTB2.publish("v1/devices/me/telemetry",payload2) #topic-v1/devices/me/telemetry
   print("Please check LATEST TELEMETRY field of your device")
   print(payload2);

   ret3 = clientTB3.publish("v1/devices/me/telemetry",payload3) #topic-v1/devices/me/telemetry
   print("Please check LATEST TELEMETRY field of your device")
   print(payload3);

   ret4 = clientTB4.publish("v1/devices/me/telemetry",payload4) #topic-v1/devices/me/telemetry
   print("Please check LATEST TELEMETRY field of your device")
   print(payload4);

   ret5 = clientTB5.publish("v1/devices/me/telemetry",payload5) #topic-v1/devices/me/telemetry
   print("Please check LATEST TELEMETRY field of your device")
   print(payload5);

   ret6 = clientTB6.publish("v1/devices/me/telemetry",payload6) #topic-v1/devices/me/telemetry
   print("Please check LATEST TELEMETRY field of your device")
   print(payload6);

   ret7 = clientTB7.publish("v1/devices/me/telemetry",payload7) #topic-v1/devices/me/telemetry
   print("Please check LATEST TELEMETRY field of your device")
   print(payload7);

   ret8 = clientTB8.publish("v1/devices/me/telemetry",payload8) #topic-v1/devices/me/telemetry
   print("Please check LATEST TELEMETRY field of your device")
   print(payload8);

   ret9 = clientTB9.publish("v1/devices/me/telemetry",payload9) #topic-v1/devices/me/telemetry
   print("Please check LATEST TELEMETRY field of your device")
   print(payload9);

   time.sleep(5)
