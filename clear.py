#!/usr/bin/env python3

import paho.mqtt.publish as publish

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

publish.single(mqtt_topic_TB, "{\"Acceleration\":0}", hostname = broker_thingsboard, auth = { 'username': ACCESS_TOKEN1 })
publish.single(mqtt_topic_TB, "{\"Speed\":0}", hostname = broker_thingsboard, auth = { 'username': ACCESS_TOKEN4 })
publish.single(mqtt_topic_TB, "{\"Seatbelt\":0}", hostname = broker_thingsboard, auth = { 'username': ACCESS_TOKEN6 })
publish.single(mqtt_topic_TB, "{\"Ultrasonic\":0}", hostname = broker_thingsboard, auth = { 'username': ACCESS_TOKEN7 })
publish.single(mqtt_topic_TB, "{\"Points\":-}", hostname = broker_thingsboard, auth = { 'username': ACCESS_TOKEN8 })
publish.single(mqtt_topic_TB, "{\"Tarif\":-}", hostname = broker_thingsboard, auth = { 'username': ACCESS_TOKEN8 })
publish.single(mqtt_topic_TB, "{\"Class\":-}", hostname = broker_thingsboard, auth = { 'username': ACCESS_TOKEN8 })
publish.single(mqtt_topic_TB, "{\"Points_acceleration\":-}", hostname = broker_thingsboard, auth = { 'username': ACCESS_TOKEN8 })
publish.single(mqtt_topic_TB, "{\"Points_distance\":-}", hostname = broker_thingsboard, auth = { 'username': ACCESS_TOKEN8 })
publish.single(mqtt_topic_TB, "{\"Points_seatbelt\":-}", hostname = broker_thingsboard, auth = { 'username': ACCESS_TOKEN8 })
publish.single(mqtt_topic_TB, "{\"Points_stops\":-}", hostname = broker_thingsboard, auth = { 'username': ACCESS_TOKEN8 })
