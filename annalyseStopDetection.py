#!/usr/bin/python 
from random import *

tabVitesse = [0.0, 0.3, 0.3, 0.225, 0.24, 0.24, 0.24, 0.25, 0.22, 0.22, 0.22, 0.22, 0.233, 0.3, 0.3, 0.24, 0.24, 0.24, 0.24, 0.983, 2.2, 3.12, 4.04, 5.28, 6.94, 6.24, 6.64, 6.5, 4.8, 4.0, 4.18, 2.8, 1.64, 0.74, 1.42, 1.58, 2.56, 3.7, 4.84, 5.28, 5.5, 5.56, 5.22, 4.7, 4.14, 3.6, 3.56, 4.08, 4.9, 5.98, 7.38, 8.72, 10.02, 11.38, 12.44, 13.16, 13.58, 13.62, 13.42, 13.34, 13.3, 13.28, 13.5, 13.84, 14.18, 14.42, 14.62, 14.7, 14.78, 14.88, 15.12, 15.24, 15.42, 15.46, 15.48, 15.4, 15.4, 15.26, 15.1, 15.02, 14.96, 14.92, 14.84, 14.66, 14.2, 13.58, 12.88, 12.04, 11.22, 10.32, 9.38, 8.22, 7.1, 5.92, 4.68, 3.66, 2.9, 3.12, 3.92, 5.18, 6.78, 8.62, 9.7, 10.68, 11.76, 12.58, 13.24, 13.88, 13.88, 14.86, 15.02, 15.26, 12.38, 12.883, 12.883, 15.44, 15.38, 15.34, 15.24, 15.08, 15.08, 17.38, 14.06, 14.06, 10.08, 10.133, 11.26, 7.66, 7.233, 6.78, 5.14, 3.86, 2.9, 3.54, 3.36, 3.64, 4.24, 3.8, 4.133, 5.12, 7.08, 6.12, 6.2, 8.08, 5.617, 6.96, 3.44, 3.25, 3.0, 1.92, 2.45, 3.36, 5.26, 6.52, 6.48, 5.12, 3.74, 3.64, 3.45, 2.76, 3.067, 4.02, 4.28, 4.28, 9.72, 10.68, 11.58, 10.82, 10.88, 9.22, 7.48, 6.233, 3.517, 2.6, 2.92, 2.92, 6.46, 7.44, 8.58, 8.02, 8.02, 8.02, 14.34, 11.42, 11.15, 10.4, 9.5, 6.98, 6.82, 7.05, 5.8, 4.833, 4.06, 2.36, 1.38, 0.66, 1.46, 1.46, 0.8, 0.8, 1.2, 1.38, 2.38, 3.74, 5.52, 6.9, 8.38, 9.88, 11.44, 12.8, 14.06, 15.26, 16.4, 17.34, 18.3, 18.6, 19.58, 20.52, 21.48, 22.46, 22.46, 23.98, 23.98, 24.34, 14.4, 16.26, 12.08, 11.86, 12.25, 12.25, 14.26, 14.2, 14.1, 14.08, 14.14, 14.12, 13.86, 13.38, 12.82, 12.06, 11.04, 9.88, 8.52, 6.72, 5.12, 3.78, 2.78, 1.76, 1.3, 0.82, 0.42, 0.0, 0.0, 0.0, 0.66, 0.66, 0.66, 0.66, 0.0, 0.5, 0.7, 0.8, 0.9, 0.98, 0.48, 0.48, 0.48, 0.48, 0.48, 0.48, 0.48, 0.48, 1.28, 2.58, 4.3, 6.12, 6.12, 9.68, 10.8, 11.44, 12.42, 13.24, 13.62, 13.82, 14.16, 14.12, 13.96, 14.12, 14.24, 14.4, 14.54, 14.62, 14.72, 14.96, 15.02, 15.26, 15.54, 15.78, 15.86, 16.04, 15.94, 15.92, 15.94, 15.9, 15.94, 16.08, 16.2, 16.3, 16.64, 16.82, 16.86, 16.74, 16.58, 16.38, 16.12, 15.76, 15.76, 14.04, 13.6, 13.44, 11.12, 11.583, 11.583, 14.56, 15.0, 15.34, 16.12, 16.98, 17.78, 18.1, 18.24, 18.38, 18.18, 17.88, 17.84, 17.9, 17.64, 17.56, 17.52, 17.48, 17.62, 17.98, 17.98, 18.16, 18.1, 17.98, 14.48, 15.267, 15.267, 18.88, 18.98, 18.98, 19.0, 19.0, 19.0, 19.04, 19.06, 19.0, 18.94, 19.02, 19.06, 19.08, 19.12, 19.1, 18.6, 17.62, 16.26, 14.4, 12.62, 11.02, 10.0, 9.42, 9.36, 9.22, 9.12, 8.84, 8.5, 8.12, 7.9, 7.78, 7.72, 7.62, 7.4, 7.16, 6.92, 6.62, 6.22, 5.66, 4.92, 4.2, 3.48, 2.94, 2.9, 3.02, 3.7, 4.64, 5.74, 6.52, 7.16, 6.98, 6.06, 4.98, 3.9, 2.94, 2.28, 3.12, 3.9, 4.98, 6.4, 7.84, 8.28, 8.78, 9.46, 10.14, 10.62, 11.1, 11.18, 10.66, 9.86, 9.28, 8.76, 8.44, 8.14, 7.86, 7.58, 7.46, 7.6, 8.0, 8.42, 8.78, 8.96, 9.12, 9.22, 9.28, 9.22, 9.1, 8.82, 8.46, 8.1, 7.88, 7.82, 8.02, 8.3, 8.58, 8.82, 9.0, 9.0, 8.94, 8.66, 8.34, 7.94, 7.46, 6.88, 6.2, 4.72, 3.3, 2.7, 2.22, 2.28, 2.96, 4.04, 4.8, 5.7, 6.42, 7.3, 7.92, 8.26, 8.44, 8.58, 8.88, 8.88, 9.26, 9.36, 9.34, 7.42, 7.783, 9.42, 9.5, 9.62, 9.74, 9.82, 9.86, 9.9, 9.92, 9.92, 10.4, 10.48, 10.72, 8.56, 8.733, 10.16, 10.08, 9.78, 9.48, 9.1, 9.54, 6.52, 5.3, 4.32, 3.02, 3.817, 5.72, 7.38, 8.98, 10.12, 10.64, 10.78, 10.64, 10.52, 10.48, 10.46, 10.08, 9.72, 10.92, 8.1, 7.46, 6.44, 4.66, 5.35, 6.98, 7.76, 9.0, 9.42, 9.6, 9.6, 9.46, 9.34, 9.38, 9.5, 9.82, 10.32, 11.0, 11.36, 11.74, 12.48, 13.0, 13.38, 13.66, 13.18, 11.68, 10.4, 9.02, 8.04, 7.78, 7.88, 7.76, 7.46, 6.86, 6.1, 5.64, 5.42, 5.5, 5.86, 6.32, 6.46, 6.4, 6.32, 6.26, 6.14, 6.2, 6.46, 6.82, 7.44, 8.38, 9.08, 9.16, 8.68, 8.2, 7.92, 7.8, 8.04, 8.36, 7.82, 5.88, 4.78, 3.06, 1.66]

