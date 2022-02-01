#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 12:40:58 2022

@author: karencaloyannis
"""
import numpy as np
import requests

from datetime import datetime, timedelta

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

###################### RECUPERATION DES DONNEES SUR FIT IOT et POST VERS TB ##################

url_fitiot = 'http://[2001:660:4403:486::1057]' #m3_149 

response = requests.get(url_fitiot)
km_fitiot = float(response.text)

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

url_last_tire = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/timeseries?keys=kilometrage&agg=NONE'

response = requests.get(url_last_tire, headers = header)
response_json = response.json()
print(response_json)

for key in response_json['kilometrage']:
    last_km = float(key['value'])
km_fitiot = km_fitiot + last_km
print(km_fitiot)

# POST de LA NOUVELLE VALEUR A THINGSBOARD 
url_post = 'http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'

header_post = {
            'Content-type': 'application/json',
}

data_fitiot = '{\"kilometrage\":' + str(km_fitiot) + '}'

response = requests.post(url_post, headers = header_post, data = data_fitiot)



############################ RECUPERATION DE L'HISTORIQUE SUR THINGSBOARD ###################

# Header
headers = {
    'Content-type': 'application/json',
    'X-Authorization': 'Bearer '+ jwt_token,
}

# URL pour récupérer la date de la dernière révision et son kilométrage
url_revision = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/attributes/SHARED_SCOPE?keys=date_derniere_revision'

response = requests.get(url_revision, headers=headers)
response_json = response.json()

# Parser la réponse
response_json = response.json() 

for key in response_json : 
    date_derniere_revision = int(int(key['value'])/1000) # Récupération de la date de dernière révision

# URL pour les kilométrages à récupérer 
# commande test sur terminal :
    # curl -v -X GET 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/timeseries?keys=kilometrage&startTs=1640991599000&endTs=1643151599000&agg=NONE' --header 'Content-Type:application/json' --header 'X-Authorization: Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0ZW5hbnRAdGhpbmdzYm9hcmQub3JnIiwic2NvcGVzIjpbIlRFTkFOVF9BRE1JTiJdLCJ1c2VySWQiOiI5ZjBiMTUzMC02ZTc3LTExZWMtYWM2NC04OWI1N2RkODVhYzEiLCJlbmFibGVkIjp0cnVlLCJpc1B1YmxpYyI6ZmFsc2UsInRlbmFudElkIjoiOWQ3NjFkNTAtNmU3Ny0xMWVjLWFjNjQtODliNTdkZDg1YWMxIiwiY3VzdG9tZXJJZCI6IjEzODE0MDAwLTFkZDItMTFiMi04MDgwLTgwODA4MDgwODA4MCIsImlzcyI6InRoaW5nc2JvYXJkLmlvIiwiaWF0IjoxNjQzNTQxODk4LCJleHAiOjE2NDM1NTA4OTh9.t_RlBwT_FdxrTHGPfRTyf2kz-RwcibNb838imN4HJwfOvN9EW6usAN9aplU7ObYLspzgyszkZUeVthoaOyQBQQ'
# On récupère les kilométrages depuis la dernière révision
today = datetime.now()
today = int(datetime.timestamp(today))
url_recup = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/timeseries?keys=kilometrage&startTs=' + str(date_derniere_revision) + "000" + '&endTs=1'+ str(today) + '000' + '&agg=NONE'
#url_recup =  'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/timeseries?keys=kilometrage&startTs=1640991599000&endTs=1643151599000&agg=NONE'

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
km_derniere_revision = np.zeros((1,))
km_derniere_revision[0] = km[0]
print(km_derniere_revision)


############## REGRESSION KILOMETRAGE ###################

degree=1 #Dregee du polynome pour la régression

# modèle prédiction de la date en fonction du kilométrage
model_date_pred = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
model_date_pred.fit(km[:, np.newaxis], ts)

# Prédiction de la date de prochaine révision (on fait une révision tous les 15 000km)
date_revision_pred = model_date_pred.predict(km_derniere_revision[:, np.newaxis]+15000) 
print(date_revision_pred)
next_service = datetime.fromtimestamp(date_revision_pred[0])
print("prochaine révision:"+str(next_service))

# Envoi de la date de prochaine révision vers Thingsboard 
url = 'http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'
data = '{"next_service":' + str(int(date_revision_pred[0])) + '}'
response = requests.post(url, headers=headers, data=data)


############# PREDICTION DU KILOMETRAGE EN FONCTION DE LA DATE ##############
# modèle prédiction du kilométrage en fonction de la date
model_km_pred = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
model_km_pred.fit(ts[:, np.newaxis], km)
# Dates dont on veut prédire le kilométrage
dates_pred = np.arange(datetime.fromtimestamp(ts[len(ts)-1]), datetime.fromtimestamp(date_revision_pred[0]), timedelta(days=1)).astype(datetime)
#Conversion en timestamps 
dates_pred_timestamps = []
for i in range(len(dates_pred)):  
    dates_pred_timestamps.append(int(datetime.timestamp(dates_pred[i])))
dates_pred_timestamps = np.array(ts).astype(int)

# kilometrage prédit
km_pred = model_km_pred.predict(dates_pred_timestamps[:, np.newaxis])

for i in range(len(km_pred)):
    data = '{'+'\"ts\":' + str(int(dates_pred_timestamps[i])) + "000," + '\"values\":{\"kilometrage_pred\":' + str(km_pred[i]) + '}}'
    response = requests.post(url, headers=headers, data=data)
