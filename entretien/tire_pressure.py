#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 16:42:51 2022

@author: karencaloyannis

Code permettant de simuler la baisse de pression pour le 4 pneus 
et de prédire la date de gonflage 

"""
import numpy as np

import requests
import time

from datetime import datetime, timedelta

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score

# Dates Simulées pour les données sur la pression des pneus
# On suppose qu'on commence les mesures à partir de la date du dernier conflage
dates_pression = np.arange(datetime(2021,12,26,23,59,59), datetime(2022,1,26,23,59,59), timedelta(days=1)).astype(datetime)
date_timestamps = []
for i in range(len(dates_pression)):  
    date_timestamps.append(int(datetime.timestamp(dates_pression[i])))
date_timestamps = np.array(date_timestamps).astype(int)

# Pression des pneus 
pr_pneu1 = np.zeros((len(dates_pression),))
# pr_pneu2 = np.zeros((len(dates_pression),))
# pr_pneu3 = np.zeros((len(dates_pression),))
# pr_pneu4 = np.zeros((len(dates_pression),))

# Initialisation
pr_pneu1[0] = 2.6
# pr_pneu2[0] = 2.6
# pr_pneu3[0] = 2.6
# pr_pneu4[0] = 2.6

# Simulation de la baisse
for i in range(len(pr_pneu1)):  
    if(i>0):
        pr_pneu1[i] = pr_pneu1[i-1] - abs(np.random.standard_normal((1,))*0.5e-2)
        # pr_pneu2[i] = pr_pneu2[i-1] - abs(np.random.standard_normal((1,))*0.5e-2)
        # pr_pneu3[i] = pr_pneu3[i-1] - abs(np.random.standard_normal((1,))*0.5e-2)
        # pr_pneu4[i] = pr_pneu4[i-1] - abs(np.random.standard_normal((1,))*0.5e-2)

pr_pneu1[pr_pneu1 < 0] = 0
# pr_pneu2[pr_pneu2 < 0] = 0
# pr_pneu3[pr_pneu3 < 0] = 0
# pr_pneu4[pr_pneu4 < 0] = 0


# URL thingsboard pour le device "Maintenance"
url_tire='http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'

headers = {
            'Content-type': 'application/json',
}

degree = 1 # degree polynome pour prédiction
date_regonflage_pred = 0 # initialisation date de regonflage 

# Seuil de presssion en dessous duquel il faut regonfler
threshold_press = np.zeros((1,))
threshold_press[0] = 2.4

for i in range(len(pr_pneu1)):
    time.sleep(1)
    
    if (i > 0) : 
        
        ############ PNEU 1 ############
        # Modèle de prédiction (linéaire)
        pneu1_donnees = pr_pneu1[0:i]
        model_pr_pneu1 = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
        model_pr_pneu1.fit(pneu1_donnees[:, np.newaxis], date_timestamps[0:i])
        
        # Prediction date de regonflage = date à laquelle la pression passe 
        # en-dessous de 2.4 bar
        # Recalculcée à chaque nouvelle mesure, à partir de la date du dernier gonflage
        date_regonflage_pred = model_pr_pneu1.predict(threshold_press[:, np.newaxis])
        date_regonflage_datetime = datetime.fromtimestamp(int(date_regonflage_pred[0]))
        print("prochain gonfflage:"+str(datetime.fromtimestamp(date_regonflage_pred[0])))
        
        # Envoi vers thingsboard
        data = "{\"ts\":" + str(int(date_timestamps[i])) + "000," + "\"values\":{\"tire\":" + str(pr_pneu1[i]) + "," + "\"date_gonflage\":" + str(date_regonflage_pred) + "}}"
        
        response = requests.post(url_tire, headers=headers, data=data)
        
        # ############ PNEU 2 ############
        # # Modèle de prédiction (linéaire)
        # pneu2_donnees = pr_pneu2[0:i]
        # model_pr_pneu2 = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
        # model_pr_pneu2.fit(pneu2_donnees[:, np.newaxis], date_timestamps[0:i])
        
        # # Prediction date de regonflage = date à laquelle la pression passe 
        # # en-dessous de 2.4 bar
        # # Recalculcée à chaque nouvelle mesure, à partir de la date du dernier gonflage
        # date_regonflage_pred2 = model_pr_pneu2.predict(threshold_press[:, np.newaxis])
        # date_regonflage_datetime2 = datetime.fromtimestamp(int(date_regonflage_pred2[0]))
        # print("prochain gonfflage:"+str(datetime.fromtimestamp(date_regonflage_pred2[0])))
        
        # # Envoi vers thingsboard 
        # data = "{\"ts\":" + str(int(date_timestamps[i])) + "000," + "\"values\":{\"tire2\":" + str(pr_pneu2[i]) + "," + "\"date_gonflage_2\":" + str(date_regonflage_pred2) + "}}"
        
        # response = requests.post(url_tire, headers=headers, data=data)
        
        # ############ PNEU 3 ############
        # # Modèle de prédiction (linéaire)
        # pneu3_donnees = pr_pneu3[0:i]
        # model_pr_pneu3 = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
        # model_pr_pneu3.fit(pneu3_donnees[:, np.newaxis], date_timestamps[0:i])
        
        # # Prediction date de regonflage = date à laquelle la pression passe 
        # # en-dessous de 2.4 bar
        # # Recalculcée à chaque nouvelle mesure, à partir de la date du dernier gonflage
        # date_regonflage_pred3 = model_pr_pneu3.predict(threshold_press[:, np.newaxis])
        # date_regonflage_datetime3 = datetime.fromtimestamp(int(date_regonflage_pred3[0]))
        # print("prochain gonfflage:"+str(datetime.fromtimestamp(date_regonflage_pred3[0])))
        
        # # Envoi vers thingsboard    
        # data = "{\"ts\":" + str(int(date_timestamps[i])) + "000," + "\"values\":{\"tire3\":" + str(pr_pneu3[i]) + "," + "\"date_gonflage_3\":" + str(date_regonflage_pred3) + "}}"
        
        # response = requests.post(url_tire, headers=headers, data=data)
        
        # ############ PNEU 4 ############
        # # Modèle de prédiction (linéaire)
        # pneu4_donnees = pr_pneu4[0:i]
        # model_pr_pneu4 = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
        # model_pr_pneu4.fit(pneu4_donnees[:, np.newaxis], date_timestamps[0:i])
        
        # # Prediction date de regonflage = date à laquelle la pression passe 
        # # en-dessous de 2.4 bar
        # # Recalculcée à chaque nouvelle mesure, à partir de la date du dernier gonflage
        # date_regonflage_pred4 = model_pr_pneu4.predict(threshold_press[:, np.newaxis])
        # date_regonflage_datetime4 = datetime.fromtimestamp(int(date_regonflage_pred4[0]))
        # print("prochain gonfflage:"+str(datetime.fromtimestamp(date_regonflage_pred4[0])))
        
        # # Envoi vers thingsboard   
        # data = "{\"ts\":" + str(int(date_timestamps[i])) + "000," + "\"values\":{\"tire4\":" + str(pr_pneu4[i]) + "," + "\"date_gonflage_4\":" + str(date_regonflage_pred4) + "}}"
        
        # response = requests.post(url_tire, headers=headers, data=data)

    else:
        ## PNEU 1
        pneu1_donnees = np.zeros((1,))
        pneu1_donnees[0] = pr_pneu1[0] 
        
        # Modèle de prédiction (linéaire)
        model_pr_pneu1 = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
        date_timestamp = date_timestamps[0] # pour i = 0, on prend la première date dans date_timestamp
        model_pr_pneu1.fit(pneu1_donnees[:, np.newaxis], [date_timestamp])

        # Prediction date de regonflage = date à laquelle la pression passe 
        # en-dessous de 2.4 bar
        date_regonflage_pred = model_pr_pneu1.predict(threshold_press[:, np.newaxis])
        print("prochain gonfflage:"+str(datetime.fromtimestamp(date_regonflage_pred[0])))
        
        # Envoi vers thingsboard
        data = '{'+'"ts":'+str(int(date_timestamps[i])) + "000," + '"values":{"tire":'+str(pr_pneu1[i])+',' +'"date_gonflage":'+ str(date_regonflage_pred) + '}}'
        
        response = requests.post(url_tire, headers=headers, data=data)
        
        
        # ## PNEU 2
        # pneu2_donnees = np.zeros((1,))
        # pneu2_donnees[0] = pr_pneu2[0] 
        
        # # Modèle de prédiction (linéaire)
        # model_pr_pneu2 = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
        # date_timestamp = date_timestamps[0] # pour i = 0, on prend la première date dans date_timestamp
        # model_pr_pneu2.fit(pneu2_donnees[:, np.newaxis], [date_timestamp])

        # # Prediction date de regonflage = date à laquelle la pression passe 
        # # en-dessous de 2.4 bar
        # date_regonflage_pred2 = model_pr_pneu2.predict(threshold_press[:, np.newaxis])
        # print("prochain gonfflage:"+str(datetime.fromtimestamp(date_regonflage_pred2[0])))
        
        # # Envoi vers thingsboard
        # data = '{'+'"ts":'+str(int(date_timestamps[i])) + "000," + '"values":{"tire":'+str(pr_pneu2[i])+',' +'"date_gonflage2":'+ str(date_regonflage_pred2) + '}}'
        
        # response = requests.post(url_tire, headers=headers, data=data)
        
        # ## PNEU 3
        # pneu3_donnees = np.zeros((1,))
        # pneu3_donnees[0] = pr_pneu3[0] 
        
        # # Modèle de prédiction (linéaire)
        # model_pr_pneu3 = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
        # date_timestamp = date_timestamps[0] # pour i = 0, on prend la première date dans date_timestamp
        # model_pr_pneu3.fit(pneu3_donnees[:, np.newaxis], [date_timestamp])

        # # Prediction date de regonflage = date à laquelle la pression passe 
        # # en-dessous de 2.4 bar
        # date_regonflage_pred3 = model_pr_pneu3.predict(threshold_press[:, np.newaxis])
        # print("prochain gonfflage:"+str(datetime.fromtimestamp(date_regonflage_pred3[0])))
        
        # # Envoi vers thingsboard     
        # data = '{'+'"ts":'+str(int(date_timestamps[i])) + "000," + '"values":{"tire":'+str(pr_pneu3[i])+',' +'"date_gonflage3":'+ str(date_regonflage_pred3) + '}}'
        
        # response = requests.post(url_tire, headers=headers, data=data)
        
        
        # ## PNEU 4
        # pneu4_donnees = np.zeros((1,))
        # pneu4_donnees[0] = pr_pneu4[0] 
        
        # # Modèle de prédiction (linéaire)
        # model_pr_pneu4 = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
        # date_timestamp = date_timestamps[0] # pour i = 0, on prend la première date dans date_timestamp
        # model_pr_pneu4.fit(pneu4_donnees[:, np.newaxis], [date_timestamp])

        # # Prediction date de regonflage = date à laquelle la pression passe 
        # # en-dessous de 2.4 bar
        # date_regonflage_pred4 = model_pr_pneu4.predict(threshold_press[:, np.newaxis])
        # print("prochain gonfflage:"+str(datetime.fromtimestamp(date_regonflage_pred4[0])))
        
        # # Envoi vers thingsboard          
        # data = '{'+'"ts":'+str(int(date_timestamps[i])) + "000," + '"values":{"tire":'+str(pr_pneu4[i])+',' +'"date_gonflage4":'+ str(date_regonflage_pred4) + '}}'
        
        # response = requests.post(url_tire, headers=headers, data=data)
        

############## Date de gonflage prédite en prenant en compte l'historique 
# de toutes les valeurs mesurées à date 
## PNEU 1
data2 = '{' + '"ts":' + str(int(date_regonflage_pred)) + "000," + '"values":{"date_gonflage_timestamp": 2.4' + '}}'
response = requests.post(url_tire, headers=headers, data=data2)

# ## PNEU 2 
# data2 = '{' + '"ts":' + str(int(date_regonflage_pred2)) + "000," + '"values":{"date_gonflage_timestamp2": 2.4' + '}}'
# response = requests.post(url_tire, headers=headers, data=data2)

# ## PNEU 3 
# data2 = '{' + '"ts":' + str(int(date_regonflage_pred3)) + "000," + '"values":{"date_gonflage_timestamp3": 2.4' + '}}'
# response = requests.post(url_tire, headers=headers, data=data2)

# ## PNEU 4 
# data2 = '{' + '"ts":' + str(int(date_regonflage_pred4)) + "000," + '"values":{"date_gonflage_timestamp4": 2.4' + '}}'
# response = requests.post(url_tire, headers=headers, data=data2)



############# Prédiction de la pression en fonction de la date (à tracer sur thingsboard) ###############

## PNEU1 
# Dates pour lesquelles on doit prédire la pression
dates_pred = np.arange(dates_pression[0], datetime.fromtimestamp(date_regonflage_pred[0]), timedelta(days=1)).astype(datetime)

# Conversion en timestamps
dates_pred_timestamps1 = []
for i in range(len(dates_pred)):  
    dates_pred_timestamps1.append(datetime.timestamp(dates_pred[i]))

dates_pred_timestamps_array = np.array(dates_pred_timestamps1).astype(int)

# ## PNEU2 
# # Dates pour lesquelles on doit prédire la pression
# dates_pred = np.arange(dates_pression[0], datetime.fromtimestamp(date_regonflage_pred2[0]), timedelta(days=1)).astype(datetime)

# # Conversion en timestamps
# dates_pred_timestamps2 = []
# for i in range(len(dates_pred)):  
#     dates_pred_timestamps2.append(datetime.timestamp(dates_pred[i]))

# dates_pred_timestamps_array2 = np.array(dates_pred_timestamps2).astype(int)

# ## PNEU3
# # Dates pour lesquelles on doit prédire la pression
# dates_pred = np.arange(dates_pression[0], datetime.fromtimestamp(date_regonflage_pred3[0]), timedelta(days=1)).astype(datetime)

# # Conversion en timestamps
# dates_pred_timestamps3 = []
# for i in range(len(dates_pred)):  
#     dates_pred_timestamps3.append(datetime.timestamp(dates_pred[i]))

# dates_pred_timestamps_array3 = np.array(dates_pred_timestamps3).astype(int)

# ## PNEU4
# # Dates pour lesquelles on doit prédire la pression
# dates_pred = np.arange(dates_pression[0], datetime.fromtimestamp(date_regonflage_pred4[0]), timedelta(days=1)).astype(datetime)

# # Conversion en timestamps
# dates_pred_timestamps4 = []
# for i in range(len(dates_pred)):  
#     dates_pred_timestamps4.append(datetime.timestamp(dates_pred[i]))

# dates_pred_timestamps_array4 = np.array(dates_pred_timestamps4).astype(int)


# Modèle pour la prédiction PNEU1 
model_press_pred = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
model_press_pred.fit(date_timestamps[:, np.newaxis], pr_pneu1)
press_pred1 = model_press_pred.predict(dates_pred_timestamps_array[:, np.newaxis])

# # Modèle pour la prédiction PNEU 2 
# model_press_pred2 = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
# model_press_pred2.fit(date_timestamps[:, np.newaxis], pr_pneu2)
# press_pred2 = model_press_pred2.predict(dates_pred_timestamps_array2[:, np.newaxis])

# # Modèle pour la prédiction PNEU 3 
# model_press_pred3 = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
# model_press_pred3.fit(date_timestamps[:, np.newaxis], pr_pneu3)
# press_pred3 = model_press_pred3.predict(dates_pred_timestamps_array3[:, np.newaxis])

# # Modèle pour la prédiction PNEU 4 
# model_press_pred4 = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
# model_press_pred4.fit(date_timestamps[:, np.newaxis], pr_pneu4)
# press_pred4 = model_press_pred4.predict(dates_pred_timestamps_array4[:, np.newaxis])


# Envoi des données de prédiction vers Thingsboard
for i in range(len(press_pred1)):
    time.sleep(1)
    
    # Pression prédite en fonction de la date pour le PNEU 1
    data3 = '{'+'\"ts\":' + str(int(dates_pred_timestamps1[i])) + "000," + '\"values\":{\"pression_pred\":' + str(press_pred1[i]) + '}}'
    response = requests.post(url_tire, headers=headers, data=data3)
    
    # # Pression prédite en fonction de la date pour le PNEU 2 
    # data3 = '{'+'\"ts\":' + str(int(dates_pred_timestamps2[i])) + "000," + '\"values\":{\"pression_pred2\":' + str(press_pred2[i]) + '}}'
    # response = requests.post(url_tire, headers=headers, data=data3)
    
    # # Pression prédite en fonction de la date pour le PNEU 3 
    # data3 = '{'+'\"ts\":' + str(int(dates_pred_timestamps3[i])) + "000," + '\"values\":{\"pression_pred3\":' + str(press_pred3[i]) + '}}'
    # response = requests.post(url_tire, headers=headers, data=data3)
    
    # # Pression prédite en fonction de la date pour le PNEU 4 
    # data3 = '{'+'\"ts\":' + str(int(dates_pred_timestamps4[i])) + "000," + '\"values\":{\"pression_pred4\":' + str(press_pred4[i]) + '}}'
    # response = requests.post(url_tire, headers=headers, data=data3)