#!/usr/bin/env python3
import sensors.PCF8591 as ADC
import time

def setup():
	ADC.setup(0x48)

setup()

def get_ceinture():
	if ADC.read(0) > 128:
		return 1
	return 0
