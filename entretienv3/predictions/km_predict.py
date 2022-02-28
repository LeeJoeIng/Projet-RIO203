#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: karencaloyannis

Prediction of the date of the next car maintenance, based on the mileage of
the car, using polynomial regression.

"""
import numpy as np
import requests

from datetime import datetime, timezone, timedelta
from sklearn.metrics import mean_squared_error

# Calculate maximum and minimum timestamp allowed
date_min = datetime.min.replace(tzinfo=timezone.utc).timestamp()
print("timestamp min. = " + str(date_min))
date_max = datetime.max.replace(tzinfo=timezone.utc).timestamp()
print("timestamp max. = " + str(date_max))

###### GET measurement data from the Fit IoT sensor nde & POST to Thingsboard ######

url_fitiot = 'http://[2001:660:4403:486::1057]' #node m3_149, Lille

# Parse the response
response = requests.get(url_fitiot)
km_fitiot = float(response.text)

############################## Get the JWT TOKEN ##################################
header = {
    'Content-type': 'application/json',
    'Accept': 'application/json',
}

data = '{"username":"tenant@thingsboard.org", "password":"tenant"}'
url = 'http://localhost:8080/api/auth/login'
response = requests.post(url=url, headers=header, data=data)
response_json = response.json()
jwt_token = response_json['token'] # JWT Token

""" Simulation Part : 
Apply offset to Fit IoT measurement - This part would not appear in the code 
for a real implementation. It is used to post realistic simulated data to thingsboard """

############## GET latest telemetry data from thingsboard : last mileage ###########
# Header
header = {
    'Content-type': 'application/json',
    'X-Authorization': 'Bearer ' + jwt_token,
}

url_last_tire = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/timeseries?keys=kilometrage&agg=NONE'

response = requests.get(url_last_tire, headers = header)
response_json = response.json()

# Parse the json response
for key in response_json['kilometrage']:
    last_km = float(key['value'])

# Add the last mileage value to the last telemetry 
km_fitiot = km_fitiot + last_km

""" End of the simulation part """

################## POST the value to Thingsboard ####################
url_post = 'http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'

header_post = {
            'Content-type': 'application/json',
}

data_fitiot = '{\"kilometrage\":' + str(km_fitiot) + '}'

response = requests.post(url_post, headers = header_post, data = data_fitiot)


####### GET thingsboard telemetry, from the last inflation until now ##########
# Header
headers = {
    'Content-type': 'application/json',
    'X-Authorization': 'Bearer '+ jwt_token,
}

# url to get the date of the last maintenance
url_revision = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/attributes/SHARED_SCOPE?keys=date_derniere_revision'

response = requests.get(url_revision, headers=headers)
response_json = response.json()

# Parse the json response
response_json = response.json() 

for key in response_json : 
    date_last_maintenance = int(int(key['value'])/1000) # date of the last car maintenance

# GET the telemetry data since the last car maintenance until now
# add &limit=1000 to be sure to get all the values
today = datetime.now()
today = int(datetime.timestamp(today))
url_recup = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/timeseries?keys=kilometrage&startTs=' + str(date_last_maintenance) + "000" + '&endTs=1'+ str(today) + '000' + '&agg=NONE&limit=1000'

print("last maintenance :" + str(datetime.fromtimestamp(date_last_maintenance)))

response = requests.get(url_recup, headers=headers)

# Parse the json response
response_json = response.json() 

ts = [] #timestamps
km = [] #kilométrage

for key in response_json['kilometrage']:
    ts.append(int(key['ts'])/1000)
    km.append(float(key['value']))

ts = np.array(ts)
ts_int = np.flip(np.arange(0, len(ts), dtype=int)) # Number of days since the last inflation
km = np.array(km)

# Mileage at the date of the last maintenance
km_last_maintenance = km[len(km)-1]


######################## Polynomial Regression ########################

## Estimate the degree for the polynomial regression
degree = 0 # initialiaze the degree of the polynomial
deg_max = 6 # Maximum degree for the polynomial
errors  = np.zeros(deg_max) # to compare the RMSE of each degree
delta_errors = np.zeros(deg_max-1) # Relative errors between RMSE of each degree

# Do the regression for each degree
for i in range(deg_max):
    degree = degree + 1
    
    polynome = np.polyfit(km, ts_int, degree)
    
    # Calculate the number days predicted for each pressure value
    ts_prediction = np.polyval(polynome, km)
    
    # RMSE : error between the days predicted and the days from the telemetry
    errors[i] = mean_squared_error(ts_int, ts_prediction, squared = False)
    print("degree = "+str(degree))
    print("RMSE = " + str(errors[i]))
    
# Calculate de difference between the RMSE of each degree (1-2, 2-3, 4-5 and 5-6)
for i in range(len(delta_errors)):
    delta_errors[i] = abs(errors[i] - errors[i+1])/errors[i]

print("delta_errors : " + str(delta_errors))

degree = 1 # Re-initialize the degree
# Chose the degree that improves best the RMSE 
for i in range(len(delta_errors)):
    print(delta_errors[i])
    if (delta_errors[i] > 0.1): # Verify that incrementing the degree decreases the RMSE by at least 10%
        degree = degree + 1

print("chosen degree = " + str(degree))
    
# Re-calculate the number of days based on the polynomial with the chosen degree
polynome = np.polyfit(km, ts_int, degree)
ts_prediction = np.polyval(polynome, km)

# Predict the number of days after the last maintenance, when the mileage
# has increased by 15 000 km
date_maintenance_pred = np.polyval(polynome, km_last_maintenance+15000)

# Convert the number of days to a timestamp = date of last inflation + number of days
date_maintenance_pred = date_last_maintenance + 86400*date_maintenance_pred

# Check if the predicted date is the unix timestamp range allowed
if(date_min < date_maintenance_pred):
    if(date_maintenance_pred < date_max):
        # Do not use datetime.fromtimestamp to convert the timestamp, throws the error timestamp out of range for platform time_t
        next_maintenance = datetime(1970, 1, 1) + timedelta(seconds=date_maintenance_pred)
        print("next maintenance : "+str(next_maintenance))
    else:
        print("Timestamp out of allowed range")
else : 
    print("Timestamp out of allowed range")

# If the predicted next maintenance is in less than 30 days 
# Predict data until the date predicted (limit number of previous measures to max. 90)
if(0 < (date_maintenance_pred - datetime.timestamp(datetime.now()))/86400):
    if((date_maintenance_pred - datetime.timestamp(datetime.now()))/86400 < 30):
        km_pred = np.append(km_last_maintenance + 15000, km[-min(len(km), 90):])
        ts_prediction = np.polyval(polynome, km_pred)
    else:
        km_pred = km 
else:
    km_pred = km 

""" Convert the number of days to timestamps : 
        - one day = 86400 in unix timestamp
        - sum the date of last inflation with the number of days predicted
