#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: karencaloyannis

Simulation of the tire pressure values. 
Data was simulated for only one tire, for simplicity.

We simulate pressures measured each day, since the last inflation of the tire. 
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

# URL to get the date of the last inflation of the tires
url_revision = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/attributes/SHARED_SCOPE?keys=date_dernier_gonflage'

response = requests.get(url_revision, headers=headers)

# Parse the json response
response_json = response.json() 

for key in response_json: 
    date_dernier_gonflage = int(int(key['value'])/1000) # Récupération de la date de dernière révision

yesterday = datetime.now() - timedelta(days=1)

# Dates simulated (from the last inflation until yesterday)
dates_pression = np.arange(datetime.fromtimestamp(date_dernier_gonflage), yesterday, timedelta(days=1)).astype(datetime)
date_timestamps = []

# Convert dates to timestamps
for i in range(len(dates_pression)):  
    date_timestamps.append(int(datetime.timestamp(dates_pression[i])))
date_timestamps = np.array(date_timestamps).astype(int)

# array for tire pressure
pr_pneu1 = np.zeros((len(dates_pression),))

""" Simulate the pressure decrease 
3 types of simulation :
    1) linear decrease
    2) random decrease using exponential function
    3) decrease using a polynomial function
"""

sim = 3

if (sim == 1):
    for i in range(len(pr_pneu1)): #Sim 1 
        pr_pneu1[0] = 2.6 # initiliaze the array
        if(i>0):
            rand = np.random.uniform(low=0, high=1)*1e-2
            pr_pneu1[i] = pr_pneu1[i-1] - abs(np.random.standard_normal((1,))*rand)
    
    pr_pneu1[pr_pneu1 < 0] = 0

if (sim == 2):
    pr_exp = np.exp(np.linspace(0.95, 3, len(pr_pneu1)))
    for i in range(len(pr_pneu1)): #Sim 1 
        pr_pneu1[i] = pr_exp[i]
        if(i>0):
            rand = np.random.uniform(low=-0.5, high=1)*1e-2
            pr_pneu1[i] = pr_pneu1[i-1] - rand
    
    pr_pneu1[pr_pneu1 < 0] = 0

if (sim == 3): 
    pr_pol = np.poly1d([1, 1, 2])
    x = np.linspace(start = -1.7, stop = -1.52, num = len(pr_pneu1))
    y = pr_pol(x)
    for i in range(len(pr_pneu1)):
        rand = np.random.uniform(low=-0.2, high=0.5)
        pr_pneu1[i] = y[i] - rand 
    for i in range(len(pr_pneu1)):
        if(i>0):
            if (pr_pneu1[i] > pr_pneu1[i-1]):
                pr_pneu1[i] = pr_pneu1[i] - (pr_pneu1[i] - pr_pneu1[i-1])

print("pressure values : "+str(pr_pneu1))

# url of the maintenance device on thingsboard
url_tire='http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'

# Header
headers = {
            'Content-type': 'application/json',
}

# Send pressure values to thingsboard 
# we send the simulated timestamps of the telemetry data in the json key "ts"
for i in range(len(pr_pneu1)):
    data = '{'+'\"ts\": ' + str(int(date_timestamps[i])) + "000," + '\"values\":{\"tire\": ' + str(pr_pneu1[i]) + '}}'
    response = requests.post(url_tire, headers=headers, data=data)