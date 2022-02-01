import json

class Eleves:
    
    def __init__(self, **dic_eleves):
        for attr_name,attr_value in dic_eleves.items():
            setattr(self,attr_name,attr_value)


class Moniteurs:

    def __init__(self,**dic_moniteur):
        for attribute_name,attribute_value in dic_moniteur.items():
            setattr(self,attribute_name,attribute_value) 

def main():
    #Moniteurs
    max_creneau=0
    nom_creneau=0
    max_code_route=0
    nom_code_route=0
    max_ceinture=0
    nom_ceinture=0
    max_distance=0
    nom_distance=0
    max_klaxon=0
    nom_klaxon=0
    for dic_moniteur in json.load(open("moniteurs.json")):
        moniteur = Moniteurs(**dic_moniteur)
        if(moniteur.creneau > max_creneau):
            max_creneau=moniteur.creneau
            nom_creneau= moniteur.name
        if(moniteur.code_route > max_code_route):
            max_code_route= moniteur.code_route
            nom_code_route=moniteur.name
        if(moniteur.ceinture > max_ceinture):
            max_ceinture = moniteur.ceinture
            nom_ceinture= moniteur.name
        if(moniteur.distance > max_distance):
            max_distance= moniteur.distance
            nom_distance = moniteur.name
        if(moniteur.klaxon > max_klaxon):
            max_klaxon = moniteur.klaxon
            nom_klaxon = moniteur.name
    #Eleves
    max_creneau_eleve=0
    nom_creneau_eleve=0
    max_code_route_eleve=0
    nom_code_route_eleve=0
    max_ceinture_eleve=0
    nom_ceinture_eleve=0
    max_distance_eleve=0
    nom_distance_eleve=0
    max_klaxon_eleve=0
    nom_klaxon_eleve=0
    for dic in json.load(open("eleves.json")):
        point_eleve = Eleves(**dic)
        if(point_eleve.creneau > max_creneau_eleve):
            max_creneau_eleve=point_eleve.creneau
            nom_creneau_eleve= point_eleve.name
        if(point_eleve.code_route > max_code_route_eleve):
            max_code_route_eleve= point_eleve.code_route
            nom_code_route_eleve=point_eleve.name
        if(point_eleve.ceinture > max_ceinture_eleve):
            max_ceinture_eleve = point_eleve.ceinture
            nom_ceinture_eleve= point_eleve.name
        if(point_eleve.distance > max_distance_eleve):
            max_distance_eleve= point_eleve.distance
            nom_distance_eleve = point_eleve.name
        if(point_eleve.klaxon > max_klaxon_eleve):
            max_klaxon_eleve = point_eleve.klaxon
            nom_klaxon_eleve = point_eleve.name



    #Eleves
    for dic_eleves in json.load(open("eleves.json")):
        eleve = Eleves(**dic_eleves)
        if(eleve.creneau < 5):      #Créneau
            print(eleve.name,"Vous devez vous exercer davantage en créneau. Le moniteur le mieux placé pour vous aidé est",nom_creneau, "il a", max_creneau, "points de créneau")
            print("Vous pouvez aussi vous faire aider par",nom_creneau_eleve,"il a",max_creneau_eleve,"points")
        if(eleve.code_route < 5):      #Code de la route
            print(eleve.name,"Vous devez vous exercer davantage en code de la route. Le moniteur le mieux placé pour vous aidé est", nom_code_route,"il a",max_code_route,"points de code de la route")
            print("Vous pouvez aussi vous faire aider par",nom_code_route_eleve,"il a",max_code_route_eleve,"points")
        if(eleve.ceinture < 5):      #Ceinture
            print(eleve.name,"Vous devez attacher davantage votre ceinture. Le moniteur le mieux placé pour vous aidé est", nom_ceinture, "il a", max_ceinture, "points de ceinture")
            print("Vous pouvez aussi vous faire aider par",nom_ceinture_eleve,"il a",max_ceinture_eleve,"points")
        if(eleve.distance < 5):      #Créneau
            print(eleve.name,"Vous devez respecter davantage la distance entre les voitures. Le moniteur le mieux placé pour vous aider est", nom_distance,"il a", max_distance,"points de distance")
            print("Vous pouvez aussi vous faire aider par",nom_distance_eleve,"il a",max_distance_eleve,"points")
        if(eleve.klaxon < 5):      #Créneau
            print(eleve.name,"Vous devez klaxonner davantage. Le moniteur le mieux placé pour vous aider est", nom_klaxon,"il a", max_klaxon,"points de klaxon")
            print("Vous pouvez aussi vous faire aider par",nom_klaxon_eleve,"il a",max_klaxon_eleve,"points")
main()