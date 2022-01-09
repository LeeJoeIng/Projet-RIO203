#!/bin/bash
# Script pour récupérer la consommation et le voltage de chaque noeud

while true
do

  # Get .oml files from ssh front-end
  scp riotp6@lille.iot-lab.info:~/.iot-lab/last/consumption/*.oml ./

  #### node 149 ###
  total_lines=$(wc -l m3_149.oml | awk '{ print $1 }')
  echo "number of lines in file m3_149.oml : $total_lines"

  power_comsumption_149=$(awk "FNR==$total_lines" m3_149.oml | awk '{print $8}')
  voltage_149=$(awk "FNR==$total_lines" m3_149.oml | awk '{print $7}')
	
  timestamp=$(awk "FNR==$total_lines" m3_149.oml | awk '{print $4}')
  datetime=$(date -r $timestamp | awk '{print $5}')

  echo "power consumption (node 149) : $power_comsumption_149"
  echo "voltage (node 149): $voltage_149"
  echo "timestamp (node 149) : $timestamp"
  echo "converted to datetime (node 149) : $datetime"


  ### node 150 ###
  total_lines=$(wc -l m3_150.oml | awk '{ print $1 }')
  echo "number of lines in file m3_150.oml : $total_lines"

  # Get power consumption & voltage measured at the same time than node 149 
  power_comsumption_150=$(awk -v pat="$timestamp" '$4 ~ pat' m3_150.oml| awk 'END{print $8}')
  voltage_150=$(awk -v pat="$timestamp" '$4 ~ pat' m3_150.oml| awk 'END{print $7}')

  echo "power consumption (node 150) : $power_comsumption_150"
  echo "voltage (node 150): $voltage_150"


  ### node 151 ###
  total_lines=$(wc -l m3_151.oml | awk '{ print $1 }')
  echo "number of lines in file m3_151.oml : $total_lines"

  # Get power consumption & voltage measured at the same time than node 149
  power_comsumption_151=$(awk -v pat="$timestamp" '$4 ~ pat' m3_151.oml| awk 'END{print $8}')
  voltage_151=$(awk -v pat="$timestamp" '$4 ~ pat' m3_151.oml| awk 'END{print $7}')

  echo "power consumption (node 151) : $power_comsumption_3"
  echo "voltage (node 151): $voltage_151"


  ### node 152 ###
  total_lines=$(wc -l m3_152.oml | awk '{ print $1 }')
  echo "number of lines in file m3_152.oml : $total_lines"

  # Get power consumption & voltage measured at the same time than node 149 
  power_comsumption_152=$(awk -v pat="$timestamp" '$4 ~ pat' m3_152.oml| awk 'END{print $8}')
  voltage_152=$(awk -v pat="$timestamp" '$4 ~ pat' m3_152.oml| awk 'END{print $7}')
	
  datetime=$(date -r $timestamp | awk '{print $5}')

  echo "power consumption (node 152) : $power_comsumption_4"
  echo "voltage (node 152): $voltage_152"

  # Total power consumption
  total_consumption=$(echo $power_comsumption_149+$power_comsumption_150+$power_comsumption_151+$power_comsumption_152|bc)
  echo "$total_consumption"

  # TODO : ADD POST TO THINGSBOARD

  sleep 30

done
