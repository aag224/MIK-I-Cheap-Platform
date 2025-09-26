import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BCM)
pump1=13
GPIO.setup(pump1,GPIO.OUT)
pump2=22
GPIO.setup(pump2,GPIO.OUT)
pump3=27
GPIO.setup(pump3,GPIO.OUT)
pump4=17
GPIO.setup(pump4,GPIO.OUT)
pump5=18
GPIO.setup(pump5,GPIO.OUT)
stir=12
GPIO.setup(stir,GPIO.OUT)

rstir=20
GPIO.setup(rstir,GPIO.OUT)
lstir=21
GPIO.setup(lstir,GPIO.OUT)
pw_s=GPIO.PWM(stir,500)
pw_s.start(0)

GPIO.output(pump1,1)
GPIO.output(pump2,1)
GPIO.output(pump3,1)
GPIO.output(pump4,1)
GPIO.output(pump5,1)


volp1=float(input("Volume_pump_1(mL): "))
volp2=float(input("Volume_pump_2(mL): "))
volp3=float(input("Volume_pump_3(mL): "))
volp4=float(input("Volume_pump_4(mL): "))
volp5=float(input("Volume_pump_5(mL): "))
charge=str(input("Consider the load time? (Y/N) "))
flow=[28,0.24,0.21,0.27,0.28]
tc=[1,17,18,18,17]


if charge == "Y":   

     def Pmp1():
         GPIO.output(pump1,0)
         print("Pump1_ON")
         sleep(volp1/flow[0]+tc[0])
         print("Pump1 _OFF")
         GPIO.output(pump1,1)
         sleep(1)
     def Pmp2():
         GPIO.output(pump2,0)
         print("Pump2_ON")
         sleep(volp2/flow[1]+tc[1])
         print("Pump2_OFF")
         GPIO.output(pump2,1)
         sleep(1)
     def sti1():
         GPIO.output(rstir,0)
         print("Stir_ON ...")
         pw_s.ChangeDutyCycle(65)
         sleep(5)
         print("Stir_OFF")
         GPIO.output(rstir,1)
         sleep(1)
     def Pmp3():
         GPIO.output(pump3,0)
         print("Pump3_ON")
         sleep(volp3/flow[2]+tc[2])
         print("Pump3_OFF")
         GPIO.output(pump3,1)
         sleep(1)
     def Pmp4():
         GPIO.output(pump4,0)
         print("Pump4_ON")
         sleep(volp4/flow[3]+tc[3])
         print("Pump4_OFF")
         GPIO.output(pump4,1)
         sleep(1)
     def sti2():
         GPIO.output(rstir,0)
         print("Stir_ON ...")
         pw_s.ChangeDutyCycle(65)
         sleep(1500)
         GPIO.output(rstir,1)
         print("Stir_OFF  ")
         sleep(1)
     def Pmp5():
         GPIO.output(pump5,0)
         print("Pump5_ON")
         sleep(volp5/flow[4]+tc[4])
         print("Pump5_OFF")
         GPIO.output(pump5,1)
         sleep(1)
elif charge == "N":
     def Pmp1():
         GPIO.output(pump1,0)
         print("Pump1_ON")
         sleep(volp1/flow[0])
         print("Pump1_OFF")
         GPIO.output(pump1,1)
         sleep(1)
     def Pmp2():
         GPIO.output(pump2,0)
         print("Pump2_ON")
         sleep(volp2/flow[1])
         print("Pump2_OFF")
         GPIO.output(pump2,1)
         sleep(1)
     def sti1():
         GPIO.output(rstir,0)
         print("Stir_ON ...")
         pw_s.ChangeDutyCycle(65)
         sleep(5)
         GPIO.output(rstir,1)
         print("Stir_OFF")
         sleep(1)
     def Pmp3():
         GPIO.output(pump3,0)
         print("Pump3_ON")
         sleep(volp3/flow[2])
         print("Pump3_OFF")
         GPIO.output(pump3,1)
         sleep(1)
     def Pmp4():
         GPIO.output(pump4,0)
         print("Pump4_ON")
         sleep(volp4/flow[3])
         print("Pump4_OFF")
         GPIO.output(pump4,1)
         sleep(1)
     def Pmp5():
         GPIO.output(pump5,0)
         print("Pump5_ON")
         sleep(volp5/flow[4])
         print("Pump5_OFF")
         GPIO.output(pump5,1)
         sleep(1)
     def sti2():
         GPIO.output(rstir,0)
         print("Stir_ON ...")
         pw_s.ChangeDutyCycle(65)
         sleep(1500)
         GPIO.output(rstir,1)
         print("Stir_OFF ")
         sleep(1)

else: 
     print("Only Y or N")
     charge = str(input("Consider the load time? (Y/N) "))


Pmp2()
Pmp3()
sti1()
Pmp1()
sti1()
Pmp4()
sti1()
Pmp5()
sti2()

GPIO.cleanup()   
