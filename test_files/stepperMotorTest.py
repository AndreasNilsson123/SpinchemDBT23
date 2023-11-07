'''
    Stepper Motor interfacing with Raspberry Pi
    http:///www.electronicwings.com
'''
import RPi.GPIO as GPIO
from time import sleep
from stepper_controller import StepperMotor

# Initialize GPIO
GPIO.setmode(GPIO.BCM)

# Create an instance of the StepperMotor class
stepperMotor = StepperMotor(18, 23)
stepperMotor.step(10,0.1)
