# !/bin/bash
while true
do
	# Pi constant
	pi=$(echo "scale=10; 4*a(1)" | bc -l)

	# Get Results from Fit-IoT nodes for User1
	lum_speed_u1=$(curl -X GET "http://[2001:660:4403:0486::1757]") 
	tire_press_u1=$(curl -X GET "http://[2001:660:4403:0486::a090]") 
	# for user 2
	lum_speed_u2=$(curl -X GET "http://[2001:660:4403:0486::1057]")
        tire_press_u2=$(curl -X GET "http://[2001:660:4403:0486::a173]")

	echo "$lum_speed_u1"
	echo "$tire_press_u1"
	echo "$lum_speed_u2"
	echo "$tire_press_u2"

	# Read lines : separate luminosity from acceleration data 
	# User 1  
    	luminosite_u1=$(echo "$lum_speed_u1" | awk "NR==1")
	vitesse_u1=$(echo "$lum_speed_u1" | awk "NR==2")
	vitesse_ang_x_u1=$(echo "$lum_speed_u1" | awk "NR==3")

	# User 2 
        luminosite_u2=$(echo "$lum_speed_u2" | awk "NR==1")
        vitesse_u2=$(echo "$lum_speed_u2" | awk "NR==2")
        vitesse_ang_x_u2=$(echo "$lum_speed_u2" | awk "NR==3")

	# Check values
	#echo "$luminosite_u1"
	#echo "$vitesse_u1"
	#echo "$vitesse_ang_x_u1"
	#echo "$luminosite_u2"
        #echo "$vitesse_u2"
        #echo "$vitesse_ang_x_u2"

	# Calculate speed from angular speed
	# angular peed in m°/s => convert to °/s
	# Wheel radius = 0.2032
	# user 1
	vitesse_gyr_u1=$(echo $vitesse_ang_x_u1/1000*$pi*2*$pi*2032/10000/180|bc -l)
	
	# user 2
	vitesse_gyr_u2=$(echo $vitesse_ang_x_u2/1000*$pi*2*$pi*2032/10000/180|bc -l)
	
	# Check speed
	echo "$vitesse_gyr_u1"
	echo "$vitesse_gyr_u2"	

	# POST data for User 1
	#curl -X POST -d "{\"temperature\": $nb_alea}" http://localhost:8080/api/v1/MYTOKEN/telemetry --header "Content-Type:application/json"
	#curl -X POST -d "{\"temperature\": $nb_alea}" https://3888-109-10-158-165.ngrok.io/api/v1/MYTOKEN/telemetry --header "Content-Type:application/json"

	nb_temp=$((RANDOM%40))
	nb_vent=$((RANDOM%120))
	nb_pressionAir=$((RANDOM%1087))
	#nb_vitesse=$((RANDOM%200))		
	nb_flamme=$((RANDOM%2))	

	curl -X POST -d "{\"temperature\" : $nb_temp}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser1/telemetry --header "Content-Type:application/json"
	curl -X POST -d "{\"vent\" : $nb_vent}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser1/telemetry --header "Content-Type:application/json"
	curl -X POST -d "{\"pressionAir\" : $nb_pressionAir}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser1/telemetry --header "Content-Type:application/json"
	#curl -X POST -d "{\"humidite\" : 16}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser1/telemetry --header "Content-Type:application/json"
	#curl -X POST -d "{\"visibilite\" : '12.9'}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser1/telemetry --header "Content-Type:application/json"
	#curl -X POST -d "{\"pluie\" : 11}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser1/telemetry --header "Content-Type:application/json"
	#curl -X POST -d "{\"latitude\" : '48.862725'}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser1/telemetry --header "Content-Type:application/json"
	#curl -X POST -d "{\"longitude\" : '2.287592'}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser1/telemetry --header "Content-Type:application/json"	
	
        #curl -X POST -d "{\"vitesse\" : $nb_vitesse}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser1/telemetry --header "Content-Type:application/json"
	curl -X POST -d "$vitesse_u1" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser1/telemetry --header "Content-Type:application/json"
        
	curl -X POST -d "{\"flamme\" : $nb_flamme}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser1/telemetry --header "Content-Type:application/json"
	
	#curl -X POST -d "{\"luminosite\" : '4.868'}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser1/telemetry --header "Content-Type:application/json"
	curl -X POST -d "$luminosite_u1" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser1/telemetry --header "Content-Type:application/json"
	

        #curl -X POST -d "{\"pressionPneus\" : '1.3'}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser1/telemetry --header "Content-Type:application/json"
	curl -X POST -d "$tire_press_u1" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser1/telemetry --header "Content-Type:application/json"
	
	#curl -X POST -d "{\"etat\" : 'arret'}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser1/telemetry --header "Content-Type:application/json"
	#curl -X POST -d "{\"portes\" : 'fermees'}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser1/telemetry --header "Content-Type:application/json"
	#curl -X POST -d "{\"alerte\" : 'Il y a le feu!!!'}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser1/telemetry --header "Content-Type:application/json"

	# POST data for user 2
	#curl -X POST -d "{\"temperature\": $nb_alea}" http://localhost:8080/api/v1/MYTOKEN/telemetry --header "Content-Type:application/json"
        #curl -X POST -d "{\"temperature\": $nb_alea}" https://3888-109-10-158-165.ngrok.io/api/v1/MYTOKEN/telemetry --header "Content-Type:application/json"

        nb_temp=$((RANDOM%40))
        nb_vent=$((RANDOM%120))
        nb_pressionAir=$((RANDOM%1087))
        #nb_vitesse=$((RANDOM%200))
        nb_flamme=$((RANDOM%2))

        curl -X POST -d "{\"temperature\" : $nb_temp}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser2/telemetry --header "Content-Type:application/json"
        curl -X POST -d "{\"vent\" : $nb_vent}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser2/telemetry --header "Content-Type:application/json"
        curl -X POST -d "{\"pressionAir\" : $nb_pressionAir}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser2/telemetry --header "Content-Type:application/json"
        #curl -X POST -d "{\"humidite\" : 16}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser2/telemetry --header "Content-Type:application/json"
        #curl -X POST -d "{\"visibilite\" : '12.9'}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser2/telemetry --header "Content-Type:application/json"
        #curl -X POST -d "{\"pluie\" : 11}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser1/telemetry --header "Content-Type:application/json"
        #curl -X POST -d "{\"latitude\" : '48.862725'}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser2/telemetry --header "Content-Type:application/json"
        #curl -X POST -d "{\"longitude\" : '2.287592'}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser2/telemetry --header "Content-Type:application/json"

        #curl -X POST -d "{\"vitesse\" : $nb_vitesse}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser2/telemetry --header "Content-Type:application/json"
        curl -X POST -d "$vitesse_u2" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser2/telemetry --header "Content-Type:application/json"

        curl -X POST -d "{\"flamme\" : $nb_flamme}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser2/telemetry --header "Content-Type:application/json"
        curl -X POST -d "$luminosite_u2" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser2/telemetry --header "Content-Type:application/json"

        #curl -X POST -d "{\"pressionPneus\" : '1.3'}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser2/telemetry --header "Content-Type:application/json"
        curl -X POST -d "$tire_press_u2" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser2/telemetry --header "Content-Type:application/json"

        #curl -X POST -d "{\"etat\" : 'arret'}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser2/telemetry --header "Content-Type:application/json"
        #curl -X POST -d "{\"portes\" : 'fermees'}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser2/telemetry --header "Content-Type:application/json"
        #curl -X POST -d "{\"alerte\" : 'Il y a le feu!!!'}" https://3888-109-10-158-165.ngrok.io/api/v1/dataUser2/telemetry --header "Content-Type:application/json"
	
	echo "sleep"
	sleep 1	
done
