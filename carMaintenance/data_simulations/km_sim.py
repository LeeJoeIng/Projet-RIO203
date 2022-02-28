#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: karencaloyannis

Simulation of the mileage values. 

We simulate the values retrieved from the mileometer everyday, since
the last car maintenance.
"""

import numpy as np
import requests
from datetime import datetime, timedelta

########### GET data from thingsboard, used for the simulation #############
# Get the JWT Token
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

# URL to get the date of the last maintenance
url_revision = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/attributes/SHARED_SCOPE?keys=date_derniere_revision'

response = requests.get(url_revision, headers=headers)

# Parse the response
response_json = response.json() 

for key in response_json: 
    date_derniere_revision = int(int(key['value'])/1000) # date of the last car maintenance

################################# Simulation #################################
# Generate the timestamps (from the last maintenance until yesterday)
yesterday = datetime.now() - timedelta(days=1)
dates = np.arange(datetime.fromtimestamp(date_derniere_revision), yesterday, timedelta(days=1)).astype(datetime)
date_timestamps = []

# Conversion from datetimeto timestamps
for i in range(len(dates)):  
    date_timestamps.append(int(datetime.timestamp(dates[i])))
date_timestamps = np.array(date_timestamps).astype(int)

## Simulation of mileage values
sim = 1
if(sim == 1): # Simulation using gaussian distribution : mileage is picked randomly with mean = 150km & scale=200km
    print("gaussian simulation")  
    km = np.random.normal(loc=150,scale=200,size=(len(dates),))
    km = np.cumsum(km)
    
if(sim == 2): # Simulation using uniform distribution : mileage is picked randomly between 0 & 200 km
    print("uniform simulation")    
    km = np.random.uniform(low=0,high=200,size=(len(dates),))
    km = np.cumsum(km)
    
if(sim == 3): # Simulating when the car is not in service for several days
    km = np.random.uniform(low=-300,high=230,size=(len(dates),))
    km[km < 0] = 0
    km[150:160] = 0 # days when car is not in service
    km[170:200] = 0
    km[201:210] = 0
    km[300:350] = 0
    km = np.cumsum(km)
    
if(sim == 4): # Polynomial simulation
    print("polynomial simulation")  
    km = np.zeros(len(dates))
    km_pol = np.poly1d([0.001, 0.001, 0])
    x = np.linspace(start = 0, stop = 6, num = len(km))
    y = km_pol(x)
    for i in range(len(km)):
        rand = np.random.uniform(low=-100, high=100)
        km[i] = y[i] + rand
    km = np.cumsum(km)
    km[km<0] = np.random.uniform(low=0, high = 100)
    km = np.cumsum(km)
    print(km)

######################### Post telemetry to thingsboard #######################
# Header
headers = {
    'Content-type': 'application/json',
}
# URL of the maintenance device
url = 'http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'

for i in range(len(km)):
    data = '{'+'\"ts\":' + str(int(date_timestamps[i])) + "000," + '\"values\":{\"kilometrage\":' + str(km[i]) + '}}'
    response = requests.post(url, headers=headers, data=data)

