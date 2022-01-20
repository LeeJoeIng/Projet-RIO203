#!/usr/bin/env python3

import json
import time
import pandas as pd

with open("Sortie_v_lo_matinale.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

data = jsonObject['data'][0]
dataFields = data['fields']
dataValues = data['values'] 

#print(dataFields)
#['time', 'latlng', 'elevation', 'h_accuracy', 'speed', 'course', 'device_time', 'distance']
#print(dataValues[0])
#[1569136049, [48.74496746916384, 2.282407478692314], 105.00115753896534, 25.048748, 8.025881, 237.03848, 1569136047.324, 0]

dataframe = pd.DataFrame(data=dataValues, index=list(range(len(dataValues))), columns=dataFields)
pd.set_option("display.max_rows", None, "display.max_columns", None)
dataframe['time']=pd.to_datetime(dataframe['time'],unit='s') #converti le temps en donnée en datetime
#print(dataframe.head(5))


#print(len(dataValues)) 

#Algo pour envoyer chaque donnée toutes les secondes

# for i in range(len(dataframe)) : 
    #print("*********************************")
    #print("Temps=" + str(i) + "s, position : "          + str((dataframe.loc[i, 'latlng'])))
    #print("Temps=" + str(i) + "s, elevation : "         + str(float(dataframe.loc[i, 'elevation'])) + "m")
    #print("Temps=" + str(i) + "s, vitesse : "           + str(float(dataframe.loc[i, 'speed']))     + "km/h")
    #print("Temps=" + str(i) + "s, distance parcouru : " + str(int(dataframe.loc[i, 'distance']))    + "m")
   # time.sleep(1)


dataframe['acceleration'] =dataframe['speed'].diff() #car il y a un relevé par seconde et la vitesse en en m/s
dataframe.loc[dataframe['acceleration'].isna()==True,'acceleration']=0 #Vérifie qu'aucune valeur ne soit NAN
#print(dataframe[['time','acceleration']])
#print(dataframe.head(5))
dataframe=dataframe.loc[:,['time','latlng','speed','acceleration']] #création d'un dataframe avec uniquement les données utiles
dataframe
