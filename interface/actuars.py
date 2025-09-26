import time
from time import sleep
import RPi.GPIO as GPIO

def pumpsWork(number,pin=int(),timework=float()):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin,GPIO.OUT)
    
    GPIO.output(pin,0)
    print(f"Pump{number}_ON")
    sleep(timework)
    GPIO.output(pin,1)
    print(f"Pump{number}_OFF")
    sleep(1)

def pumpsWorkTC(number,pin=int(),timewait=float(),timework=float()):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin,GPIO.OUT)

    GPIO.output(pin,1)
    print(f"Pump{number}_OFF")
    sleep(timewait)
    GPIO.output(pin,0)
    print(f"Pump{number}_ON")
    sleep(timework)
    GPIO.output(pin,1)
    print(f"Pump{number}_OFF")
    sleep(1)

def stirring(pin1=int(), pin2=int(), timework=int()):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin1,GPIO.OUT)
    GPIO.setup(pin2,GPIO.OUT)
    pw_s = GPIO.PWM(pin2,500)
    pw_s.start(0)
    
    GPIO.output(pin2,0)
    pw_s.ChangeDutyCycle(65)
    sleep(timework)
    GPIO.output(pin2,1)
    sleep(1)
    
def cleanUp(ans,array,flows):
    vol = 4
    if ans:
        for kei in array:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(kei,GPIO.OUT)
            
            GPIO.output(kei,0)
            sleep(1)
            print("Start cleaning...")
            GPIO.output(kei,1)
            sleep(1)
            GPIO.output(kei,0)
            print("Solvent removing the residues...")
            sleep(vol/flows[kei])
            GPIO.output(kei,1)
            sleep(1)
            print("Purging...")
            for i in range(3):
                GPIO.output(kei,0)
                sleep(0.5)
                GPIO.output(kei,1)
                sleep(0.5)
    
    
    
    
    
    
    
    