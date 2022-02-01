#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 00:38:32 2022

@author: karencaloyannis
"""

import requests
import subprocess
import numpy as np


################# RECUPERATION CONSO @ RADIO DEPUIS FIT IOT (scp) #####################
url_kilometrage = "http://[2001:660:4403:486::1757]"
url_pression_pneu = "http://[2001:660:4403:486::1057]"
url_frein = "http://[2001:660:4403:486::a090]"
url_oil = "http://[2001:660:4403:486::a173]"

kilometrage_inst = requests.get(url_kilometrage)
pression_inst = requests.get(url_pression_pneu)
frein_inst = requests.get(url_frein)

# Récupération des fichiers .oml
# Consommation
p = subprocess.Popen(['scp',
                      'riotp6@lille.iot-lab.info:~/.iot-lab/last/consumption/*.oml',
                      './conso'])
sts = p.wait()

# Radio (RSSI) sur le canal 15
p = subprocess.Popen(['scp',
                      'riotp6@lille.iot-lab.info:~/.iot-lab/last/radio/*.oml',
                      './radio'])
sts = p.wait()


#################### INFOS CONSOMMATION #############################################
# Récupération consommation noeud kilometrage
current_km_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_149.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_149.oml | awk '{print $8}'); echo $consumption"])
voltage_km_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_149.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_149.oml | awk '{print $7}'); echo $consumption"])
timestamps_km_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_149.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_149.oml | awk '{print $4}'); echo $consumption"])

    #Conversion des Strings obtenus en tableaux d'integers
map_object = map(float, current_km_str.split())
current_km = list(map_object)
map_object = map(int, timestamps_km_str.split())
timestamps_km = list(map_object)
map_object = map(float, voltage_km_str.split())
volt_km = list(map_object)


# Récupération consommation noeud pneu
current_pneu_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_150.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_150.oml | awk '{print $8}'); echo $consumption"])
voltage_pneu_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_150.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_150.oml | awk '{print $7}'); echo $consumption"])
timestamps_pneu_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_150.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_150.oml | awk '{print $4}'); echo $consumption"])

    #Conversion des Strings obtenus en tableaux d'integers
map_object = map(float, current_pneu_str.split())
current_pneu = list(map_object)
map_object = map(int, timestamps_pneu_str.split())
timestamps_pneu = list(map_object)
map_object = map(float, voltage_pneu_str.split())
volt_pneu= list(map_object)

# Récupération consommation noeud frein 
current_frein_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_151.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_151.oml | awk '{print $8}'); echo $consumption"])
voltage_frein_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_151.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_151.oml | awk '{print $7}'); echo $consumption"])
timestamps_frein_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_151.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_151.oml | awk '{print $4}'); echo $consumption"])

    #Conversion des Strings obtenus en tableaux d'integers
map_object = map(float, current_frein_str.split())
current_frein = list(map_object)
map_object = map(int, timestamps_frein_str.split())
timestamps_frein = list(map_object)
map_object = map(float, voltage_frein_str.split())
volt_frein = list(map_object)

# Récupération consommation noeud huile 
current_oil_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_152.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_152.oml | awk '{print $8}'); echo $consumption"])
voltage_oil_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_152.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_152.oml | awk '{print $7}'); echo $consumption"])
timestamps_oil_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_152.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_152.oml | awk '{print $4}'); echo $consumption"])

    #Conversion des Strings obtenus en tableaux d'integers
map_object = map(float, current_oil_str.split())
current_oil = list(map_object)
map_object = map(int, timestamps_oil_str.split())
timestamps_oil = list(map_object)
map_object = map(float, voltage_oil_str.split())
volt_oil = list(map_object)


#################### Envoi vers thingsboard ########################################

# Consos moyennes (W)
moyenne_current_km = np.mean(current_km)
moyenne_current_pneu = np.mean(current_pneu)
moyenne_current_frein = np.mean(current_frein)
moyenne_current_oil = np.mean(current_oil)

# Duree de vie 
capacity = 650 #mAh
duree_vie_km = 650/moyenne_current_km/1000
duree_vie_pneu = 650/moyenne_current_pneu/1000
duree_vie_frein = 650/moyenne_current_frein/1000
duree_vie_oil = 650/moyenne_current_oil/1000

############# TOKEN JWT #############
# Récupération du token JWT
header = {
    'Content-type': 'application/json',
    'Accept': 'application/json',
}

data = '{"username":"tenant@thingsboard.org", "password":"tenant"}'
url = 'http://localhost:8080/api/auth/login'
response = requests.post(url=url, headers=header, data=data)
response_json = response.json()
jwt_token = response_json['token'] # Token JWT

# POST VERS THINGSBOARD 
url_post = 'http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'

header_post = {
            'Content-type': 'application/json',
}

data_lifes = '{\"life_km\":' + str(duree_vie_km) + ',\"life_tire\":' + str(duree_vie_pneu) + ',\"life_break\":' + str(duree_vie_frein) + ',\"life_oil\":' + str(duree_vie_oil) + '}'
response = requests.post(url_post, headers = header_post, data = data_lifes)
print(response)

data_means = '{\"mean_current_km\":' + str(moyenne_current_km) + ',\"mean_current_tire\":' + str(moyenne_current_pneu ) + ',\"mean_conso_break\":' + str(moyenne_current_frein) + ',\"mean_current_oil\":' + str(moyenne_current_oil) + '}'
response = requests.post(url_post, headers = header_post, data = data_means)
print(response)
