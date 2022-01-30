#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 19:58:37 2022

@author: karencaloyannis

Code permettant de simuler le kilométrage relevé et 
de prédire la date de revision.

On verra comment faire la date de contrôle et de validité
directement sur thingsboard (pas de besoin de prédiction pour
ces données)
    
"""

import numpy as np
import time
import requests

from datetime import datetime, timedelta

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

# préparation pour envoi vers thingsboard
# Header
headers = {
    'Content-type': 'application/json',
}
# URL thingsboard pour le device "Maintenance"
url_tire='http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'

################## GENERATION DES DONNEES DE SIMULATION ###################
## Dates simulées pour le kilométrage
# On suppose qu'on commence les mesures à partir de la date de la derniere revision 
dates = np.arange(datetime(2021,11,20,23,59,59), datetime(2022,1,26,23,59,59), timedelta(days=1)).astype(datetime)
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
    response = requests.post(url_tire, headers=headers, data=data)

# kilométrage à la dernière révision
km_derniere_revision = np.zeros((1,))
km_derniere_revision[0] = km[0]

# Date dernière révision => valeur à récupérer sur thingsboard ? 
derniere_revision_timestamp = np.zeros((1,))
derniere_revision_timestamp[0] = date_timestamps[0]


############## REGRESSION KILOMETRAGE ###################

degree=1 #Dregee du polynome pour la régression

# modèle prédiction de la date en fonction du kilométrage
model_date_pred = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
model_date_pred.fit(km[:, np.newaxis], date_timestamps)

# Prédiction de la date de prochaine révision (on fait une révision tous les 15 000km)
date_revision_pred = model_date_pred.predict(km_derniere_revision[:, np.newaxis]+15000) 
next_service = datetime.fromtimestamp(date_revision_pred[0])
print("prochaine révision:"+str(next_service))

# Envoi de la date de prochaine révision vers Thingsboard 
data = '{"next_service":' + str(int(date_revision_pred[0])) + '}'
response = requests.post(url_tire, headers=headers, data=data)


############# PREDICTION DU KILOMETRAGE EN FONCTION DE LA DATE ##############
# modèle prédiction du kilométrage en fonction de la date
model_km_pred = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
model_km_pred.fit(date_timestamps[:, np.newaxis], km)
# Dates dont on veut prédire le kilométrage
dates_pred = np.arange(datetime(2021,11,20,23,59,59), datetime.fromtimestamp(date_revision_pred[0]), timedelta(days=1)).astype(datetime)
#Conversion en timestamps 
dates_pred_timestamps = []
for i in range(len(dates)):  
    dates_pred_timestamps.append(int(datetime.timestamp(dates_pred[i])))
dates_pred_timestamps = np.array(date_timestamps).astype(int)

# kilometrage prédit
km_pred = model_km_pred.predict(dates_pred_timestamps[:, np.newaxis])

for i in range(len(km_pred)):
    time.sleep(1)
    
    data = '{'+'\"ts\":' + str(int(dates_pred_timestamps[i])) + "000," + '\"values\":{\"kilometrage_pred\":' + str(km_pred[i]) + '}}'
    response = requests.post(url_tire, headers=headers, data=data)

