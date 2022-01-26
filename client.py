from sensors.potentiometer import get_ceinture
from sensors.ultrasonic import timeAndDistance
import time as t

while True:
	print("état de la ceinture= ", get_ceinture())
	time, distance = timeAndDistance()
	print("time ultrasonic= ", time)
	print("distance (cm) =", distance)
	print()
	t.sleep(0.2)
