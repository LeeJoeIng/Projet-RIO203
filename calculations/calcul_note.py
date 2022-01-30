import numpy as np

def note(data):
  data['dist_s']=data['capteur_dist']/data['speed'] # Calcul de la distance en seconde
  data['acc_pb']=data['acceleration'].loc[(data['acceleration']>= 4.5) | (data['acceleration']<=- 4.5)]# détermination des accélération hors de l'intervalle [-4.5,4.5]
  data['dist_pb']=data['dist_s'].loc[data['dist_s']<2]#détermination des distance problématique

# calcul du nombre de fois où la voiture reste pendant plus de 5s à moins de 2s d'une autre voiture
  i=0
  compteur=0 #compteur de la durée passée à moins de 5 s
  nb_dist_pb=0
  while i<len(data['dist_pb']):
    if(np.isnan(data.loc[i,'dist_pb'])):
      compteur=0
    else:
      compteur+=1
      if(compteur==5):
        nb_dist_pb+=1
        compteur=0
    i+=1
  points_dist=10-nb_dist_pb

  #compte le nombre de points problématiques pour l'acceleration
  acc_pb=data['acc_pb'].loc[data['acc_pb'].isna()!=True].count()

  # calcul de la note liée à la ceinture
  seat_belt=data['seat_belt'].loc[data['seat_belt']==0].count()
  points_seat_belt=10-seat_belt

  #Cette fonction permet detecter lorsqu'il y a des panneaux stop et selon la vitesse de l'élève à ce moment là,
  #on va lui enlever ou non des points
  #
  #Cette fonction a en entreée 2 arguments qui sont les suivants:
  #  - tabVitesse : le tableau des vitesses en m/s
  # - tabStop    : le tableau des detections de stop
  #
  #En sortie on renvoit la note de l'élève

  #conversion m/s en km/h
  data['speed']=data['speed']*3.6
  tabVitesse=data['speed']
  tabStop=data['Stop']

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
          if (tabVitesse[j] <= 5) :
                #vitesse inférieur ou égale à 5km/h
              pointsEleve = pointsEleve - 1
                # print("-->Vitesse : " + str(tabVitesse[j]) + "km/h à " + str(j) + "s")
              break #sort de la boucle for j in range(paire[0],paire[1],1)
  if (pointsEleve > 10) :
        #nombre de point de l'élève est plafonné à 10 points
      pointsEleve = 10

  points_stop=10-pointsEleve


  # calcul de la note à attribuer
  points_acc=10-acc_pb

  # vérification qu'il n'y ait pas de notes negatives
  if points_acc<0:
    points_acc=0

  if points_dist<0:
    points_dist=0

  if points_seat_belt<0:
    points_seat_belt=0

  points_tot=points_acc+points_dist+points_seat_belt+points_stop
  return points_tot
