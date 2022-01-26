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

# Date du dernier controle technique => valeur à récupérer sur thingsboard ? 
# Voir  BDD psql
dernier_ctrl = '2020-04-01'
dernier_ctrl = datetime.strptime(dernier_ctrl, "%Y-%m-%d")

# Kilometrge initial => valeur à récupérer sur thingsboard ? 
# Voir  BDD psql
km_initial = 14000

# Fichiers de simulation avec les données nécessaires
# Sert juste pour tester, il faudra les récupérer dans la BDD 
df = pd.read_csv('simulation_entr.csv', sep=';')

# Traitement 
# simulation des données
#dates = df.date.values
dates = np.arange(datetime(2021,12,24), datetime(2022,1,25), timedelta(days=1)).astype(datetime)
km = np.random.normal(loc=80,scale=50,size=(len(dates),))
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
print(prochain_ctrl)

# Kilométrage
km = np.cumsum(km)
km = km + km_initial

# Prévision de la date de la prochaine révision 
date_timestamps = np.zeros(len(dates))
for i in range(len(date_timestamps)):  
    date_timestamps[i] = datetime.timestamp(dates[i])
    if(i>0):
        pr_pneu1[i] = pr_pneu1[i-1] - abs(np.random.standard_normal((1,))*1e-2)
        pr_pneu2[i] = pr_pneu2[i-1] - abs(np.random.standard_normal((1,))*1e-2)
        pr_pneu3[i] = pr_pneu3[i-1] - abs(np.random.standard_normal((1,))*1e-2)
        pr_pneu4[i] = pr_pneu4[i-1] - abs(np.random.standard_normal((1,))*1e-2)
        pf_avt_1[i] = pf_avt_1[i-1] - abs(np.random.standard_normal((1,))*1e-3)
        pf_arr_1[i] = pf_arr_1[i-1] - abs(np.random.standard_normal((1,))*1e-3)

print(date_timestamps)

#fig1, axs = plt.subplots(7)
#axs[0].plot(dates,km)
# axs[1].plot(dates, pr_pneu1)
# axs[2].plot(dates, pr_pneu2)
# axs[3].plot(dates, pr_pneu3)
# axs[4].plot(dates, pr_pneu4)
# axs[5].plot(dates, pf_avt_1)
# axs[6].plot(dates, pf_arr_1)
#plt.show()



############## REGRESSION KILOMETRAGE ###################
#Prédiction Kilométrage à venir 
degree=1

model = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
model.fit(date_timestamps[:, np.newaxis], km)
x_plot = np.arange(datetime(2021,12,24), datetime(2022,2,15), timedelta(days=1)).astype(datetime)

for i in range(len(x_plot)):
    x_plot[i] = datetime.timestamp(x_plot[i])
    
print(x_plot)
    
y_plot = model.predict(x_plot[:, np.newaxis])

# Evaluate the models using crossvalidation
scores = cross_val_score(
        model, date_timestamps[:, np.newaxis], km, scoring="neg_mean_squared_error", cv=10
)

# Plot figure
plt.figure(2)
plt.plot(x_plot, y_plot, label=f"degree {degree}")
plt.plot(date_timestamps, km)
plt.title(
        "Degree {}\nMSE = {:.2e}(+/- {:.2e})".format(
        degree, -scores.mean(), scores.std())
)
plt.show()

#Prédiction de la révision
#Vérifier si révision entre-temps 


############## REGRESSION PNEUS ###################




############## REGRESSION FREINS ###################