"""
ts_prediction = date_last_maintenance + 86400*ts_prediction # timestamps predicted
    
############# POST the results to thingsboard #####################################

# Header
headers = {
    'Content-type': 'application/json',
    'X-Authorization': 'Bearer '+ jwt_token,
}

url = 'http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'

# Check if the predicted date is the unix timestamp range allowed
if(date_min < date_maintenance_pred):
    if(date_maintenance_pred < date_max):
        
        # POST the date of next maintenance 
        next_maintenance = datetime.fromtimestamp(date_maintenance_pred)
        data = '{"next_service":' + str(int(date_maintenance_pred)) + '}'
        response = requests.post(url, headers=headers, data=data)
        
        # POST the date of the next inflation as telemtery data 
        # which will be plotted on the graph 
        data = '{ \"ts\":' + str(int(date_maintenance_pred)) + '000,' + '\"values\":{\"km_maintenance\":' + str(km_last_maintenance+15000) + '}}'
        print(data)
        response = requests.post(url, headers=headers, data=data)
        print("timestamp : " + str(response))
        
    else:
        print("Timestamp out of allowed range")
else : 
    print("Timestamp out of allowed range")

# POST the regression as telemtery data to thingsboard
# To post the timestamps, modify the timestamps (the "ts" json key) of the pressure data sent to thingsboard
for i in range(len(ts_prediction)):
    data = '{'+'\"ts\":' + str(int(ts_prediction[i])) + "000," + '\"values\":{\"kilometrage_pred\":' + str(km_pred[i]) + '}}'
    response = requests.post(url, headers=headers, data=data)
