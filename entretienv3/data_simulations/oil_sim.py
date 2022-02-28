#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Karen Caloyannis

Simulation of the oil levels.

"""

import numpy as np
import requests

from datetime import datetime, timedelta

########### GET data from thingsboard, used for the simulation #############
# GET the JWT Token
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

# URL pour get the date of the last oil change
url_revision = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/attributes/SHARED_SCOPE?keys=date_derniere_vidange'

response = requests.get(url_revision, headers=headers)

# Parser the response
response_json = response.json() 

for key in response_json: 
    print(key)
    date_derniere_vidange = int(int(key['value'])/1000) # date of the last oil change


# Generate the timestamps of the measurements (from the last oil change until yesterday)
yesterday = datetime.now() - timedelta(days=1)
dates = np.arange(datetime.fromtimestamp(date_derniere_vidange), yesterday, timedelta(days=1)).astype(datetime)

date_timestamps = []
for i in range(len(dates)):  
    date_timestamps.append(int(datetime.timestamp(dates[i])))
date_timestamps = np.array(date_timestamps).astype(int)

# Initialize oil level
oil = np.zeros((len(dates),))
oil[0] = 4.6

# Simulation the oil level decrease
sim = 1

if(sim == 1):
    for i in range(len(oil)):
        if(i>0):
            oil[i] = oil[i-1] - abs(np.random.standard_normal((1,))*0.6e-2)
if(sim == 2):
    pr_pol = np.poly1d([1, 1, 2])
    x = np.linspace(start = -2, stop = -1.8, num = len(oil))
    y = pr_pol(x)
    for i in range(len(oil)):
        rand = np.random.uniform(low=0, high=0.1)
        oil[i] = y[i] - rand 
    for i in range(len(oil)):
        if(i>0):
            if (oil[i] > oil[i-1]):
                oil[i] = oil[i] - (oil[i] - oil[i-1])

# URL of the maintenance device
url='http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'

# POST the simulated data to thingsboard
headers = {
    'Content-type': 'application/json',
}

for i in range(len(oil)):
    # Replace the timestamps of the telemetry by the simulated timestamps
    data = '{'+'\"ts\":' + str(int(date_timestamps[i])) + "000," + '\"values\":{\"oil\":' + str(oil[i]) + '}}'
    response = requests.post(url, headers=headers, data=data)