#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 14:09:32 2022

@author: karencaloyannis
"""
import numpy as np
import requests

from datetime import datetime, timedelta

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

########### RECUPERATION DES DONNEES SUR THINGSBOARD #############
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
    'X-Authorization': 'Bearer ' + jwt_token,
}

# URL pour récupérer la date de dernier gonflage
url_revision = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/attributes/SHARED_SCOPE?keys=date_dernier_gonflage'

response = requests.get(url_revision, headers=headers)

# Parser la réponse
response_json = response.json() 

for key in response_json: 
    print(key)
    date_dernier_gonflage = int(int(key['value'])/1000) # Récupération de la date de dernière révision
print(str(datetime.fromtimestamp(date_dernier_gonflage )))
print(date_dernier_gonflage)

# URL pour les pressions à récupérer
# commande test sur terminal :
    # curl -v -X GET 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/timeseries?keys=tire&startTs=1640991599000&endTs=1643151599000&agg=NONE' --header 'Content-Type:application/json' --header 'X-Authorization: Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0ZW5hbnRAdGhpbmdzYm9hcmQub3JnIiwic2NvcGVzIjpbIlRFTkFOVF9BRE1JTiJdLCJ1c2VySWQiOiI5ZjBiMTUzMC02ZTc3LTExZWMtYWM2NC04OWI1N2RkODVhYzEiLCJlbmFibGVkIjp0cnVlLCJpc1B1YmxpYyI6ZmFsc2UsInRlbmFudElkIjoiOWQ3NjFkNTAtNmU3Ny0xMWVjLWFjNjQtODliNTdkZDg1YWMxIiwiY3VzdG9tZXJJZCI6IjEzODE0MDAwLTFkZDItMTFiMi04MDgwLTgwODA4MDgwODA4MCIsImlzcyI6InRoaW5nc2JvYXJkLmlvIiwiaWF0IjoxNjQzNTQxODk4LCJleHAiOjE2NDM1NTA4OTh9.t_RlBwT_FdxrTHGPfRTyf2kz-RwcibNb838imN4HJwfOvN9EW6usAN9aplU7ObYLspzgyszkZUeVthoaOyQBQQ'
# On récupère les kilométrages depuis la dernière révision
url_recup = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/timeseries?keys=tire&startTs=' + str(date_dernier_gonflage) + '000' + '&endTs=1643151599000&agg=NONE'
#url_recup =  'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/timeseries?keys=kilometrage&startTs=1640991599000&endTs=1643151599000&agg=NONE'

response = requests.get(url_recup, headers=headers)
print(response.json())

# Parser la réponse
response_json = response.json() 

ts = [] #timestamps
pression = [] #kilométrage

for key in response_json['tire']:
    ts.append(int(key['ts'])/1000)
    pression.append(float(key['value']))

ts = np.array(ts)
pression = np.array(pression)

###################### REGRESSION PRESSION #############################

# URL thingsboard pour le device "Maintenance"
url_tire='http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'

headers = {
            'Content-type': 'application/json',
}

# Seuil de presssion en dessous duquel il faut regonfler
threshold_press = np.zeros((1,))
threshold_press[0] = 2.4

degree = 1 # degree polynome pour prédiction

############ PNEU 1 ############
# Modèle de prédiction (linéaire)
model_pr_pneu1 = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
model_pr_pneu1.fit(pression[:, np.newaxis], ts)

# Prediction date de regonflage = date à laquelle la pression passe 
# en-dessous de 2.4 bar
# Recalculcée à chaque nouvelle mesure, à partir de la date du dernier gonflage
date_regonflage_pred = model_pr_pneu1.predict(threshold_press[:, np.newaxis])
date_regonflage_datetime = datetime.fromtimestamp(int(date_regonflage_pred[0]))
print("prochain gonfflage:"+str(datetime.fromtimestamp(date_regonflage_pred[0])))

# Envoi vers thingsboard
data = '{\"date_gonflage\":' + str(int(date_regonflage_pred)) + "}"

response = requests.post(url_tire, headers=headers, data=data)


############## Date de gonflage : envoi en modifiant le timestamp ############
## PNEU 1
data2 = '{' + '"ts":' + str(int(date_regonflage_pred)) + "000," + '"values":{"date_gonflage_timestamp": 2.4' + '}}'
response = requests.post(url_tire, headers=headers, data=data2)


############# Prédiction de la pression en fonction de la date (à tracer sur thingsboard) ###############
## PNEU1 
# Dates pour lesquelles on doit prédire la pression
dates_pred = np.arange(datetime.fromtimestamp(ts[len(ts)-1]), datetime.fromtimestamp(date_regonflage_pred[0]), timedelta(days=1)).astype(datetime)
print(dates_pred)
# Conversion en timestamps
dates_pred_timestamps = []
for i in range(len(dates_pred)):  
    dates_pred_timestamps.append(datetime.timestamp(dates_pred[i]))

dates_pred_timestamps_array = np.array(dates_pred_timestamps).astype(int)

print(len(dates_pred_timestamps_array ))

# Modèle pour la prédiction PNEU1 
model_press_pred = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
model_press_pred.fit(ts[:, np.newaxis], pression)
press_pred1 = model_press_pred.predict(dates_pred_timestamps_array[:, np.newaxis])


# Envoi des données de prédiction vers Thingsboard
for i in range(len(press_pred1)):
    
    # Pression prédite en fonction de la date pour le PNEU 1
    data3 = '{'+'\"ts\":' + str(int(dates_pred_timestamps[i])) + "000," + '\"values\":{\"pression_pred\":' + str(press_pred1[i]) + '}}'
    response = requests.post(url_tire, headers=headers, data=data3)
