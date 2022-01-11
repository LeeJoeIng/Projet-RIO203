import paho.mqtt.publish as publish

import time
import random

from sensors.barometerAndThermometer import get_temp,get_pressure
from sensors.humiture_sensor import get_humidity
from sensors.notyet import *
from sensors.light import get_light
from sensors.water import get_water

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

# Mettre uniquement les capteurs branchés sur True

has_temp = True
has_humidity = True
has_pressure = True
has_water = True
has_light = True
has_wind = False
has_tire = False
has_vitesse = False
has_fire = False



def read_temp():
    temperature = get_temp(has_temp)
    print("Temperature= ",temperature)
    payload="{"
    payload+="\"Temperature\":"
    payload+=temperature
    payload+="}"
    return payload

def read_humidity():
    humidity = get_humidity(has_humidity)
    print("Humidity= ", humidity)
    payload="{"
    payload+="\"Humidity\":"
    payload+=humidity
    payload+="}"
    return payload

def read_pressure():
    pressure = get_pressure(has_pressure)
    print("Pressure= ", pressure)
    payload="{"
    payload+="\"Pressure\":"
    payload+=pressure
    payload+="}"
    return payload

def read_water():
    water = get_water(has_water)
    print("Water= ", water)
    payload="{"
    payload+="\"Water\":"
    payload+=water
    payload+="}"
    return payload

def read_light():
    light = get_light(has_light)
    print("light= ", light)
    payload="{"
    payload+="\"Light\":"
    payload+=light
    payload+="}"
    return payload

def read_wind():
    wind = get_wind(has_wind)
    print("Wind= ", wind)
    payload="{"
    payload+="\"Wind\":"
    payload+=wind
    payload+="}"
    return payload

def read_tire():
    tire = get_tire(has_tire)
    print("Tire= ", tire)
    payload="{"
    payload+="\"Tire\":"
    payload+=tire
    payload+="}"
    return payload

def read_vitesse():
    vitesse = get_vitesse(has_vitesse)
    print("Speed= ", vitesse)
    payload="{"
    payload+="\"Vitesse\":"
    payload+=vitesse
    payload+="}"
    return payload

def read_fire():
    fire = get_fire(has_fire)
    print("fire= ", fire)
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
