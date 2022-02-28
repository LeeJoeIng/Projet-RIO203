#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: karencaloyannis

Parse the  .oml files containing consumption & rssi information. 
Estimate the remaining battery life of the nodes. 
POST data and rssi to thingsboard.

"""

import requests
import subprocess
import numpy as np

################# Get consumption & rssi data from fit iot nodes #####################
url_kilometrage = "http://[2001:660:4403:486::1757]" #mileometer node
url_pression_pneu = "http://[2001:660:4403:486::1057]" #tire pressure node
url_frein = "http://[2001:660:4403:486::a090]" #brake pad node
url_oil = "http://[2001:660:4403:486::a173]" #oil level node

kilometrage_inst = requests.get(url_kilometrage)
pression_inst = requests.get(url_pression_pneu)
frein_inst = requests.get(url_frein)

# Get .oml files
# Consumption
p = subprocess.Popen(['scp',
                      'riotp6@lille.iot-lab.info:~/.iot-lab/last/consumption/*.oml',
                      './conso'])
sts = p.wait()

# RSSI on channel 15
p = subprocess.Popen(['scp',
                      'riotp6@lille.iot-lab.info:~/.iot-lab/last/radio/*.oml',
                      './radio'])
sts = p.wait()


#################### Consumption #############################################
# mileometer node
current_km_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_149.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_149.oml | awk '{print $8}'); echo $consumption"])
voltage_km_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_149.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_149.oml | awk '{print $7}'); echo $consumption"])
timestamps_km_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_149.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_149.oml | awk '{print $4}'); echo $consumption"])

    #Convert string to integers
map_object = map(float, current_km_str.split())
current_km = list(map_object)
map_object = map(int, timestamps_km_str.split())
timestamps_km = list(map_object)
map_object = map(float, voltage_km_str.split())
volt_km = list(map_object)


# tire pressure node
current_pneu_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_150.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_150.oml | awk '{print $8}'); echo $consumption"])
voltage_pneu_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_150.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_150.oml | awk '{print $7}'); echo $consumption"])
timestamps_pneu_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_150.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_150.oml | awk '{print $4}'); echo $consumption"])

    #Convert string to integers
map_object = map(float, current_pneu_str.split())
current_pneu = list(map_object)
map_object = map(int, timestamps_pneu_str.split())
timestamps_pneu = list(map_object)
map_object = map(float, voltage_pneu_str.split())
volt_pneu= list(map_object)

# brake pad thickness node  
current_frein_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_151.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_151.oml | awk '{print $8}'); echo $consumption"])
voltage_frein_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_151.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_151.oml | awk '{print $7}'); echo $consumption"])
timestamps_frein_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_151.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_151.oml | awk '{print $4}'); echo $consumption"])

    #Convert string to integers
map_object = map(float, current_frein_str.split())
current_frein = list(map_object)
map_object = map(int, timestamps_frein_str.split())
timestamps_frein = list(map_object)
map_object = map(float, voltage_frein_str.split())
volt_frein = list(map_object)

# Oil level node 
current_oil_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_152.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_152.oml | awk '{print $8}'); echo $consumption"])
voltage_oil_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_152.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_152.oml | awk '{print $7}'); echo $consumption"])
timestamps_oil_str = subprocess.getoutput(["total_lines=$(wc -l ./conso/m3_152.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./conso/m3_152.oml | awk '{print $4}'); echo $consumption"])

    #Convert string to integers
map_object = map(float, current_oil_str.split())
current_oil = list(map_object)
map_object = map(int, timestamps_oil_str.split())
timestamps_oil = list(map_object)
map_object = map(float, voltage_oil_str.split())
volt_oil = list(map_object)

#################### RSSI #############################################

# mileometer node
rssi_km_str = subprocess.getoutput(["total_lines=$(wc -l ./radio/m3_149.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./radio/m3_149.oml | awk '{print $7}'); echo $consumption"])
tsrssi_km_str = subprocess.getoutput(["total_lines=$(wc -l ./radio/m3_149.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./radio/m3_149.oml | awk '{print $4}'); echo $consumption"])

    #Convert string to integers
map_object = map(float, rssi_km_str.split())
rssi_km= list(map_object)
map_object = map(int, tsrssi_km_str.split())
tsrssi_km = list(map_object)

# tire pressure node
rssi_pneu_str = subprocess.getoutput(["total_lines=$(wc -l ./radio/m3_150.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./radio/m3_150.oml | awk '{print $7}'); echo $consumption"])
tsrssi_pneu_str = subprocess.getoutput(["total_lines=$(wc -l ./radio/m3_150.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./radio/m3_150.oml | awk '{print $4}'); echo $consumption"])

    #Convert string to integers
map_object = map(float, rssi_pneu_str.split())
rssi_pneu = list(map_object)
map_object = map(int, tsrssi_pneu_str.split())
tsrssi_pneu = list(map_object)

# brake pad thickness node 
rssi_frein_str = subprocess.getoutput(["total_lines=$(wc -l ./radio/m3_151.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./radio/m3_151.oml | awk '{print $7}'); echo $consumption"])
tsrssi_frein_str = subprocess.getoutput(["total_lines=$(wc -l ./radio/m3_151.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./radio/m3_151.oml | awk '{print $4}'); echo $consumption"])

    #Convert string to integers
map_object = map(float, rssi_frein_str .split())
rssi_frein = list(map_object)
map_object = map(int, tsrssi_frein_str.split())
tsrssi_frein = list(map_object)

# Oil level node 
rssi_oil_str = subprocess.getoutput(["total_lines=$(wc -l ./radio/m3_152.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./radio/m3_152.oml | awk '{print $7}'); echo $consumption"])
tsrssi_oil_str = subprocess.getoutput(["total_lines=$(wc -l ./radio/m3_152.oml | awk '{ print $1 }'); consumption=$(awk 'NR==11,NR==total_lines' ./radio/m3_152.oml | awk '{print $4}'); echo $consumption"])

    #Convert string to integers
map_object = map(float, rssi_oil_str.split())
rssi_oil = list(map_object)
map_object = map(int, tsrssi_oil_str.split())
tsrssi_oil = list(map_object)

# Take the last 500 values
rssi_km = rssi_km[-500:]
rssi_pneu = rssi_pneu[-500:]
rssi_frein = rssi_frein[-500:]
rssi_oil = rssi_oil[-500:]
tsrssi_km = tsrssi_km[-500:]
tsrssi_pneu = tsrssi_pneu[-500:]
tsrssi_frein = tsrssi_frein[-500:]
tsrssi_oil = tsrssi_oil[-500:]

#################### POST data to thingsboard ########################################
##### Consumption
# Mean consumptionss (W)
moyenne_current_km = np.mean(current_km)
moyenne_current_pneu = np.mean(current_pneu)
moyenne_current_frein = np.mean(current_frein)
moyenne_current_oil = np.mean(current_oil)

# Calculate the remaining battery life hours 
capacity = 650 #mAh
duree_vie_km = 650/moyenne_current_km/1000
duree_vie_pneu = 650/moyenne_current_pneu/1000
duree_vie_frein = 650/moyenne_current_frein/1000
duree_vie_oil = 650/moyenne_current_oil/1000

# post data to thingsboard
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

##### Post RSSI values to thingsboard
for i in range(len(tsrssi_km)) :
    data_rssi = '{\"ts\":' + str(int(tsrssi_km[i])) + "000" + ',\"values\":{\"rssi_km\":' + str(rssi_km[i]) + '}}'
    response = requests.post(url_post, headers = header_post, data = data_rssi)
    #print(response)

for i in range(len(tsrssi_oil)) :
    data_rssi = '{\"ts\":' + str(int(tsrssi_oil[i])) + "000" + ',\"values\":{\"rssi_oil\":' + str(rssi_oil[i]) + '}}'
    response = requests.post(url_post, headers = header_post, data = data_rssi)
    #print(response)
    
for i in range(len(tsrssi_frein)) :
    data_rssi = '{\"ts\":' + str(int(tsrssi_frein[i])) + "000" + ',\"values\":{\"rssi_frein\":' + str(rssi_oil[i]) + '}}'
    response = requests.post(url_post, headers = header_post, data = data_rssi)
    #print(response)
    
for i in range(len(tsrssi_pneu)) :
    data_rssi = '{\"ts\":' + str(int(tsrssi_pneu[i])) + "000" + ',\"values\":\"rssi_tire\":' + str(rssi_pneu[i]) + '}}'
    response = requests.post(url_post, headers = header_post, data = data_rssi)
    #print(response)