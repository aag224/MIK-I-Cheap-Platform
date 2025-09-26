import RPi.GPIO as GPIO
import time
from time import sleep

pin_pumps = {"1" : 13,    # Pins for each pump
         "2" : 22,
         "3" : 27,
         "4" : 17,
         "5" : 18}
pin_stiring = {"stir" : 12,	# Pin for the stirring plate 
               "r" : 20,	# Pins for the directions of the stirring plate
               "l" : 21}

GPIO.setmode(GPIO.BCM)		# Call mode of the pins
for pin in pin_pumps:		# Pin setup for each pump
    GPIO.setup(pin_pumps.get(pin),GPIO.OUT)
GPIO.setup(pin_stiring.get("stir"),GPIO.OUT) 
GPIO.setup(pin_stiring.get("r"),GPIO.OUT)	 
GPIO.setup(pin_stiring.get("l"),GPIO.OUT)
pw_s=GPIO.PWM(pin_stiring.get("stir"),500)  # Creation of the PWM object for the stirring plate
pw_s.start(0)                               # Start of the PWM with 0% duty cycle

for pump in pin_pumps:                  # Initialization of the pumps in OFF state
    GPIO.output(pin_pumps.get(pump),1)

vol_entry = ["volp1","volp2","volp3","volp4"]
volp5 = 100
vol_assg = []
for ventry in vol_entry:                # Input of the volumes to add for each pump
    ventry = float(input("Volume_to_Add_Pump_",vol_entry.index(ventry) ,"(mL): "))
    vol_assg.append(ventry)
charge=str(input("Consider the load time? (Y/N) "))     # Input to consider the load time
flow=[28,0.24,0.21,0.27,0.28]           # Flow rates of each pump (mL/s)
tc=[1,17,18,18,17]                      # Charge times for each pump (s)

def PumpsWorkWChrg(numberPump,volume,flow,chargeTime): # Function modular for the addition of a solution with charge time
    GPIO.output(pin_pumps[str(numberPump)],0)
    print("Pump",numberPump,"_ON")
    print("Adding reactive",numberPump)
    sleep(volume/flow+chargeTime)
    print("Pump",numberPump,"_OFF")
    GPIO.output(pin_pumps[str(numberPump)],1)
    sleep(1)

def PumpsWork(numberPump,volume,flow):  # Function modular for the addition of a solution without charge time
    GPIO.output(pin_pumps[str(numberPump)],0)
    print("Pump",numberPump,"_ON")
    print("Adding reactive",numberPump)
    sleep(volume/flow)
    print("Pump",numberPump,"_OFF")
    GPIO.output(pin_pumps[str(numberPump)],1)
    sleep(1)

def MixReac(direction,time):    # Fuction modular for the stirring plate
    GPIO.output(pin_stiring[str(direction)],0)
    print("Stir_ON ...")
    pw_s.ChangeDutyCycle(65)
    sleep(1)
    pw_s.ChangeDutyCycle(55)
    sleep(1)
    pw_s.ChangeDutyCycle(50)
    sleep(time)
    print("Stir_OFF")
    GPIO.output(pin_stiring[str(direction)],1)
    sleep(1)

while True:     # Cycle to consider or not the charge time
    if charge == "Y":   
        PumpsWorkWChrg(1,vol_assg[1],flow[1],tc[1]) # Adding reactant 1
        PumpsWorkWChrg(2,vol_assg[2],flow[2],tc[2])	# Adding reactant 2
        MixReac("r",5)					            # Start stirring
        PumpsWorkWChrg(3,vol_assg[3],flow[3],tc[3])	# Adding reactant 3
        PumpsWorkWChrg(4,vol_assg[4],flow[4],tc[4])	# Adding reactant 4
        PumpsWorkWChrg(5,volp5,flow[0],tc[0])	    # Coling water
        MixReac("r",10)					            # Final stirring
        break
    elif charge == "N":
        PumpsWork(1,vol_assg[1],flow[1]) 
        PumpsWork(2,vol_assg[2],flow[2]) 
        MixReac("r",5)                   
        PumpsWork(3,vol_assg[3],flow[3])  
        PumpsWork(4,vol_assg[4],flow[4])
        PumpsWork(5,volp5,flow[0])
        MixReac("r",10)
        break
    else: 
        print("Only Y or N")
        charge = str(input("Consider the load time? (Y/N) "))

GPIO.cleanup()  

