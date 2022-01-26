#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 16:42:51 2022

@author: karencaloyannis
"""
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import requests
import sys
import time

from datetime import datetime, timedelta

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score

# Dates Simulées 
dates = np.arange(datetime(2021,12,26,23,59,59), datetime(2022,1,26,23,59,59), timedelta(days=1)).astype(datetime)
date_timestamps = []
for i in range(len(dates)):  
    date_timestamps.append(int(datetime.timestamp(dates[i])))
date_timestamps = np.array(date_timestamps).astype(int)


pr_pneu1 = np.zeros((len(dates),))
pr_pneu2 = np.zeros((len(dates),))
pr_pneu3 = np.zeros((len(dates),))
pr_pneu4 = np.zeros((len(dates),))
pf_avt_1 = np.zeros((len(dates),))
pf_arr_1 = np.zeros((len(dates),))

pr_pneu1[0] = 2.6
pr_pneu2[0] = 2.6
pr_pneu3[0] = 2.6
pr_pneu4[0] = 2.6
pf_avt_1[0] = 18
pf_arr_1[0] = 18

for i in range(len(pr_pneu1)):  
    if(i>0):
        pr_pneu1[i] = pr_pneu1[i-1] - abs(np.random.standard_normal((1,))*0.5e-2)
        pr_pneu2[i] = pr_pneu2[i-1] - abs(np.random.standard_normal((1,))*0.5e-2)
        pr_pneu3[i] = pr_pneu3[i-1] - abs(np.random.standard_normal((1,))*0.5e-2)
        pr_pneu4[i] = pr_pneu4[i-1] - abs(np.random.standard_normal((1,))*0.5e-2)
        pf_avt_1[i] = pf_avt_1[i-1] - abs(np.random.standard_normal((1,))*0.5e-2)
        pf_arr_1[i] = pf_arr_1[i-1] - abs(np.random.standard_normal((1,))*0.5e-2)

pr_pneu1[pr_pneu1 < 0] = 0


# Envoie vers thingsboard
url_tire='http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'

degree = 1
date_regonflage_pred = 0

for i in range(len(pr_pneu1)):
    
    time.sleep(1)
    if (i > 0) : 
        # PNEU 1
        pneu1_donnees = pr_pneu1[0:i] # Prendre les 40 dernières valeurs
        model_pr_pneu1 = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
        model_pr_pneu1.fit(pneu1_donnees[:, np.newaxis], date_timestamps[0:i])
        pr_pneu1_pred = np.array(pr_pneu1[0:i]) #Pression dont on doit prédire la date
        
        threshold_press = np.zeros((1,))
        threshold_press[0] = 2.4
        date_regonflage_pred = model_pr_pneu1.predict(threshold_press[:, np.newaxis])
        date_regonflage_datetime = datetime.fromtimestamp(int(date_regonflage_pred[0]))
        print("prochain gonfflage:"+str(datetime.fromtimestamp(date_regonflage_pred[0])))
        
        headers = {
            'Content-type': 'application/json',
        }
           
        data = "{\"ts\":" + str(int(date_timestamps[i])) + "000," + "\"values\":{\"tire\":" + str(pr_pneu1[i]) + "," + "\"date_gonflage\":" + str(date_regonflage_pred) + "}}"
        
        response = requests.post(url_tire, headers=headers, data=data)
        

    else:
        # PNEU 1
        pneu1_donnees = np.zeros((1,))
        pneu1_donnees[0] = pr_pneu1[0] # Prendre les 40 dernières valeurs
        model_pr_pneu1 = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
        date_timestamp = date_timestamps[0]
        model_pr_pneu1.fit(pneu1_donnees[:, np.newaxis], [date_timestamp])
        pr_pneu1_pred = np.array(pr_pneu1[0]) #Pression dont on doit prédire la date
        
        threshold_press = np.zeros((1,))
        threshold_press[0] = 2.4
        date_regonflage_pred =model_pr_pneu1.predict(threshold_press[:, np.newaxis])
        print("prochain gonfflage:"+str(datetime.fromtimestamp(date_regonflage_pred[0])))
        
        headers = {
            'Content-type': 'application/json',
        }
          
        data = '{'+'"ts":'+str(int(date_timestamps[i])) + "000," + '"values":{"tire":'+str(pr_pneu1[i])+',' +'"date_gonflage":'+ str(date_regonflage_pred) + '}}'
        
        response = requests.post(url_tire, headers=headers, data=data)
        

data2 = '{' + '"ts":' + str(int(date_regonflage_pred)) + "000," + '"values":{"date_gonflage_timestamp": 2.4' + '}}'
        
response = requests.post(url_tire, headers=headers, data=data2)

# Dates pour lesquelles on doit prédire la pression
dates_pred = np.arange(dates[0], datetime.fromtimestamp(date_regonflage_pred[0]), timedelta(days=1)).astype(datetime)

dates_pred_timestamps = []
for i in range(len(dates_pred)):  
    dates_pred_timestamps.append(datetime.timestamp(dates_pred[i]))

dates_pred_timestamps_array = np.array(dates_pred_timestamps).astype(int)
model_press_pred = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
model_press_pred.fit(date_timestamps[:, np.newaxis], pr_pneu1)
press_pred = model_press_pred.predict(dates_pred_timestamps_array[:, np.newaxis])

for i in range(len(press_pred)):
    time.sleep(1)
    
    data3 = '{'+'\"ts\":' + str(int(dates_pred_timestamps[i])) + "000," + '\"values\":{\"pression_pred\":' + str(press_pred[i]) + '}}'
        
    response = requests.post(url_tire, headers=headers, data=data3)
    
