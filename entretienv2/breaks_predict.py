#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 15:49:25 2022

@author: karencaloyannis
"""
import numpy as np
import requests

from datetime import datetime, timedelta

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

###################### RECUPERATION DES DONNEES SUR FIT IOT et POST VERS TB ##################

url_fitiot = 'http://[2001:660:4403:486::1057]' #m3_151 

response = requests.get(url_fitiot)
break_fitiot = float(response.text)

############# TOKEN JWT #############
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


################## Récupération dernière télémétrie sur thingsboard @##########
# Header
header = {
    'Content-type': 'application/json',
    'X-Authorization': 'Bearer ' + jwt_token,
}

url_last_break = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/timeseries?keys=break1&agg=NONE'

response = requests.get(url_last_break, headers = header)
response_json = response.json()
print(response_json)

for key in response_json['break1']:
    last_break = float(key['value'])

delta = last_break - break_fitiot 
break_fitiot = break_fitiot - delta/5
print(break_fitiot)

# POST de LA NOUVELLE VALEUR A THINGSBOARD 
url_post = 'http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'

header_post = {
            'Content-type': 'application/json',
}

data_fitiot = '{\"break1\":' + str(break_fitiot) + '}'

response = requests.post(url_post, headers = header_post, data = data_fitiot)


######### RECUPERATION DES DONNEES SUR THINGSBOARD ###########

# URL pour récupérer la date de dernier changement des freins
url_revision = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/attributes/SHARED_SCOPE?keys=date_dernier_changement_freins'

response = requests.get(url_revision, headers=header)
response_json = response.json()

# Parser la réponse
response_json = response.json() 

for key in response_json : 
    date_dernier_freins = int(int(key['value'])/1000) # Récupération de la date de dernière révision

print(datetime.fromtimestamp(date_dernier_freins))

# URL pour les kilométrages à récupérer 
# commande test sur terminal :
    # curl -v -X GET 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/timeseries?keys=kilometrage&startTs=1640991599000&endTs=1643151599000&agg=NONE' --header 'Content-Type:application/json' --header 'X-Authorization: Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0ZW5hbnRAdGhpbmdzYm9hcmQub3JnIiwic2NvcGVzIjpbIlRFTkFOVF9BRE1JTiJdLCJ1c2VySWQiOiI5ZjBiMTUzMC02ZTc3LTExZWMtYWM2NC04OWI1N2RkODVhYzEiLCJlbmFibGVkIjp0cnVlLCJpc1B1YmxpYyI6ZmFsc2UsInRlbmFudElkIjoiOWQ3NjFkNTAtNmU3Ny0xMWVjLWFjNjQtODliNTdkZDg1YWMxIiwiY3VzdG9tZXJJZCI6IjEzODE0MDAwLTFkZDItMTFiMi04MDgwLTgwODA4MDgwODA4MCIsImlzcyI6InRoaW5nc2JvYXJkLmlvIiwiaWF0IjoxNjQzNTQxODk4LCJleHAiOjE2NDM1NTA4OTh9.t_RlBwT_FdxrTHGPfRTyf2kz-RwcibNb838imN4HJwfOvN9EW6usAN9aplU7ObYLspzgyszkZUeVthoaOyQBQQ'
# On récupère les kilométrages depuis la dernière révision
today = datetime.now()
today = int(datetime.timestamp(today))
url_recup = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/timeseries?keys=break1&startTs=' + str(date_dernier_freins) + "000" + '&endTs=' + str(today) + '000' + '&agg=NONE'
#url_recup =  'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/timeseries?keys=kilometrage&startTs=1640991599000&endTs=1643151599000&agg=NONE'

response = requests.get(url_recup, headers=header)

# Parser la réponse
response_json = response.json() 

ts = [] #timestamps
frein = [] #kilométrage

for key in response_json['break1']:
    ts.append(int(key['ts'])/1000)
    frein.append(float(key['value']))

ts = np.array(ts)
frein = np.array(frein)

print(ts)
print(frein)
print(len(frein))

############## REGRESSION FREINS ###################

degree = 1 # degree polynome pour prédiction

# seuil en mm
threshold_frein = np.zeros((1,))
threshold_frein[0] = 3

## FREIN 1

model_pf_avt = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
model_pf_avt.fit(frein[:, np.newaxis], ts)

# Prédiction date de changement
date_frein1 = model_pf_avt.predict(threshold_frein[:, np.newaxis])
print(date_frein1)
print("prochain changement de plaquettes de freins:"+str(datetime.fromtimestamp(date_frein1[0])))

############## Date de changement ############
headers = {
    'Content-type': 'application/json',
}

url = 'http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'

data = '{\"date_frein1\":' + str(int(date_frein1)) + '}'
response = requests.post(url, headers=headers, data=data)


############# Prédiction de l'épaisseur en fonction de la date (à tracer sur thingsboard) ###############

## FREIN 1 
# Dates pour lesquelles on doit prédire l'épaisseur'
dates_pred = np.arange(datetime.fromtimestamp(ts[len(ts)-1]), datetime.fromtimestamp(date_frein1[0]), timedelta(days=1)).astype(datetime)

# Conversion en timestamps
dates_pred_timestamps1 = []
for i in range(len(dates_pred)):  
    dates_pred_timestamps1.append(datetime.timestamp(dates_pred[i]))

dates_pred_timestamps_array = np.array(dates_pred_timestamps1).astype(int)

# Modèle pour la prédiction FREIN 1
model_frein = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
model_frein.fit(ts[:, np.newaxis], frein)
frein_pred = model_frein.predict(dates_pred_timestamps_array[:, np.newaxis])

# Envoi des données de prédiction vers Thingsboard
for i in range(len(frein_pred)):
    # Pression prédite en fonction de la date pour le PNEU 1
    data3 = '{'+'\"ts\":' + str(int(dates_pred_timestamps1[i])) + "000," + '\"values\":{\"frein_pred\":' + str(frein_pred[i]) + '}}'
    response = requests.post(url, headers=headers, data=data3)