tabVitesse = [int(element*3.6) for element in tabVitesse]

tabStop = []
for i in range(len(tabVitesse)):
    if (tabVitesse[i] <= 0) : 
        tabStop.append(1)
    else : 
        tabStop.append(0)
        
# tabStop = [1,1,1,0,0,0,1,0,1,1,1]
# tabVitesse = []
# for i in range(len(tabStop)):
    # if (tabStop[i] == 1) : 
        # tabVitesse.append(0)
    # else : 
        # tabVitesse.append(20)      
    
print("tabStop    " + str(tabStop))
print("tabVitesse " + str(tabVitesse))


def functionStopDetection(tabVitesse, tabStop) :
    #Cette fonction permet detecter lorsqu'il y a des panneaux stop et selon la vitesse de l'élève à ce moment là, 
    #on va lui enlever ou non des points
    #
    #Cette fonction a en entreée 2 arguments qui sont les suivants: 
    # - tabVitesse : le tableau des vitesses
    # - tabStop    : le tableau des detections de stop
    #
    #En sortie on renvoit la note de l'élève
    
    ######### Traitement de la detection des panneaux stops #########
    pointsEleve = 0
    paireTimeDebutFin = []
    tabPaire = []
    flagFirstTime = True
    paireTimeDebutFin = []
    for time in range(len(tabStop)) :
        if (flagFirstTime == True) :
            stopAvant = tabStop[time]
            if (tabStop[time] == 1) :
                #on detecte un stop
                tabPaire.append(time) #time du début
            flagFirstTime = False
        else :
            if (stopAvant == 0) :
                #on avait pas detecter un stop au coup d'avant
                if (tabStop[time] == 1) :
                    #on detecte actuellement un stop
                    tabPaire.append(time) #temps du début
            else :
                #stopAvant == 1 cad on avait detecter un stop au coup d'avant
                if (tabStop[time] == 0) :
                    #on detecte actuellement plus de stop
                    pointsEleve = pointsEleve + 1 #incrémente les points
                    tabPaire.append(time) #temps de la fin
                    paireTimeDebutFin.append(tabPaire)
                    tabPaire = [] #initialise le tableau de paire
                    
            if (time == len(tabStop)-1) :
                if (tabStop[time] == 1) :
                    #on detecte un stop à la fin
                    pointsEleve = pointsEleve + 1 #incrémente les points
                    tabPaire.append(time+1)                
                    paireTimeDebutFin.append(tabPaire) 
                    
            stopAvant = tabStop[time]
    print("paireTimeDebutFin : " + str(paireTimeDebutFin))
    print("Detecte " + str(pointsEleve) + " stop(s)")

    ######### Regarde la vitesse lorsqu'on a detecte un panneau stop #########
    vitesseRalentie = False
    for i in range(len(paireTimeDebutFin)) :
        paire = paireTimeDebutFin[i]
        #print("Paire de time où il y a eu un stop " + str(paire))
        for j in range(paire[0],paire[1],1) :
            if (tabVitesse[j] <= 1) :
                #vitesse inférieur à 1km/h
                pointsEleve = pointsEleve - 1
                print("-->Vitesse : " + str(tabVitesse[j]) + "km/h à " + str(j) + "s")
                break
    if (pointsEleve > 10) :
        #nombre de point de l'élève est plafonné à 10 points
        pointsEleve = 10
        
    return pointsEleve 



pointsEleve1 = functionStopDetection(tabVitesse,tabStop)
######### Note final de l'élève ######### 
print("Point eleve final : " + str(pointsEleve1))
        
        
        
        
        
        