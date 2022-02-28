#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Karen Caloyannis

Simulation of the brake pad thickness.

"""

import numpy as np
import requests

from datetime import datetime, timedelta

########### GET data from thingsboard, used for the simulation #############
header = {
    'Content-type': 'application/json',
    'Accept': 'application/json',
}

data = '{"username":"tenant@thingsboard.org", "password":"tenant"}'
url = 'http://localhost:8080/api/auth/login'
response = requests.post(url=url, headers=header, data=data)
response_json = response.json()
jwt_token = response_json['token'] # JWT Token

# Header
headers = {
    'Content-type': 'application/json',
    'X-Authorization': 'Bearer ' + jwt_token,
}

# URL to get the date of the last change of the brake pads (from the last oil change until yesterday)
url_revision = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/attributes/SHARED_SCOPE?keys=date_dernier_changement_freins'

response = requests.get(url_revision, headers=headers)

# Parse the response
response_json = response.json() 

for key in response_json: 
    date_dernier_freins = int(int(key['value'])/1000) # date of the last change of the brake pad

# Generate the timestamps of the measurements
yesterday = datetime.now() - timedelta(days=1)
dates = np.arange(datetime.fromtimestamp(date_dernier_freins), yesterday, timedelta(days=1)).astype(datetime)
date_timestamps = []
for i in range(len(dates)):  
    date_timestamps.append(int(datetime.timestamp(dates[i])))
date_timestamps = np.array(date_timestamps).astype(int)

brake = np.zeros((len(dates),)) #brake pad thickness

# Simulate the decrease of the thickness - Chose the simulation
sim = 2

if(sim == 1): # linear decrease
    random = np.random.uniform(low=-0.1, high=0.1, size = len(brake))
    random[random<0] = 0
    random = np.cumsum(random)
    brake = 18 - random
    brake[brake<0] = 0
if(sim == 2): # Polynomial decrease
    polynome = np.poly1d([0.1, 1, -1, 10])
    x = np.linspace(start = -3.2, stop = -0.5, num = len(brake))
    y = polynome(x)
    for i in range(len(brake)):
        rand = np.random.uniform(low=-0.5, high=0.5)
        brake[i] = y[i] - rand 
    for i in range(len(brake)):
        if(i>0):
            if (brake[i] > brake[i-1]):
                brake[i] = brake[i] - (brake[i] - brake[i-1])
                

# URL of th maintenance device
url='http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'

# POST the simulated data to thingsboard
headers = {
    'Content-type': 'application/json',
}

for i in range(len(brake)):
    # Replace the timestamps of the telemetry by the simulated timestamps
    data = '{'+'\"ts\":' + str(int(date_timestamps[i])) + "000," + '\"values\":{\"brake\":' + str(brake[i]) + '}}'
    response = requests.post(url, headers=headers, data=data)