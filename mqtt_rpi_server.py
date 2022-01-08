import paho.mqtt.client as mqtt

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
   message = str(msg.payload)
   print(msg.topic + " " + message)

   if msg.topic == sub_topic1:
       print("Received message #1, do something")
       # Do something à modifier

    if msg.topic == sub_topic2:
        print("Received message #2, do something else")
        # Do something else à modifier

    if msg.topic == sub_topic3:
        print("Received message #3, do something")
        # Do something à modifier

   if msg.topic == sub_topic4:
       print("Received message #4, do something")
       # Do something à modifier

   if msg.topic == sub_topic5:
       print("Received message #5, do something")
       # Do something à modifier

   if msg.topic == sub_topic6:
       print("Received message #6, do something")
       # Do something à modifier

   if msg.topic == sub_topic7:
       print("Received message #7, do something")
       # Do something à modifier

   if msg.topic == sub_topic8:
       print("Received message #8, do something")
       # Do something à modifier

   if msg.topic == sub_topic9:
       print("Received message #9, do something")
       # Do something à modifier

# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, 1883, 60)

# Process network traffic and dispatch callbacks. This will also handle
# reconnecting.
client.loop_forever()
