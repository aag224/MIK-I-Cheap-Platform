#Run in parallel a stepper motor and a peristaltic pump
import RPi.GPIO as GPIO
import time 
from time import sleep
import threading

GPIO.setmode(GPIO.BCM)

bomba_1=17
bomba_2=27
bomba_3=22
bomba_4=13
motor_A=24
motor_A1=12
motor_A2=20

GPIO.setup(bomba_1,GPIO.OUT)
GPIO.setup(bomba_2,GPIO.OUT)
GPIO.setup(bomba_3,GPIO.OUT)
GPIO.setup(bomba_4,GPIO.OUT)

GPIO.setup(motor_A,GPIO.OUT)
GPIO.setup(motor_A1,GPIO.OUT)
GPIO.setup(motor_A2,GPIO.OUT)
pw_A=GPIO.PWM(motor_A,500)
pw_A.start(0)

def Dir_L_motorA():
	GPIO.outout(12,0)
	GPIO.output(20,0)
	sleep(15)
	GPIO.output(12,0)
	print('Motor Activate \n')
	GPIO.output(20,1)
	pw_A.ChangeDutyCycle(80)
	sleep(10)
	print('Motor Deactivate \n')

def Dir_R_motorA():
	GPIO.outout(12,0)
	GPIO.output(20,0)
	sleep(30)
	GPIO.output(12,1)
	print('Motor Activate \n')
	GPIO.output(20,0)
	pw_A.ChangeDutyCycle(80)
	sleep(15)
	print('Motor Deactivate \n')	
	
def Pump_1():
	GPIO.output(13,1)
	sleep(80)
	GPIO.output(13,0)
	print('Pump 1 ON \n')
	sleep(20)
	GPIO.output(13,1)
	print('Pump 2 OFF \n')
	sleep(5)
def Pump_2():
	GPIO.output(22,1)
	sleep(30)
	GPIO.output(22,0)
	print('Pump 2 ON \n')
	sleep(16.5)
	GPIO.output(22,1)
	print('Pump 2 OFF \n')
	sleep(5)
def Pump_3():
	GPIO.output(27,1)
	print('Pump 3 ON \n')
	sleep(30)
	GPIO.output(27,0)
	print('Pump 3 OFF \n')
	sleep(5)
def Pump_4():
	GPIO.output(17,1)
	sleep(46.5)
	GPIO.output(17,0)
	print('Pump 4 ON \n')
	sleep(33.2)
	GPIO.output(17,1)
	print('Pump 4 OFF \n')
	sleep(5)
	

h1=threading.Thread(target=Pump_1)
h2=threading.Thread(target=Pump_2)
h3=threading.Thread(target=Pump_3)
h4=threading.Thread(target=Pump_4)
hm=threading.Thread(target=Dir_L_motorA)
hm2=threading.Thread(target=Dir_R_motorA)


h3.run()
hm.run()
h2.run()
h4.run()
h1.run()
hm2.run()

pw_A.stop()
GPIO.cleanup_()
