#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 15:43:48 2022

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

# URL pour récupérer la date du dernier changement des plaquettes de frein
url_revision = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/attributes/SHARED_SCOPE?keys=date_dernier_changement_freins'

response = requests.get(url_revision, headers=headers)

# Parser la réponse
response_json = response.json() 
print(response_json)

for key in response_json: 
    print(key)
    date_dernier_freins = int(int(key['value'])/1000) # Récupération de la date de dernière révision


# Dates Simulées pour les données sur la pression des pneus
# On suppose qu'on commence les mesures à partir de la date du dernier changement
dates = np.arange(datetime.fromtimestamp(date_dernier_freins), datetime(2022,1,26,23,59,59), timedelta(days=1)).astype(datetime)
date_timestamps = []
for i in range(len(dates)):  
    date_timestamps.append(int(datetime.timestamp(dates[i])))
date_timestamps = np.array(date_timestamps).astype(int)

# Epaisseur plaquettes de frein
pf_1 = np.zeros((len(dates),))

pf_1[0] = 18

# Simulation de la baisse 
for i in range(len(pf_1)):
    if(i>0):
        pf_1[i] = pf_1[i-1] - abs(np.random.standard_normal((1,))*0.5e-2)

# URL thingsboard pour le device "Maintenance"
url='http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'

# Envoi vers thingsboard
headers = {
    'Content-type': 'application/json',
}

for i in range(len(pf_1)):
    data = '{'+'\"ts\":' + str(int(date_timestamps[i])) + "000," + '\"values\":{\"break1\":' + str(pf_1[i]) + '}}'
    response = requests.post(url, headers=headers, data=data)