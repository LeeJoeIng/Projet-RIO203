#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 20:53:48 2022

@author: karencaloyannis
"""

import numpy as np
import requests

from datetime import datetime, timedelta

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

# URL pour récupérer la date de la dernière vidange
url_revision = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/attributes/SHARED_SCOPE?keys=date_derniere_vidange'

response = requests.get(url_revision, headers=headers)

# Parser la réponse
response_json = response.json() 
print(response_json)

for key in response_json: 
    print(key)
    date_derniere_vidange = int(int(key['value'])/1000) # Récupération de la date de dernière révision


################## GENERATION DES DONNEES DE SIMULATION ###################

## Dates simulées pour le niveau d'huile 
dates = np.arange(datetime.fromtimestamp(date_derniere_vidange), datetime(2022,1,26,23,59,59), timedelta(days=1)).astype(datetime)

date_timestamps = []
for i in range(len(dates)):  
    date_timestamps.append(int(datetime.timestamp(dates[i])))
date_timestamps = np.array(date_timestamps).astype(int)

# Niveau d'huile initial
oil = np.zeros((len(dates),))
oil[0] = 4.6

# Simulation de la baisse 
for i in range(len(oil)):
    if(i>0):
        oil[i] = oil[i-1] - abs(np.random.standard_normal((1,))*0.1e-2)

# URL thingsboard pour le device "Maintenance"
url='http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'

# Envoi vers thingsboard
headers = {
    'Content-type': 'application/json',
}

for i in range(len(oil)):
    data = '{'+'\"ts\":' + str(int(date_timestamps[i])) + "000," + '\"values\":{\"oil\":' + str(oil[i]) + '}}'
    response = requests.post(url, headers=headers, data=data)