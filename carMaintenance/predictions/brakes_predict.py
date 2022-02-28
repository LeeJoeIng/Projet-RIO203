#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: karencaloyannis


Prediction of the date of the next change of the brake pads, based on the pad thickness, 
using polynomial regression.

The simulation was done for only one brake pad, for simplicity.

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

# url_fitiot = 'http://[2001:660:4403:486::1057]' #node m3_151, Lille

# # Parse the response
# response = requests.get(url_fitiot)
# brake_fitiot = float(response.text)


############################## Get the JWT TOKEN ##################################
header = {
    'Content-type': 'application/json',
    'Accept': 'application/json',
}

data = '{"username":"tenant@thingsboard.org", "password":"tenant"}'
url = 'http://localhost:8080/api/auth/login'
response = requests.post(url=url, headers=header, data=data)
response_json = response.json()
jwt_token = response_json['token'] # Token JWT

""" Simulation Part : 
Apply offset to Fit IoT measurement - This part would not appear in the code 
for a real implementation. It is used to post realistic simulated data to thingsboard """

############## GET latest telemetry data from thingsboard : last brake pad thickness ###########
# Header
header = {
    'Content-type': 'application/json',
    'X-Authorization': 'Bearer ' + jwt_token,
}

url_last_break = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/timeseries?keys=brake&agg=NONE'

# Par the json response
response = requests.get(url_last_break, headers = header)
response_json = response.json()

for key in response_json['brake']:
    last_break = float(key['value'])

# # Difference between the sensor value (simulated) and the last telemetry
# delta = last_break - brake_fitiot 

# # Apply the offset
# brake_fitiot = brake_fitiot - delta/5

""" End of the simulation part """

################## POST the value to Thingsboard ####################
# url_post = 'http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'

# header_post = {
#             'Content-type': 'application/json',
# }

# data_fitiot = '{\"brake\":' + str(brake_fitiot) + '}'

# response = requests.post(url_post, headers = header_post, data = data_fitiot)


####### GET thingsboard telemetry, from the last inflation until now ##########
# URL to get the date of the last change of the brake pads
url_revision = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/attributes/SHARED_SCOPE?keys=date_dernier_changement_freins'

response = requests.get(url_revision, headers=header)
response_json = response.json()

# Parse the response
response_json = response.json() 

for key in response_json : 
    date_last_change = int(int(key['value'])/1000) # Récupération de la date de dernière révision

# GET the telemetry data since the last change until now
# add &limit=1000 to be sure to get all the values
today = datetime.now()
today = int(datetime.timestamp(today))
url_recup = 'http://localhost:8080/api/plugins/telemetry/DEVICE/4f5afac0-70a5-11ec-a326-4345504f184b/values/timeseries?keys=brake&startTs=' + str(date_last_change) + "000" + '&endTs=' + str(today) + '000' + '&agg=NONE&limit=1000'

response = requests.get(url_recup, headers=header)

# Parse the json response
response_json = response.json() 

ts = [] #timestamps
brake = [] #mileage

for key in response_json['brake']:
    ts.append(int(key['ts'])/1000)
    brake.append(float(key['value']))

ts = np.array(ts) #timestamps
ts_int = np.flip(np.arange(0, len(ts), dtype=int)) # Number of days since the last inflation
brake = np.array(brake) #mileage


######################## Polynomial Regression ########################

## Estimate the degree for the polynomial regression
degree = 0 # initialiaze the degree of the polynomial
deg_max = 6 # Maximum degree for the polynomial
errors  = np.zeros(deg_max) # to compare the RMSE of each degree
delta_errors = np.zeros(deg_max-1) # Relative errors between RMSE of each degree

# Do the regression for each degree
for i in range(deg_max):
    degree = degree + 1 # Increment the degree 
    
    # Stop the regression for degrees above deg_max
    if(degree > deg_max + 1):
        break
    
    # Do the regression : x = pressure values, y = days until the last inflation
    polynome, error, _, _, _ = np.polyfit(brake, ts_int, degree, full=True)
    
    # Calculate the number days predicted for each pressure value
    ts_prediction = np.polyval(polynome, brake)
    
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
        degree = degree+1

print("chosen degree = " + str(degree))

# pressure threshold => predict the date when the pressure reaches that threshold
threshold_brake = 3

# Predict the number of days after the last inflation, when the pressure
# goes below the threshold (defined above)
date_brake_pred = np.polyval(polynome,threshold_brake)

# Convert the number of days to a timestamp = date of last inflation + number of days
date_brake_pred = date_last_change + 86400*date_brake_pred
print(date_brake_pred)
# Check if the predicted date is the unix timestamp range allowed
if(date_min < date_brake_pred):
    if(date_brake_pred < date_max):
        # Do not use datetime.fromtimestamp to convert the timestamp, throws the error timestamp out of range for platform time_t
        print("next change of the brake pads:"+str(datetime(1970, 1, 1) + timedelta(seconds=date_brake_pred)))
    else:
        print("Timestamp out of allowed range")
else : 
    print("Timestamp out of allowed range")

# If the predicted next change is in less than 30 days 
# Predict data until the date predicted (limit number of previous measures to max. 90)
if(0 < (date_brake_pred - datetime.timestamp(datetime.now()))/86400):
    if((date_brake_pred - datetime.timestamp(datetime.now()))/86400 < 30):
        brake_pred = np.append(threshold_brake, brake[-min(len(brake), 90):])
        ts_prediction = np.polyval(polynome, brake_pred)
    else:
        brake_pred = brake
else:
    brake_pred = brake

""" Convert the number of days to timestamps : 
        - one day = 86400 in unix timestamp
        - sum the date of last inflation with the number of days predicted
"""
ts_prediction = date_last_change + 86400*ts_prediction # timestamps predicted

############# POST the results to thingsboard #####################################

# url of the maintenance device
url = 'http://localhost:8080/api/v1/vmWsSYMqGg8AGCiamhM9/telemetry'

# Check if the predicted date is the unix timestamp range allowed
if(date_min < date_brake_pred):
    if(date_brake_pred < date_max):
        
        # POST the date of next change 
        data = '{\"date_frein1\":' + str(int(date_brake_pred)) + '}'
        response = requests.post(url, headers=header, data=data)
        
        # POST the date of the next inflation as telemtery data 
        # which will be plotted on the graph 
        data2 = '{' + '"ts":' + str(int(date_brake_pred)) + "000," + '"values":{"date_frein_timestamp": 3' + '}}'
        response = requests.post(url, headers=header, data=data2)
                
    else:
        print("Timestamp out of allowed range")
else : 
    print("Timestamp out of allowed range")

# POST the regression as telemtery data to thingsboard
# To post the timestamps, modify the timestamps (the "ts" json key) of the pressure data sent to thingsboard
for i in range(len(ts_prediction)):
    # data to send : ts = modified timestamp (prediction), frein_pred = thickness
    data3 = '{'+'\"ts\":' + str(int(ts_prediction[i])) + "000," + '\"values\":{\"frein_pred\":' + str(brake[i]) + '}}'
    response = requests.post(url, headers=header, data=data3)