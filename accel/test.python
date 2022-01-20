import json
import time
import pandas as pd

with open("Sortie_v_lo_matinale.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

data = jsonObject['data'][0]
dataFields = data['fields']
dataValues = data['values'] 

#print(dataFields)
#['time', 'latlng', 'elevation', 'h_accuracy', 'speed', 'course', 'device_time', 'distance']
#print(dataValues[0])
#[1569136049, [48.74496746916384, 2.282407478692314], 105.00115753896534, 25.048748, 8.025881, 237.03848, 1569136047.324, 0]

dataframe = pd.DataFrame(data=dataValues, index=list(range(len(dataValues))), columns=dataFields)
pd.set_option("display.max_rows", None, "display.max_columns", None)

#print(dataframe.head(5))

# Declare a list that is to be converted into a column
acceleration = []
#print(len(dataValues)) 

#Algo pour envoyer chaque donnée toutes les secondes
first_time = True
for i in range(len(dataframe)) : 
    #print("*********************************")
    #print("Temps=" + str(i) + "s, position : "          + str((dataframe.loc[i, 'latlng'])))
    #print("Temps=" + str(i) + "s, elevation : "         + str(float(dataframe.loc[i, 'elevation'])) + "m")
    #print("Temps=" + str(i) + "s, vitesse : "           + str(float(dataframe.loc[i, 'speed']))     + "km/h")
    #print("Temps=" + str(i) + "s, distance parcouru : " + str(int(dataframe.loc[i, 'distance']))    + "m")
    if first_time==False :
        vitesseActuel = float(dataframe.loc[i, 'speed'])*1000 #en m
        accel = (vitesseActuel - vitessePrecedente)/3600
        #print("Temps=" + str(i) + "s, acceleration : "  + str(accel) + "m/s²")
        acceleration.append(str(accel))

    else :
        first_time = False
        acceleration.append('0')
    vitessePrecedente = float(dataframe.loc[i, 'speed'])*1000 #en m
   # time.sleep(1)

# Using 'acceleration' as the column name
# and equating it to the list
dataframe['acceleration'] = acceleration
#print(acceleration)
#print(dataframe[['time','acceleration']])
#print(dataframe.head(5))
print(dataframe.iloc[:,[0,8]].head(5))
