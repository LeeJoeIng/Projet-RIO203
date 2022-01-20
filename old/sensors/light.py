#!/usr/bin/env python3
import sensors.PCF8591 as ADC
import RPi.GPIO as GPIO
import time

DO = 17
GPIO.setmode(GPIO.BCM)

def setup():
	ADC.setup(0x48)
	GPIO.setup(DO, GPIO.IN)

setup()

def get_light(has_light):
	if has_light:
		result = ADC.read(0)
		percentage = 100*(150-result)/150
		if percentage > 100:
			percentage = 100
		if percentage < 0:
			percentage = 0

		return str(int(percentage))
	return str(random.randint(0,100))
