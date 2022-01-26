#!/usr/bin/python 
#pour télécharger un paquet sur windows :  py -m pip install NomDuPaquet

import json
import time
import dateutil
import pandas as pd
import numpy as np

def iso2datetime(obj):
    d = {}
    for k,v in obj:
        if isinstance(v, str):
            try:
                d[k] = dateutil.parser.parse(v)
            except ValueError:
                d[k] = v
        else:
            d[k] = v
    return d


records = []
with open('Fichiers/trace_trajet4.json', 'r') as f:
    for d in f.readlines():
        records.append(json.loads(d, object_pairs_hook=iso2datetime))
        
df = pd.DataFrame.from_records(records) #convertion en dataframe
dfData = pd.DataFrame.from_records(df['data']) #récupère le champs 'data'
dfData0 = pd.DataFrame.from_records(dfData[0]) #récupère le premiere champs 'fields'
dfDataFields = pd.DataFrame.from_records(dfData0['fields']) #récupère les données du champs 'fields'
dfDataValues = pd.DataFrame.from_records(dfData0['values']) #recupère les valeurs

#titre de la dataframe
fieldsArray = dfDataFields.values.tolist() #conversion des titres en liste
#la liste : ["time","latlng","elevation","h_accuracy","speed","course","device_time","distance"]

#données de la dataframe
valuesArray = np.transpose(dfDataValues.to_numpy()) #transposition du tableau de valeur
tabValue = []
for i in range(len(valuesArray)) :
    tabValue.append(valuesArray[i][0]) #ajout à la liste tabValue
tabValue = np.array(tabValue, dtype=object) #conversion de la liste en array

#création de la dataframe
dataframe = pd.DataFrame(data=tabValue, index=list(range(len(tabValue))), columns=fieldsArray)

#Algo pour envoyer chaque donnée toutes les secondes
first_time = True
tabVitesse = []
for i in range(len(valuesArray)) : 
    print("*********************************")
    vitesseActuel = int(dataframe.loc[i, 'speed'].values) #en m/s
    print("Temps=" + str(i) + "s, position : "          + str((dataframe.loc[i, 'latlng'].values[0])))
    print("Temps=" + str(i) + "s, elevation : "         + str(int(dataframe.loc[i, 'elevation'].values))   + "m")
    print("Temps=" + str(i) + "s, vitesse : "           + str(int(vitesseActuel*3.6))                      + "km/h")
    print("Temps=" + str(i) + "s, distance parcouru : " + str(int(dataframe.loc[i, 'distance'].values))    + "m")
    tabVitesse.append(int(vitesseActuel*3.6))
    if first_time==False :
        accel = (vitesseActuel - vitessePrecedente)/3600
        print("Temps=" + str(i) + "s, acceleration : "  + str(accel) + "m/s²")
    else :
        first_time = False
    vitessePrecedente = int(dataframe.loc[i, 'speed'].values) #en m
    #time.sleep(1)
    
print("tabVitesse final : " + str(tabVitesse)) 









