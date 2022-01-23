#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 22:55:21 2022

@author: karencaloyannis

Modifie le .json de Steve pour mettre les valeurs mesurées pendant
le trajet en voiture

"""
import json 

# ouvrir les fichiers
with open('/Users/karencaloyannis/Downloads/streams.json') as jsonFile:
    json_karen = json.load(jsonFile)
    jsonFile.close()

with open('/Users/karencaloyannis/Downloads/Sortie_v_lo_matinale.json') as jsonFile:
    json_steve = json.load(jsonFile)
    jsonFile.close()

# prendre les valeurs qui nous intéresse dans la trace de karen
time = json_karen['time']

# ajouter un offset aux valeurs de "time" (car time a les valeurs 0, 1, ... 576)
# pour avoir des valeurs réalistes
for i in range(len(time)):
    time[i] += 1642864500

latlng = json_karen['latlng']
altitude = json_karen['altitude']
speed = json_karen['velocity_smooth']
distance = json_karen['distance']

# regarder le nombre de mesures dans le fichier de steve
data = json_steve['data']
data_0 = data[0]
measures = data_0['values']
measures_steve = len(measures)
print(len(measures))

# nombre de mesures dans le fichier de karen
measures_karen = len(time)

# remplacer les mesures de steve par les mesures de karen
for i in range(measures_karen):
    measures[i][0] = time[i]
    measures[i][1] = latlng[i]
    measures[i][2] = altitude[i]
    measures[i][4] = speed[i]
    measures[i][7] = distance[i]

# tronquer le fichier de steve
del measures[measures_karen:measures_steve]

# remplacer les mesures de steve dans le fichier .json 
index = 0;
for dic in json_steve['data']:
        index+=1
        if(index==1):
            dic['values'] = measures;

print(json_steve['data'])

# Ecrire les modiications dans le fichier original de steve
with open('/Users/karencaloyannis/Downloads/Sortie_v_lo_matinale.json', 'w') as jsonFile:
    json.dump(json_steve, jsonFile)
    
    