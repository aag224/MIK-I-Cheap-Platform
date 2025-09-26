import RPi.GPIO as GPIO
import time
from time import sleep

pump1=13
pump2=22
pump3=27
pump4=17

GPIO.setmode(GPIO.BCM)
GPIO.setup(pump1,GPIO.OUT)
GPIO.setup(pump2,GPIO.OUT)
GPIO.setup(pump3,GPIO.OUT)
GPIO.setup(pump4,GPIO.OUT)

for i in range(1):
	print("Reaction start")
	GPIO.output(pump3,0)
	GPIO.output(pump2,1)
	GPIO.output(pump4,1)
	GPIO.output(pump1,1)
	print("Pump 3 ON")
	sleep(24)
	GPIO.output(pump3,1)
	print("Pump 3 OFF")
	sleep(2)
	GPIO.output(pump2,0)
	print("Pump 2 ON")
	sleep(25)
	GPIO.output(pump2,1)
	print("Pump 2 OFF")
	sleep(2)
	GPIO.output(pump1,0)
	print("Pump 1 ON")
	sleep(2)
	GPIO.setup(pump1,1)
	print("Pump 1 OFF")
	sleep(30)
	GPIO.output(pump4,0)
	print("Pump 4 ON")
	sleep(22)
	GPIO.output(pump4,1)
	print("Pump 4 OFF")
	sleep(2)
	print("Reaction continues")
	sleep(1500)
	print("")
	print("Reaction end :)!")
GPIO.cleanup()
