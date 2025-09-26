import RPi.GPIO as GPIO
import time
from time import sleep

bomb=[0,17,27,22,13,18]
pump=int(input("Select Pump 1, 2, 3, 4 or 5 (#): "))
tim=int(input("Operation time (s): "))

GPIO.setmode(GPIO.BCM)
GPIO.setup(bomb[pump],GPIO.OUT)


for i in range(1):
	GPIO.output(bomb[pump],0)
	print("Pump ON")
	sleep(tim)
	GPIO.output(bomb[pump],1)
	print("Pump OFF")
	sleep(2)
	
GPIO.cleanup()