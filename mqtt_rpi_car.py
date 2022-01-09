import paho.mqtt.publish as publish

import time
import random

#broker_address = "137.194.218.9"
broker_address = "test.mosquitto.org"

# publish messages on these topics
pub_topic1 = "sensor/temperature"
pub_topic2 = "sensor/humidity"
pub_topic3 = "sensor/pressure"
pub_topic4 = "sensor/water"
pub_topic5 = "sensor/light"
pub_topic6 = "sensor/wind"
pub_topic7 = "sensor/tire"
pub_topic8 = "sensor/vitesse"
pub_topic9 = "sensor/fire"

# # # # # # # # # # # # # # # GPIO inputs # # # # # # # # # # # # # # # # # #

def read_temp():
   temperature = str(random.randint(0,100)) #random modifier
   payload="{"
   payload+="\"Temperature\":"
   payload+=temperature
   payload+="}"
   return payload

def read_humidity():
   humidity = str(random.randint(0,100)) #random modifier
   payload="{"
   payload+="\"Humidity\":"
   payload+=humidity
   payload+="}"
   return payload

def read_pressure():
   pressure = str(random.randint(0,100)) #random modifier
   payload="{"
   payload+="\"Pressure\":"
   payload+=pressure
   payload+="}"
   return payload

def read_water():
   water = str(random.randint(0,100)) #random modifier
   payload="{"
   payload+="\"Water\":"
   payload+=water
   payload+="}"
   return payload

def read_light():
   light = str(random.randint(0,100)) #random modifier
   payload="{"
   payload+="\"Light\":"
   payload+=light
   payload+="}"
   return payload

def read_wind():
   wind = str(random.randint(0,100)) #random modifier
   payload="{"
   payload+="\"Wind\":"
   payload+=wind
   payload+="}"
   return payload

def read_tire():
   tire = str(random.randint(0,100)) #random modifier
   payload="{"
   payload+="\"Tire\":"
   payload+=tire
   payload+="}"
   return payload

def read_vitesse():
   vitesse = str(random.randint(0,100)) #random modifier
   payload="{"
   payload+="\"Vitesse\":"
   payload+=vitesse
   payload+="}"
   return payload

def read_fire():
   fire = str(random.randint(0,100)) #random modifier
   payload="{"
   payload+="\"Fire\":"
   payload+=fire
   payload+="}"
   return payload

while True:
    publish.single(pub_topic1, read_temp(), hostname = broker_address)
    publish.single(pub_topic2, read_humidity(), hostname = broker_address)
    publish.single(pub_topic3, read_pressure(), hostname = broker_address)
    publish.single(pub_topic4, read_water(), hostname = broker_address)
    publish.single(pub_topic5, read_light(), hostname = broker_address)
    publish.single(pub_topic6, read_wind(), hostname = broker_address)
    publish.single(pub_topic7, read_tire(), hostname = broker_address)
    publish.single(pub_topic8, read_vitesse(), hostname = broker_address)
    publish.single(pub_topic9, read_fire(), hostname = broker_address)
    print("Done")
    time.sleep(10)
