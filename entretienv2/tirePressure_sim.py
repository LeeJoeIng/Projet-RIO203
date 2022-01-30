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
dates_pression = np.arange(datetime(2021,1,1,23,59,59), datetime(2022,1,26,23,59,59), timedelta(days=1)).astype(datetime)
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
    data = '{'+'\"ts\":' + str(int(date_timestamps[i])) + "000," + '\"values\":{\"tire\":' + str(pr_pneu1[i]) + '}}'
    response = requests.post(url_tire, headers=headers, data=data)