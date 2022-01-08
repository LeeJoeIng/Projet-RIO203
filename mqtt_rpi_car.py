import paho.mqtt.publish as publish
import time

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
   temperature = get_temperature() #random à modifier
   payload="{"
   payload+="\"Temperature\":"
   payload+=temperature
   payload+=";"
   payload+="}"
   return payload

def read_humidity():
   humidity = get_humidity() #random à modifier
   payload="{"
   payload+="\"Humidity\":"
   payload+=humidity
   payload+=";"
   payload+="}"
   return payload

def read_pressure():
   pressure = get_pressure() #random à modifier
   payload="{"
   payload+="\"Pressure\":"
   payload+=pressure
   payload+=";"
   payload+="}"
   return payload

def read_water():
   water = get_water() #random à modifier
   payload="{"
   payload+="\"Water\":"
   payload+=water
   payload+=";"
   payload+="}"
   return payload

def read_light():
   light = get_light() #random à modifier
   payload="{"
   payload+="\"Light\":"
   payload+=light
   payload+=";"
   payload+="}"
   return payload

def read_wind():
   wind = get_wind() #random à modifier
   payload="{"
   payload+="\"Wind\":"
   payload+=wind
   payload+=";"
   payload+="}"
   return payload

def read_tire():
   tire = sense.get_tire() #random à modifier
   payload="{"
   payload+="\"Tire\":"
   payload+=tire
   payload+=";"
   payload+="}"
   return payload

def read_vitesse():
   vitesse = sense.get_vitesse() #random à modifier
   payload="{"
   payload+="\"Vitesse\":"
   payload+=vitesse
   payload+=";"
   payload+="}"
   return payload

def read_fire():
   fire = sense.get_fire() #random à modifier
   payload="{"
   payload+="\"Fire\":"
   payload+=fire
   payload+=";"
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
   time.sleep(1 * 60)
