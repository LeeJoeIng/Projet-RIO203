#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 20:53:58 2022

@author: karencaloyannis
"""

import numpy as np

import requests
import time

from datetime import datetime, timedelta

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

# Dates Simulées pour les données sur la pression des pneus
# On suppose qu'on commence les mesures à partir de la date du dernier changement
dates = np.arange(datetime(2021,12,26,23,59,59), datetime(2022,1,26,23,59,59), timedelta(days=7)).astype(datetime)
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
url_tire='http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'

# Envoi vers thingsboard
headers = {
    'Content-type': 'application/json',
}

degree = 1 # degree polynome pour prédiction

# seuil en mm
threshold_frein = np.zeros((1,))
threshold_frein[0] = 3

############## REGRESSION FREINS ###################

for i in range(len(pf_1)):
    
    if (i > 0) : 
        
        ## FREIN 1
        pf1_donnees = pf_1[0:i]
        
        model_pf_avt = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
        model_pf_avt.fit(pf1_donnees[:, np.newaxis], date_timestamps[0:i])
        
        # Prédiction date de changement
        date_frein1 = model_pf_avt.predict(threshold_frein[:, np.newaxis])
        print("prochain changement de plaquettes de freins:"+str(datetime.fromtimestamp(date_frein1[0])))
   
        # Envoi vers thingsboard          
        data = '{'+'"ts":'+str(int(date_timestamps[i])) + "000," + '"values":{"break1":'+str(pf_1[i])+',' +'"date_frein1":'+ str(date_frein1) + '}}'
        response = requests.post(url_tire, headers=headers, data=data)
    
    else:
        
        ## FREIN 1
        pf1_donnees = np.zeros((1,))
        pf1_donnees[0] = pf_1[0]
        
        model_pf_avt = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
        date_timestamp = np.zeros((1,))
        date_timestamp[0] = date_timestamps[0]
        model_pf_avt.fit(pf1_donnees[:, np.newaxis], date_timestamp)
        
        # Prédiction date de changement
        date_frein1 = model_pf_avt.predict(threshold_frein[:, np.newaxis])
        print("prochain changement de plaquettes de freins:"+str(datetime.fromtimestamp(date_frein1[0])))
   
        # Envoi vers thingsboard          
        data = '{'+'"ts":'+str(int(date_timestamps[i])) + "000," + '"values":{"break1":'+str(pf_1[i])+',' +'"date_frein1":'+ str(date_frein1) + '}}'
        response = requests.post(url_tire, headers=headers, data=data)


############# Prédiction de l'épaisseur en fonction de la date (à tracer sur thingsboard) ###############

## FREIN 1 
# Dates pour lesquelles on doit prédire la pression
dates_pred = np.arange(dates[0], datetime.fromtimestamp(date_frein1[0]), timedelta(days=1)).astype(datetime)

# Conversion en timestamps
dates_pred_timestamps1 = []
for i in range(len(dates_pred)):  
    dates_pred_timestamps1.append(datetime.timestamp(dates_pred[i]))

dates_pred_timestamps_array = np.array(dates_pred_timestamps1).astype(int)

# Modèle pour la prédiction FREIN 1
model_frein = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
model_frein.fit(date_timestamps[:, np.newaxis], pf_1)
press_frein = model_frein.predict(dates_pred_timestamps_array[:, np.newaxis])

# Envoi des données de prédiction vers Thingsboard
for i in range(len(press_frein)):
    # Pression prédite en fonction de la date pour le PNEU 1
    data3 = '{'+'\"ts\":' + str(int(dates_pred_timestamps1[i])) + "000," + '\"values\":{\"pression_pred\":' + str(press_frein[i]) + '}}'
    response = requests.post(url_tire, headers=headers, data=data3)