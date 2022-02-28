#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 17:05:42 2022

@author: karencaloyannis
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

#### GET measurement data from the Fit IoT sensor nde & POST to Thingsboard ###

url_fitiot = 'http://[2001:660:4403:486::a173]' #m3_152

response = requests.get(url_fitiot)
oil_fitiot = float(response.text)

############################## Get the JWT TOKEN ##############################
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

############## GET latest telemetry data from thingsboard : last oil level ###########
# Header
header = {
    'Content-type': 'application/json',
    'X-Authorization': 'Bearer ' + jwt_token,
}

url_last_tire = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/timeseries?keys=oil&agg=NONE'

response = requests.get(url_last_tire, headers = header)
response_json = response.json()

# Parse the json response
for key in response_json['oil']:
    last_oil = float(key['value'])

# Difference between the sensor value (simulated) and the last telemetry
delta = oil_fitiot - last_oil

# Apply the offset
oil_fitiot = oil_fitiot - delta

################## POST the value to Thingsboard ####################
url_post = 'http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'

header_post = {
            'Content-type': 'application/json',
}

data_fitiot = '{\"oil\":' + str(oil_fitiot) + '}'

response = requests.post(url_post, headers = header_post, data = data_fitiot)

####### GET thingsboard telemetry, from the last inflation until now ##########
headers = {
    'Content-type': 'application/json',
    'X-Authorization': 'Bearer '+ jwt_token,
}

# url to get the last oil change
url_revision = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/attributes/SHARED_SCOPE?keys=date_derniere_vidange'

response = requests.get(url_revision, headers=headers)
response_json = response.json()

# Parse the json response
response_json = response.json() 

for key in response_json : 
    date_last_oil = int(int(key['value'])/1000) # date of the last oil change

# GET the mileage telemetry data since the last oil change until now
# add &limit=1000 to be sure to get all the values
today = datetime.now()
today = int(datetime.timestamp(today))
url_recup = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/timeseries?keys=kilometrage&startTs=' + str(date_last_oil) + "000" + '&endTs=' + str(today) + '000' + '&agg=NONE&limit=1000'

response = requests.get(url_recup, headers=headers)

# Parse the response
response_json = response.json() 

ts_km = [] #timestamps
km = [] #mileage

for key in response_json['kilometrage']:
    ts_km.append(int(key['ts'])/1000)
    km.append(float(key['value']))

ts_km = np.array(ts_km) # timestamps
ts_int_km = np.flip(np.arange(0, len(ts_km), dtype=int)) # Number of days since the last oil change
km = np.array(km) # mileage since the last oil change
km_last_oil = km[len(km)-1] #mileage at the last oil change

# GET the oil level telemetry data since the last oil change until now
# add &limit=1000 to be sure to get all the values
url_recup = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/timeseries?keys=oil&startTs=' + str(date_last_oil) + "000" + '&endTs=' + str(today) + '000' + '&agg=NONE&limit=1000'

response = requests.get(url_recup, headers=headers)

# Parse the reponse
response_json = response.json() 

ts_oil = [] #timestamps
oil = [] #kilométrage

for key in response_json['oil']:
    ts_oil.append(int(key['ts'])/1000)
    oil.append(float(key['value']))

ts_oil = np.array(ts_oil) # timestamps
ts_int_oil = np.flip(np.arange(0, len(ts_oil), dtype=int)) # Number of days since the last oil change
oil = np.array(oil) # oil level

######################## Polynomial Regression - Mileage ######################

## Estimate the degree for the polynomial regression
degree = 0 # initialiaze the degree of the polynomial
deg_max = 6 # Maximum degree for the polynomial
errors  = np.zeros(deg_max) # to compare the RMSE of each degree
delta_errors = np.zeros(deg_max-1) # Relative errors between RMSE of each degree

# Do the regression for each degree
for i in range(deg_max):
    degree = degree + 1 # Increment the degree 
    
    # Stop the estimation for degrees above 6
    if(degree > deg_max):
        break
    
    # Do the regression : x = pressure values, y = days until the last inflation
    polynome, error, _, _, _ = np.polyfit(km, ts_int_km, degree, full=True)
    
    # Calculate the number days predicted for each pressure value
    ts_km_prediction = np.polyval(polynome, km)
    
    # RMSE : error between the days predicted and the days from the telemetry
    errors[i] = mean_squared_error(ts_int_km, ts_km_prediction, squared = False)
    print("degree = "+str(degree))
    print("RMSE = " + str(errors[i]))

# Calculate de difference between the RMSE of each degree (1-2, 2-3, 4-5 and 5-6)
for i in range(len(delta_errors)):
    delta_errors[i] = abs(errors[i] - errors[i+1])/errors[i]

print("delta_errors : " + str(delta_errors))

degree = 1 # Re-initialize the degree
# Chose the degree that improves best the RMSE 
for i in range(len(delta_errors)):
    if (delta_errors[i] > 0.1): # Verify that incrementing the degree decreases the RMSE by at least 10%
        degree = degree+1

print("chosen degree = " + str(degree))

""" Convert the number of days to timestamps : 
        - one day = 86400 in unix timestamp
        - sum the date of last inflation with the number of days predicted
"""
ts_km_prediction = date_last_oil + 86400*ts_km_prediction # timestamps predicted

