'''
    Stepper Motor interfacing with Raspberry Pi
    http:///www.electronicwings.com
'''
import RPi.GPIO as GPIO
from time import sleep
from stepper_controller import StepperMotor

# Initialize GPIO
GPIO.setmode(GPIO.BCM)

# Set up pins
S1PINSTEP = 17
S1PINDIR = 27

S2PINSTEP = 22
S2PINDIR = 23

# Steps and delay 
nstep = 200
delay_time = 0.001
# Create an instance of the StepperMotor class
stepperMotor1 = StepperMotor(S1PINSTEP, S1PINDIR)
stepperMotor2 = StepperMotor(S2PINSTEP, S2PINDIR)

# Start stepper motor 1 
stepperMotor1.step(nstep, delay_time)
stepperMotor2.set_direction("clockwise")
# Start stepper motor 2
stepperMotor2.step(nstep, delay_time)

GPIO.cleanup()