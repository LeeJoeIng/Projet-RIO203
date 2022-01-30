#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 00:38:32 2022

@author: karencaloyannis
"""

import requests
import subprocess


################# RECUPERATION CONSO @ RADIO DEPUIS FIT IOT (scp) #####################
url_kilometrage = "http://[2001:660:4403:486::1757]"
url_pression_pneu = "http://[2001:660:4403:486::1057]"
url_frein = "http://[2001:660:4403:486::a090]"

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

#################### Envoi vers thingsboard ########################################