# Predict the number of days after the last oil change, when the mileage
# has increased by 10000 km 
date_change_pred= np.polyval(polynome,km_last_oil+10000)
print(date_change_pred)

# Convert the number of days to a timestamp = date of last inflation + number of days
date_change_pred = date_last_oil + 86400*date_change_pred

# Check if the predicted date is the unix timestamp range allowed
if(date_min < date_change_pred):
    if(date_change_pred < date_max):
        # Do not use datetime.fromtimestamp to convert the timestamp, throws the error timestamp out of range for platform time_t
        print("next oil change : "+str(datetime(1970, 1, 1) + timedelta(seconds=date_change_pred)))
    else:
        print("Timestamp out of allowed range")
else : 
    print("Timestamp out of allowed range")

######################## Polynomial Regression - Oil change ###################

## Estimate the degree for the polynomial regression
degree = 0 # initialiaze the degree of the polynomial
deg_max = 6 # Maximum degree for the polynomial
errors  = np.zeros(deg_max) # to compare the RMSE of each degree
delta_errors = np.zeros(deg_max-1) # Relative errors between RMSE of each degree

# Do the regression for each degree
for i in range(deg_max):
    degree = degree + 1 # Increment the degree 
    
    # Stop the estimation for degrees above 6
    if(degree > deg_max):
        break
    
    # Do the regression : x = pressure values, y = days until the last inflation
    polynome, error, _, _, _ = np.polyfit(oil, ts_int_oil, degree, full=True)
    
    # Calculate the number days predicted for each pressure value
    ts_oil_prediction = np.polyval(polynome, oil)
    
    # RMSE : error between the days predicted and the days from the telemetry
    errors[i] = mean_squared_error(ts_int_oil, ts_oil_prediction, squared = False)
    print("degree = "+str(degree))
    print("RMSE = " + str(errors[i]))

# Calculate de difference between the RMSE of each degree (1-2, 2-3, 4-5 and 5-6)
for i in range(len(delta_errors)):
    delta_errors[i] = abs(errors[i] - errors[i+1])/errors[i]

print("delta_errors : " + str(delta_errors))

degree = 1 # Re-initialize the degree
# Chose the degree that improves best the RMSE 
for i in range(len(delta_errors)):
    if (delta_errors[i] > 0.1): # Verify that incrementing the degree decreases the RMSE by at least 10%
        degree = degree+1

print("chosen degree = " + str(degree))

# pressure threshold => predict the date when the oil level reaches that threshold
threshold_oil = 4.1

# Predict the number of days after the last inflation, when the pressure
# goes below the threshold (defined above)
date_oil_pred = np.polyval(polynome,threshold_oil)

# Convert the number of days to a timestamp = date of last inflation + number of days
date_oil_pred = date_last_oil + 86400*date_oil_pred

# Check if the predicted date is the unix timestamp range allowed
if(date_min < date_oil_pred):
    if(date_oil_pred < date_max):
        # Do not use datetime.fromtimestamp to convert the timestamp, throws the error timestamp out of range for platform time_t
        print("next oil change (based on oil level):"+str(datetime(1970, 1, 1) + timedelta(seconds=date_oil_pred)))
    else:
        print("Timestamp out of allowed range")

# If the predicted next oil change is in less than 30 days 
# Predict data until the date predicted (limit number of previous measures to max. 90)
if(0 < (date_oil_pred - datetime.timestamp(datetime.now()))/86400):
    if(date_oil_pred - datetime.timestamp(datetime.now()) < 30):
        oil_pred = np.append(threshold_oil, oil[-min(len(oil)), 90:])
        ts_oil_prediction = np.polyval(polynome, oil_pred)
    else:
        oil_pred = oil
else:
    oil_pred = oil

""" Convert the number of days to timestamps : 
        - one day = 86400 in unix timestamp
        - sum the date of last inflation with the number of days predicted
"""
ts_oil_prediction = date_last_oil + 86400*ts_oil_prediction # timestamps predicted

############# POST the results to thingsboard #################################
url = 'http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'

# Check if the predicted date is the unix timestamp range allowed
if(date_min < date_change_pred):
    if(date_change_pred < date_max):
        
        # POST the date of next oil change  (based on the mileage)
        data = '{"next_oil_change":' + str(int(date_change_pred)) + '}'
        response = requests.post(url, headers=headers, data=data)
        
        # POST the date when the oil level goes below the threshold
        data = '{\"date_oil\":' + str(int(date_oil_pred)) + "}"
        response = requests.post(url, headers=headers, data=data)
        
        # POST the date when the oil level will go below the threshold
        # which will be plotted on the graph 
        data2 = '{' + '"ts":' + str(int(date_oil_pred)) + "000," + '"values":{"date_oil_timestamp": 4.1' + '}}'
        response = requests.post(url, headers=headers, data=data2)
        
    else:
        print("unable to predict the oil change date based on mileage")

# POST the regression (oil level) as telemtery data to thingsboard
# To post the timestamps, modify the timestamps (the "ts" json key) of the pressure data sent to thingsboard
for i in range(len(ts_oil_prediction)):
    data = '{'+'\"ts\":' + str(int(ts_oil_prediction[i])) + "000," + '\"values\":{\"oil_pred\":' + str(oil[i]) + '}}'
    response = requests.post(url, headers=headers, data=data)
