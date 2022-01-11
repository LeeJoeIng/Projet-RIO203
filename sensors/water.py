#!/usr/bin/env python3
import sensors.PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import math

DO = 12
GPIO.setmode(GPIO.BCM)

def setup():
	ADC.setup(0x48)
	GPIO.setup(DO, GPIO.IN)

def Print(x):
	if x == 1:
		print ('')
		print ('   ***************')
		print ('   * Not raining *')
		print ('   ***************')
		print ('')
	if x == 0:
		print ('')
		print ('   *************')
		print ('   * Raining!! *')
		print ('   *************')
		print ('')

def loop():
	status = 1
	while True:
		print (ADC.read(0))
		
		tmp = GPIO.input(DO);
		if tmp != status:
			Print(tmp)
			status = tmp
		
		time.sleep(1)

setup()

def get_water(has_water):
	if has_water:
		result = ADC.read(0)
		percentage = (result - 50) / 160
		percentage = min(100, percentage)
		percentage = max(0, percentage)
		return str(int(percentage))
	return str(random.randint(0,100))
