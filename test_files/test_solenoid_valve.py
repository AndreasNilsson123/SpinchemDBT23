#Import all neccessary features to code.
import RPi.GPIO as GPIO
from time import sleep

#If code is stopped while the solenoid is active it stays active
#This may produce a warning if the code is restarted and it finds the GPIO Pin, which it defines as non-active in next line, is still active
#from previous time the code was run. This line prevents that warning syntax popping up which if it did would stop the code running.
#GPIO.setwarnings(False)
#This means we will refer to the GPIO pins
#by the number directly after the word GPIO. A good Pin Out Resource can be found here https://pinout.xyz/
GPIO.setmode(GPIO.BCM)
#This sets up the GPIO 18 pin as an output pin
GPIO.setup(18, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup()

while (True):    
    
    #This Turns Relay Off. Brings Voltage to Max GPIO can output ~3.3V
    GPIO.output(18, 1)
    #This Turns Relay Off. Brings Voltage to Max GPIO can output ~3.3V
    GPIO.output(16, 1)
   #This Turns Relay Off. Brings Voltage to Max GPIO can output ~3.3V
    GPIO.output(7, 1)
    #This Turns Relay Off. Brings Voltage to Max GPIO can output ~3.3V
    GPIO.output(12, 1)

    sleep(150)

    #This Turns Relay Off. Brings Voltage to Max GPIO can output ~3.3V
    GPIO.output(18, 0)
    #This Turns Relay Off. Brings Voltage to Max GPIO can output ~3.3V
    GPIO.output(16, 0)
   #This Turns Relay Off. Brings Voltage to Max GPIO can output ~3.3V
    GPIO.output(7, 0)
    #This Turns Relay Off. Brings Voltage to Max GPIO can output ~3.3V
    GPIO.output(12, 0)
    
    sleep(50)
    #Wait 1 Seconds
    sleep(1)