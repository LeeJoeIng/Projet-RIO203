#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Karen Caloyannis

Prediction of the inflation of one of the tires, using polynomial regression. 
The simualtion was done for only one tire, for simplicity. 
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

# Fit IoT URL 
# url_fitiot = 'http://[2001:660:4403:486::1057]' #node m3_150, Lille

# response = requests.get(url_fitiot)
# tire_fitiot = float(response.text)
# print(tire_fitiot)

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

##### GET latest telemetry data from thingsboard : last tire pressure measurement ##
# Header
header = {
    'Content-type': 'application/json',
    'X-Authorization': 'Bearer ' + jwt_token,
}

# url 
url_last_tire = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/timeseries?keys=tire&agg=NONE'

response = requests.get(url_last_tire, headers = header)
response_json = response.json()

# Parse the json response
# for key in response_json['tire']:
#     last_tire = float(key['value'])

# # Difference between the sensor value (simulated) and the last telemetry
# print(last_tire)
# delta = tire_fitiot - last_tire 

# # apply the offset
# tire_fitiot = tire_fitiot - delta

################## POST the value to Thingsboard ####################
# url_post = 'http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'

# header_post = {
#             'Content-type': 'application/json',
# }

# data_fitiot = '{\"tire\":' + str(tire_fitiot) + '}'

# response = requests.post(url_post, headers = header_post, data = data_fitiot)

""" End of the simulation part """

####### GET thingsboard telemetry, from the last inflation until now ##########
# Header
header = {
    'Content-type': 'application/json',
    'X-Authorization': 'Bearer ' + jwt_token,
}

# url to get the date of the last inflation
url_revision = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/attributes/SHARED_SCOPE?keys=date_dernier_gonflage'

response = requests.get(url_revision, headers=header)

# Parser the response
response_json = response.json() 

for key in response_json: 
    date_last_inflation = int(int(key['value'])/1000) # date of the last inflation
print("last inflation :" + str(datetime.fromtimestamp(date_last_inflation)))

today = datetime.now()
today = int(datetime.timestamp(today))

# GET the telemetry data since the last inflation until now
# add &limit=400 to be sure to get all the values
url_recup = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/timeseries?keys=tire&startTs=' + str(date_last_inflation) + '000' + '&endTs=' + str(today) + '000' + '&agg=NONE&limit=400'

response = requests.get(url_recup, headers=header)

# Parser the response
response_json = response.json() 

ts = [] #timestamps
pressure = [] #pressure values

for key in response_json['tire']:
    ts.append(int(key['ts'])/1000)
    pressure.append(float(key['value']))

ts = np.array(ts) #timestamps
ts_int = np.flip(np.arange(0, len(ts), dtype=int)) # Number of days since the last inflation
pressure = np.array(pressure) #pressure values

######################## Polynomial Regression ########################

# url to post telemtry to the maintenance device
url_tire='http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'

header = {
            'Content-type': 'application/json',
}

# pressure threshold => predict the date when the pressure reaches that threshold
threshold_press = 2.4

## Estimate the degree for the polynomial regression
degree = 0 # initialiaze the degree of the polynomial
deg_max = 6 # Maximum degree for the polynomial
errors  = np.zeros(deg_max) # to compare the RMSE of each degree
delta_errors = np.zeros(deg_max-1) # Relative errors between RMSE of each degree

# Do the regression for each degree
for i in range(deg_max):
    degree = degree + 1 # Increment the degree 
    
    # Do the regression : x = pressure values, y = days until the last inflation
    polynome, mse, _, _, _ = np.polyfit(pressure, ts_int, degree, full=True)
    
    # Calculate the number days predicted for each pressure value
    ts_prediction = np.polyval(polynome, pressure)
    
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
    if (delta_errors[i] > 0.1): # Verify that incrementing the degree decreases the RMSE by at least 10%
        degree = degree + 1

print("chosen degree = " + str(degree))
    
# Re-calculate the number of days based on the polynomial with the chosen degree
polynome, mse, _, _, _ = np.polyfit(pressure, ts_int, degree, full=True)
ts_prediction = np.polyval(polynome, pressure)
    
# Predict the number of days after the last inflation, when the pressure
# goes below the threshold (defined above)
date_regonflage_pred = np.polyval(polynome,threshold_press)

# Convert the number of days to a timestamp = date of last inflation + number of days
date_regonflage_pred = date_last_inflation + 86400*date_regonflage_pred
print(date_regonflage_pred)

# Check if the predicted date is the unix timestamp range allowed
if(date_min < date_regonflage_pred):
    if(date_regonflage_pred < date_max):
        # Do not use datetime.fromtimestamp to convert the timestamp, throws the error timestamp out of range for platform time_t
        print("next inflation : "+str(datetime(1970, 1, 1) + timedelta(seconds=date_regonflage_pred)))
    else:
        print("Timestamp out of allowed range")
else : 
    print("Timestamp out of allowed range")

# If the predicted next inflation is in less than 30 days 
# Predict data until the date predicted (limit number of previous measures to max. 90)
print(date_regonflage_pred - datetime.timestamp(datetime.now()))
if(0 < (date_regonflage_pred - datetime.timestamp(datetime.now()))/86400):
    if((date_regonflage_pred - datetime.timestamp(datetime.now()))/86400 < 30):
        pressure_pred = np.append(threshold_press, pressure)
        ts_prediction = np.polyval(polynome, pressure_pred)
    else:
        pressure_pred = pressure
else:
    pressure_pred = pressure
            
""" Convert the number of days to timestamps : 
        - one day = 86400 in unix timestamp
        - sum the date of last inflation with the number of days predicted
"""
ts_prediction = date_last_inflation + 86400*ts_prediction # timestamps predicted

print(datetime.fromtimestamp(ts_prediction[0]))

############# POST the results to thingsboard #####################################

# Check if the predicted date is the unix timestamp range allowed
if(date_min < date_regonflage_pred):
    if(date_regonflage_pred < date_max):
        
        # POST the date of next inflation 
        data = '{\"date_gonflage\":' + str(int(date_regonflage_pred)) + "}"
        response = requests.post(url_tire, headers=header, data=data)
        
        # POST the date of the next inflation as telemtery data 
        # which will be plotted on the graph 
        data2 = '{' + '"ts":' + str(int(date_regonflage_pred)) + "000," + '"values":{"date_gonflage_timestamp": 2.4' + '}}'
        response = requests.post(url_tire, headers=header, data=data2)
        
    else:
        print("Timestamp out of allowed range")
else : 
    print("Timestamp out of allowed range")

# POST the regression as telemtery data to thingsboard
# To post the timestamps, modify the timestamps (the "ts" json key) of the pressure data sent to thingsboard
for i in range(len(ts_prediction)):
    # data to send : ts = modified timestamp (prediction), pression_pred = pressure
    data3 = '{'+'\"ts\":' + str(int(ts_prediction[i])) + "000," + '\"values\":{\"pression_pred\":' + str(pressure_pred[i]) + '}}'
    response = requests.post(url_tire, headers=header, data=data3)
