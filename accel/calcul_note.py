data=dataframe.loc[:,['time','speed','acceleration']]
data['capteur_dist']=[random.randrange(0,50) for i in range(len(data['time']))]#génère la distance de façon random

data['dist_s']=data['capteur_dist']/data['speed'] # Calcul de la distance en seconde 
data['acc_pb']=data['acceleration'].loc[(data['acceleration']>= 4.5) | (data['acceleration']<=- 4.5)]# détermination des accélération hors de l'intervalle [-4.5,4.5]
data['dist_pb']=data['dist_s'].loc[(data['dist_s']<2)&(data['speed']!=0)]#détermination des distance problématique

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
  

#compte le nombre de points problématiques pour l'acceleration
acc_pb=data['acc_pb'].loc[data['acc_pb'].isna()!=True].count()

print('nombre d acceleration problématique=', acc_pb, 'temps totale passé à une distance inférienre à 2s, pendant plus de 5s=',nb_dist_pb)

# calcul de la note à attribuer 
points_acc=10-acc_pb
if points_acc<0:
  points_acc=0
points_dist=10-nb_dist_pb
if points_dist<0:
  points_dist=0
points_tot=points_acc+points_dist
print(points_tot)
