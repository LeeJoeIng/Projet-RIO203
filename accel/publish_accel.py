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
   accel = dataframe.loc[i,'acceleration'] #random modifier
   payload="{"
   payload+="\"Acceleration\":"
   payload+=str(accel)
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
dataframe['time']=pd.to_datetime(dataframe['time'],unit='s')

dataframe['acceleration'] =dataframe['speed'].diff() #car il y a un relevé par seconde et la vitesse en en m/s
dataframe.loc[dataframe['acceleration'].isna()==True,'acceleration']=0 #Vérifie qu'aucune valeur ne soit NAN

for j in range(len(dataframe['acceleration'])) :
    publish.single(pub_topic1, read_accel(j), hostname = broker_address)
    print("Done")
    time.sleep(1)
