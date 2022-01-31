#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 17:05:42 2022

@author: karencaloyannis
"""

import numpy as np
import requests

from datetime import datetime, timedelta

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

############# RECUPERATION DES VALEURS STOCKEES SUR THINGSBOARD #############
# Récupération du token JWT
header = {
    'Content-type': 'application/json',
    'Accept': 'application/json',
}

data = '{"username":"tenant@thingsboard.org", "password":"tenant"}'
url = 'http://localhost:8080/api/auth/login'
response = requests.post(url=url, headers=header, data=data)
response_json = response.json()
jwt_token = response_json['token'] # Token JWT

# Header
headers = {
    'Content-type': 'application/json',
    'X-Authorization': 'Bearer '+ jwt_token,
}

# URL pour récupérer la date de la dernière révision et son kilométrage
url_revision = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/attributes/SHARED_SCOPE?keys=date_derniere_vidange'

response = requests.get(url_revision, headers=headers)
response_json = response.json()

# Parser la réponse
response_json = response.json() 

for key in response_json : 
    date_derniere_vidange = int(int(key['value'])/1000) # Récupération de la date de dernière révision

# URL pour les kilométrages à récupérer 
# commande test sur terminal :
    # curl -v -X GET 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/timeseries?keys=kilometrage&startTs=1640991599000&endTs=1643151599000&agg=NONE' --header 'Content-Type:application/json' --header 'X-Authorization: Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0ZW5hbnRAdGhpbmdzYm9hcmQub3JnIiwic2NvcGVzIjpbIlRFTkFOVF9BRE1JTiJdLCJ1c2VySWQiOiI5ZjBiMTUzMC02ZTc3LTExZWMtYWM2NC04OWI1N2RkODVhYzEiLCJlbmFibGVkIjp0cnVlLCJpc1B1YmxpYyI6ZmFsc2UsInRlbmFudElkIjoiOWQ3NjFkNTAtNmU3Ny0xMWVjLWFjNjQtODliNTdkZDg1YWMxIiwiY3VzdG9tZXJJZCI6IjEzODE0MDAwLTFkZDItMTFiMi04MDgwLTgwODA4MDgwODA4MCIsImlzcyI6InRoaW5nc2JvYXJkLmlvIiwiaWF0IjoxNjQzNTQxODk4LCJleHAiOjE2NDM1NTA4OTh9.t_RlBwT_FdxrTHGPfRTyf2kz-RwcibNb838imN4HJwfOvN9EW6usAN9aplU7ObYLspzgyszkZUeVthoaOyQBQQ'
# On récupère les kilométrages depuis la dernière vidange
url_recup = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/timeseries?keys=kilometrage&startTs=' + str(date_derniere_vidange) + "000" + '&endTs=1643151599000&agg=NONE'

response = requests.get(url_recup, headers=headers)

# Parser la réponse
response_json = response.json() 

ts = [] #timestamps
km = [] #kilométrage

for key in response_json['kilometrage']:
    ts.append(int(key['ts'])/1000)
    km.append(float(key['value']))

ts = np.array(ts)
km = np.array(km)
km_derniere_vidange = np.zeros((1,))
km_derniere_vidange[0] = km[0]
print(km_derniere_vidange)


# URL pour le niveau d'huile depuis la dernière vidange
url_recup = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/timeseries?keys=oil&startTs=' + str(date_derniere_vidange) + "000" + '&endTs=1643151599000&agg=NONE'

response = requests.get(url_recup, headers=headers)

# Parser la réponse
response_json = response.json() 

ts_oil = [] #timestamps
oil = [] #kilométrage

for key in response_json['oil']:
    ts_oil.append(int(key['ts'])/1000)
    oil.append(float(key['value']))

ts_oil = np.array(ts_oil)
oil = np.array(oil)

########## REGRESSION ##############

##### Date de la prochaine Vidange #####
degree=1 #Dregee du polynome pour la régression

# modèle prédiction de la date en fonction du kilométrage
model_date_pred = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
model_date_pred.fit(km[:, np.newaxis], ts)

# Prédiction de la date de prochaine révision (on fait une révision tous les 15 000km)
date_vidange_pred = model_date_pred.predict(km_derniere_vidange[:, np.newaxis]+10000) 
print(date_vidange_pred)
next_oil_change = datetime.fromtimestamp(date_vidange_pred[0])
print("prochaine vidange:"+str(next_oil_change))

# Envoi de la date de prochaine révision vers Thingsboard 
url = 'http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'
data = '{"next_oil_change":' + str(int(date_vidange_pred[0])) + '}'
response = requests.post(url, headers=headers, data=data)


##### Prediction date à laquelle le niveau d'huile passe en-dessous du seuil ####

# Seuil du niveau d'huile en-dessous dequel il faut re-remplir ou faire une vérification
threshold_oil = np.zeros((1,))
threshold_oil[0] = 4.1

# Modèle de prédiction (linéaire)
model_oil = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
model_oil.fit(oil[:, np.newaxis], ts_oil)

# Prediction date à laquelle niveau huile < 4.1 L
# Recalculcée à chaque nouvelle mesure, à partir de la date du dernier gonflage
date_oil_pred = model_oil.predict(threshold_oil[:, np.newaxis])
date_oil_datetime = datetime.fromtimestamp(int(date_oil_pred[0]))
print("prochaine date huile:"+str(datetime.fromtimestamp(date_oil_pred[0])))

# Envoi vers thingsboard
data = '{\"date_oil\":' + str(int(date_oil_pred)) + "}"

response = requests.post(url, headers=headers, data=data)

############## Date de gonflage : envoi en modifiant le timestamp ############
## PNEU 1
data2 = '{' + '"ts":' + str(int(date_oil_pred)) + "000," + '"values":{"date_oil_timestamp": 4.1' + '}}'
response = requests.post(url, headers=headers, data=data2)

##### Prediction sur le niveau d'huile à venir ####

# modèle prédiction du kilométrage en fonction de la date
model_oil_pred = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
model_oil_pred.fit(ts_oil[:, np.newaxis], oil)
# Dates dont on veut prédire le kilométrage
dates_pred = np.arange(datetime.fromtimestamp(ts_oil[len(ts_oil)-1]), datetime.fromtimestamp(date_vidange_pred[0]), timedelta(days=1)).astype(datetime)
#Conversion en timestamps 
dates_pred_timestamps = []
for i in range(len(dates_pred)):  
    dates_pred_timestamps.append(int(datetime.timestamp(dates_pred[i])))
dates_pred_timestamps = np.array(ts).astype(int)

# niveau d'huile prédit 
oil_pred = model_oil_pred.predict(dates_pred_timestamps[:, np.newaxis])

for i in range(len(oil_pred)):
    data = '{'+'\"ts\":' + str(int(dates_pred_timestamps[i])) + "000," + '\"values\":{\"oil_pred\":' + str(oil_pred[i]) + '}}'
    response = requests.post(url, headers=headers, data=data)
