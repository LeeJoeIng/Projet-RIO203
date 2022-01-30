#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 22:45:46 2022

@author: karencaloyannis
"""

import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import requests
import subprocess

from datetime import datetime, timedelta

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score


################## RECUPERATION CONSO @ RADIO DEPUIS FIT IOT (scp) #####################
# url_kilometrage = "http://[2001:660:4403:486::1757]"
# url_pression_pneu = "http://[2001:660:4403:486::1057]"
# url_frein = "http://[2001:660:4403:486::a090]"

# kilometrage_inst = requests.get(url_kilometrage)
# pression_inst = requests.get(url_pression_pneu)
# frein_inst = requests.get(url_frein)

# # Récupération des fichiers .oml
# # Consommation
# p = subprocess.Popen(['scp',
#                       'riotp6@lille.iot-lab.info:~/.iot-lab/last/consumption/*.oml',
#                       './conso'])
# sts = p.wait()

# # Radio (RSSI) sur le canal 15
# p = subprocess.Popen(['scp',
#                       'riotp6@lille.iot-lab.info:~/.iot-lab/last/radio/*.oml',
#                       './radio'])
# sts = p.wait()


#################### INFOS CONSOMMATION #############################################
# Récupération consommation noeud kilometrage
conso_km_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_149.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_149.oml | awk '{print $8}'); echo $consumption"])
timestamps_km_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_149.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_149.oml | awk '{print $4}'); echo $consumption"])

    #Conversion des Strings obtenus en tableaux d'integers
map_object = map(float, conso_km_str.split())
conso_km = list(map_object)
map_object = map(int, timestamps_km_str.split())
timestamps_km = list(map_object)

# Récupération consommation noeud pneu
conso_pneu_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_150.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_150.oml | awk '{print $8}'); echo $consumption"])
timestamps_pneu_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_150.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_150.oml | awk '{print $4}'); echo $consumption"])

    #Conversion des Strings obtenus en tableaux d'integers
map_object = map(float, conso_pneu_str.split())
conso_pneu = list(map_object)
map_object = map(int, timestamps_pneu_str.split())
timestamps_pneu = list(map_object)

# Récupération consommation noeud frein 
conso_frein_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_151.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_151.oml | awk '{print $8}'); echo $consumption"])
timestamps_frein_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_150.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_150.oml | awk '{print $4}'); echo $consumption"])

    #Conversion des Strings obtenus en tableaux d'integers
map_object = map(float, conso_frein_str.split())
conso_frein = list(map_object)
map_object = map(int, timestamps_frein_str.split())
timestamps_frein = list(map_object)



############# Génération Données de Simulation ####################@
# Date de première mise en circulation => valeur à récupérer sur thingsboard ? 
# Voir  BDD psql
date_first = '2012-01-01'
date_first = datetime.strptime(date_first, "%Y-%m-%d")
date_first_timestamp = datetime.timestamp(date_first)
print(date_first_timestamp)

# Date du dernier controle technique => valeur à récupérer sur thingsboard ? 
# Voir  BDD psql
dernier_ctrl = '2020-04-01'
dernier_ctrl = datetime.strptime(dernier_ctrl, "%Y-%m-%d")

# Date dernière révision => valeur à récupérer sur thingsboard ? 
derniere_revision = '2021-11-20'
derniere_revision = datetime.strptime(derniere_revision, "%Y-%m-%d")
derniere_revision_timestamp = np.zeros((1,))
derniere_revision_timestamp[0] = datetime.timestamp(derniere_revision)

km_derniere_revision = np.zeros((1,))
km_derniere_revision[0] = 45000

# Date de la dernière vidange
derniere_vidange = '2021-11-20'
derniere_vidange = datetime.strptime(derniere_vidange, "%Y-%m-%d")
derniere_vidange_timestamp = np.zeros((1,))
derniere_vidange_timestamp[0] = datetime.timestamp(derniere_vidange)


# Fichiers de simulation avec les données nécessaires
# Sert juste pour tester, il faudra les récupérer dans la BDD 
df = pd.read_csv('simulation_entr.csv', sep=';')

# Traitement 
# simulation des données
#dates = df.date.values
dates = np.arange(datetime(2020,1,1), datetime(2022,1,25), timedelta(days=1)).astype(datetime)

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


#for i in range(len(dates)):
#   dates[i] = datetime.strptime(dates[i],"%Y-%m-%d %H:%M:%S")

# Prévision date du contrôle technique 
actual_date = datetime.now()
prochain_ctrl = dernier_ctrl.replace(year=dernier_ctrl.year+2)
print("prochain contrôle:"+str(prochain_ctrl))

# Kilométrage
km = np.random.normal(loc=80,scale=50,size=(len(dates),))
km_initial = 0
km = np.cumsum(km)
km = km + km_initial

# Prévision de la date de la prochaine révision 
date_timestamps = np.zeros(len(dates))
tmp = 1

for i in range(len(date_timestamps)):  
    date_timestamps[i] = datetime.timestamp(dates[i])
    if(i>0):
        tmp += 1
        if (tmp == 40): 
            pr_pneu1[i] = 2.6
            pr_pneu2[i] = 2.6
            pr_pneu3[i] = 2.6
            pr_pneu4[i] = 2.6
            pf_avt_1[i] = pf_avt_1[i-1] - abs(np.random.standard_normal((1,))*1e-2)
            pf_arr_1[i] = pf_arr_1[i-1] - abs(np.random.standard_normal((1,))*1e-2)
            tmp = 0
            
        else:
            pr_pneu1[i] = pr_pneu1[i-1] - abs(np.random.standard_normal((1,))*1e-2)
            pr_pneu2[i] = pr_pneu2[i-1] - abs(np.random.standard_normal((1,))*1e-2)
            pr_pneu3[i] = pr_pneu3[i-1] - abs(np.random.standard_normal((1,))*1e-2)
            pr_pneu4[i] = pr_pneu4[i-1] - abs(np.random.standard_normal((1,))*1e-2)
            pf_avt_1[i] = pf_avt_1[i-1] - abs(np.random.standard_normal((1,))*1e-2)
            pf_arr_1[i] = pf_arr_1[i-1] - abs(np.random.standard_normal((1,))*1e-2)
    

#fig1, axs = plt.subplots(7)
#axs[0].plot(dates,km)
# axs[1].plot(dates, pr_pneu1)
# axs[2].plot(dates, pr_pneu2)
# axs[3].plot(dates, pr_pneu3)
# axs[4].plot(dates, pr_pneu4)
# axs[5].plot(dates, pf_avt_1)
# axs[6].plot(dates, pf_arr_1)
#plt.show()

############## PREDICTION SUR VALIDITE DU VECHIULE (ancienneté > 7 ans) ###################
today = datetime.now()
# if(today - date_first < 7): 
#     validite = False
# else:
#     validite = True
#     remaining_validite = today.year - date_first.year;
# print(remaining_validite)

############## REGRESSION KILOMETRAGE ###################
#On considère qu'il y a eu une révision à l'achat du véhicule s'il a été acheté d'occasion
#Prédiction de la Date des prochains 15000km 
degree=1 #Dregee du polynome pour la régression

# Création du modèle
model_date_pred = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
model_date_pred.fit(km[:, np.newaxis], date_timestamps)
km_pred = np.linspace(km[0],km[len(km)-1]+1000) #kiloètre dont on droit prédire la date

# Recherche du kilometrage a la derniere revision
# index_derniere_revision = date_timestamps.where(derniere_revision_timestamp[0])

km_derniere_revision = np.zeros((1,))
km_derniere_revision[0] = 45000 #km[index_derniere_revision]

date_timestamps_pred = model_date_pred.predict(km_pred[:, np.newaxis]) # Prédiction des dates
# Prédiction de la date de prochaine révision
date_revision_pred = model_date_pred.predict(km_derniere_revision[:, np.newaxis]+15000) 
print("prochaine révision:"+str(datetime.fromtimestamp(date_revision_pred[0])))

# Evaluate the models using crossvalidation
scores = cross_val_score(
        model_date_pred, date_timestamps[:, np.newaxis], km, scoring="neg_mean_squared_error", cv=10
)

# Plot figure
plt.figure(2)
plt.plot(km_pred, date_timestamps_pred)
plt.plot(km, date_timestamps)
plt.title(
        "Degree {}\nMSE = {:.2e}(+/- {:.2e})".format(
        degree, -scores.mean(), scores.std())
)
plt.show()

############## REGRESSION HUILE MOTEUR ###################

# Recherche du kilometrage de la derniere vidange 
# index_derniere_vidange = date_timestamps.where(derniere_vidange_timestamp[0])

km_derniere_vidange = np.zeros((1,))
km_derniere_vidange[0] = 45000 # km[index_derniere_vidange]

date_vidange_pred = model_date_pred.predict(km_derniere_vidange[:, np.newaxis]+10000) 
print("prochaine vidange:"+str(datetime.fromtimestamp(date_vidange_pred[0])))


############## REGRESSION PNEUS ###################
# PNEU 1
pneu1_donnees = pr_pneu1[len(pr_pneu1)-35:] # Prendre les 40 dernières valeurs
model_pr_pneu1 = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
model_pr_pneu1.fit(pneu1_donnees[:, np.newaxis], date_timestamps[len(date_timestamps)-35:])
pr_pneu1_pred = np.array(pr_pneu1[len(pr_pneu1)-35:]) #Pression dont on doit prédire la date

date_timestamps_pred = model_pr_pneu1.predict(pneu1_donnees[:, np.newaxis])
threshold_press = np.zeros((1,))
threshold_press[0] = 2.4
date_regonflage_pred = model_pr_pneu1.predict(threshold_press[:, np.newaxis])
print("prochain gonfflage:"+str(datetime.fromtimestamp(date_regonflage_pred[0])))

# Evaluate the models using crossvalidation
scores = cross_val_score(
        model_pr_pneu1, pneu1_donnees[:, np.newaxis], date_timestamps[len(date_timestamps)-35:], scoring="neg_mean_squared_error", cv=10
)

plt.figure(3)
plt.plot(pr_pneu1_pred, date_timestamps_pred)
plt.plot(pr_pneu1[len(pr_pneu1)-35:], date_timestamps[len(date_timestamps)-35:])
plt.title(
        "Degree {}\nMSE = {:.2e}(+/- {:.2e})".format(
        degree, -scores.mean(), scores.std())
)
plt.show()


############## REGRESSION FREINS ###################
# FREIN AVANT 1
model_pf_avt1 = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
model_pf_avt1.fit(pf_avt_1[:, np.newaxis], date_timestamps)

date_timestamps_pred = model_pf_avt1.predict(pf_avt_1[:, np.newaxis])
threshold_frein = np.zeros((1,))
threshold_frein[0] = 3
date_frein_pred = model_pf_avt1.predict(threshold_frein[:, np.newaxis])
print("prochain changement de plaquettes de freins:"+str(datetime.fromtimestamp(date_frein_pred[0])))

# Evaluate the models using crossvalidation
scores = cross_val_score(
        model_pf_avt1, pf_avt_1[:, np.newaxis], date_timestamps, scoring="neg_mean_squared_error", cv=10
)

plt.figure(4)
plt.plot(pf_avt_1, date_timestamps_pred)
plt.plot(pf_avt_1, date_timestamps)
plt.title(
        "Degree {}\nMSE = {:.2e}(+/- {:.2e})".format(
        degree, -scores.mean(), scores.std())
)
plt.show()



