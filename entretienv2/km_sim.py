#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 12:40:47 2022

@author: karencaloyannis
"""

import numpy as np
import requests

from datetime import datetime, timedelta

# préparation pour envoi vers thingsboard
# Header
headers = {
    'Content-type': 'application/json',
}
# URL thingsboard pour le device "Maintenance"
url = 'http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'


################## GENERATION DES DONNEES DE SIMULATION ###################
## Dates simulées pour le kilométrage
# On suppose qu'on commence les mesures à partir de la date de la derniere revision 
dates = np.arange(datetime(2021,1,1,23,59,59), datetime(2022,1,26,23,59,59), timedelta(days=1)).astype(datetime)
date_timestamps = []
for i in range(len(dates)):  
    date_timestamps.append(int(datetime.timestamp(dates[i])))
date_timestamps = np.array(date_timestamps).astype(int)

## simulation du kilométrage
km = np.random.normal(loc=80,scale=50,size=(len(dates),))
km_initial = 0
km = np.cumsum(km)
km = km + km_initial

# Envoi du kilometrage a thingsboard
for i in range(len(km)):
    #time.sleep(1)
    data = '{'+'\"ts\":' + str(int(date_timestamps[i])) + "000," + '\"values\":{\"kilometrage\":' + str(km[i]) + '}}'
    response = requests.post(url, headers=headers, data=data)

