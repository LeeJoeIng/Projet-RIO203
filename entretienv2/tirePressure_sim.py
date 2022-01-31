#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 13:54:47 2022

@author: karencaloyannis
"""
import numpy as np

import requests

from datetime import datetime, timedelta

# Dates Simulées pour les données sur la pression des pneus

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
print(response_json['token'])
jwt_token = response_json['token'] # Token JWT
print(jwt_token)

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
print(response_json)

for key in response_json: 
    print(key)
    date_dernier_gonflage = int(int(key['value'])/1000) # Récupération de la date de dernière révision

dates_pression = np.arange(datetime.fromtimestamp(date_dernier_gonflage), datetime(2022,1,26,23,59,59), timedelta(days=1)).astype(datetime)
print(dates_pression)
date_timestamps = []
for i in range(len(dates_pression)):  
    date_timestamps.append(int(datetime.timestamp(dates_pression[i])))
date_timestamps = np.array(date_timestamps).astype(int)

# Pression des pneus 
pr_pneu1 = np.zeros((len(dates_pression),))

# Initialisation
pr_pneu1[0] = 2.6

# Simulation de la baisse
for i in range(len(pr_pneu1)):  
    if(i>0):
        pr_pneu1[i] = pr_pneu1[i-1] - abs(np.random.standard_normal((1,))*0.5e-2)

pr_pneu1[pr_pneu1 < 0] = 0

# URL thingsboard pour le device "Maintenance"
url_tire='http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'

headers = {
            'Content-type': 'application/json',
}

# Envoi des pression à thingsboard
for i in range(len(pr_pneu1)):
    data = '{'+'\"ts\": ' + str(int(date_timestamps[i])) + "000," + '\"values\":{\"tire\": ' + str(pr_pneu1[i]) + '}}'
    print(data)
    response = requests.post(url_tire, headers=headers, data=data)
    print(response)