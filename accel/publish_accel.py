#!/usr/bin/env python3

import json
import time
import pandas as pd
import paho.mqtt.publish as publish

broker_address = "test.mosquitto.org"

# publish messages on these topics
pub_topic1 = "rio203/accelerationFromJSON"

# # # # # # # # # # # # # # # Preparing payload # # # # # # # # # # # # # # # # # #

def read_accel(i):
   accel = acceleration[i] #random modifier
   payload="{"
   payload+="\"Acceleration\":"
   payload+=accel
   payload+=";"
   payload+="}"
   print(payload)
   return payload

# # # # # # # # # # # # # # # JSON inputs # # # # # # # # # # # # # # # # # #

#read json file
with open("Sortie_v_lo_matinale.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

#read data from json file
data = jsonObject['data'][0]
dataFields = data['fields']
dataValues = data['values']

#create dataframe
dataframe = pd.DataFrame(data=dataValues, index=list(range(len(dataValues))), columns=dataFields)

# Declare a list that is to be converted into a column
acceleration = []

#Algo pour envoyer chaque donnée toutes les secondes
first_time = True
for i in range(len(dataframe)) :
    if first_time==False :
        vitesseActuel = float(dataframe.loc[i, 'speed'])*1000 #en m
        accel = (vitesseActuel - vitessePrecedente)/3600
        acceleration.append(str(accel))

    else :
        first_time = False
        acceleration.append('0')
    vitessePrecedente = float(dataframe.loc[i, 'speed'])*1000 #en m

for j in range(len(acceleration)) :
    publish.single(pub_topic1, read_accel(j), hostname = broker_address)
    print("Done")
    time.sleep(1)
