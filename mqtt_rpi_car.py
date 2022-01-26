#!/usr/bin/env python3

import json
import time
import pandas as pd
import paho.mqtt.publish as publish

broker_address = "test.mosquitto.org"

# publish messages on these topics
pub_topic1 = "rio203/accelerationFromJSON"
pub_topic2 = "rio203/latitudeFromJSON"
pub_topic3 = "rio203/longitudeFromJSON"
pub_topic4 = "rio203/speedFromJSON"
pub_topic5 = "rio203/status"

# # # # # # # # # # # # # # # Preparing payload # # # # # # # # # # # # # # # # # #

def read_accel(i):
   accel = dataframe.loc[i,'acceleration']
   payload="{"
   payload+="\"Acceleration\":"
   payload+=str(accel)
   payload+="}"
   #print(payload)
   return payload

def read_speed(i):
   speed = dataframe.loc[i,'speed']
   payload="{"
   payload+="\"Speed\":"
   payload+=str(speed)
   payload+="}"
   #print(payload)
   return payload

def read_latitude(i):
   latitude = dataframe.loc[i,'latlng'][0]
   payload="{"
   payload+="\"Latitude\":"
   payload+=str(latitude)
   payload+="}"
   #print(payload)
   return payload

def read_longtitude(i):
   longtitude = dataframe.loc[i,'latlng'][1]
   payload="{"
   payload+="\"Longtitude\":"
   payload+=str(longtitude)
   payload+="}"
   #print(payload)
   return payload

def read_status(str):
   status = str
   payload="{"
   payload+="\"Status\":"
   payload+=status
   payload+="}"
   #print(payload)
   return payload
# # # # # # # # # # # # # # # JSON inputs # # # # # # # # # # # # # # # # # #

#read json file
with open("trajet.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

#read data from json file
data = jsonObject['data'][0]
dataFields = data['fields']
dataValues = data['values']

#create dataframe
dataframe = pd.DataFrame(data=dataValues, index=list(range(len(dataValues))), columns=dataFields)
dataframe['time']=pd.to_datetime(dataframe['time'],unit='s')

dataframe['acceleration'] = dataframe['speed'].diff() #car il y a un relevé par seconde et la vitesse en en m/s
dataframe.loc[dataframe['acceleration'].isna()==True,'acceleration']=0 #Vérifie qu'aucune valeur ne soit NAN

#mention that the session is started
publish.single(pub_topic5, read_status("On route"), hostname = broker_address)

#publish messages to Rpi server
for j in range(len(dataframe['acceleration'])) :
#for j in range(5) :
    publish.single(pub_topic1, read_accel(j), hostname = broker_address)
    publish.single(pub_topic2, read_latitude(j), hostname = broker_address)
    publish.single(pub_topic3, read_longtitude(j), hostname = broker_address)
    publish.single(pub_topic4, read_speed(j), hostname = broker_address)

    print("Done")
#    time.sleep(1)

#mention that the session is over
publish.single(pub_topic5, read_status("Stop"), hostname = broker_address)
