#!/usr/bin/python 
import json
import time
import dateutil
import pandas as pd
import numpy as np
from random import *
   
   
maxTab = 100
tabStop = []
for i in range(maxTab):
    tabStop.append(randint(0, 1))

tabVitesse = []
for i in range(maxTab):
    if(tabStop[i] == 1) : 
        tabVitesse.append(randint(0, 3))
    else :
        tabVitesse.append(80)
    
print("tabVitesse " + str(tabVitesse))
print("tabStop    " + str(tabStop))

pointsEleve = 0
paireTimeDebutFin = []
tabPaire = []
flagFirstTime = True
paireTimeDebutFin = []
for time in range(len(tabVitesse)) :
    if (flagFirstTime == True) :
        stopAvant = tabStop[time]
        if (tabStop[time] == 1) :
            #on detecte un stop
            tabPaire.append(time) #time du début
        flagFirstTime = False
    else :
        if (stopAvant == 0) :
            #on a detecter pas un stop 
            if (tabStop[time] == 1) :
                #on detecte un stop
                tabPaire.append(time) #time du début
        else :
            #stopAvant == 1 cad on a detecter un stop avant
            if (tabStop[time] == 0) :
                #on detecte plus un stop
                pointsEleve = pointsEleve + 1 #incrémente
                tabPaire.append(time) #time de la fin
                paireTimeDebutFin.append(tabPaire)
                tabPaire = []
                
        if (time == len(tabVitesse)-1) : 
            if (tabStop[time] == 1) :
                #on detecte un stop à la fin
                pointsEleve = pointsEleve + 1
                tabPaire.append(time+1)                
                paireTimeDebutFin.append(tabPaire) #time du début
                
        stopAvant = tabStop[time]

print("paireTimeDebutFin : " + str(paireTimeDebutFin))
print("Detecte " + str(pointsEleve) + " stop(s)")

vitesseRalentie = False
for i in range(len(paireTimeDebutFin)) :
    paire = paireTimeDebutFin[i]
    print("paire : " + str(paire))
    for j in range(paire[0],paire[1],1) :
        if (tabVitesse[j] <= 1) :
            #vitesse inférieur à 1km/h
            pointsEleve = pointsEleve - 1
            print("Time de ralentissement : " + str(j) + "s , vitesse : " + str(tabVitesse[j]))
            break
    
if (pointsEleve > 10) :
    #nombre de point de l'élève est plafonné à 10 points
    pointsEleve = 10
    
print("Point eleve final : " + str(pointsEleve))
        