'''
    Stepper Motor interfacing with Raspberry Pi
    http:///www.electronicwings.com
'''
import RPi.GPIO as GPIO
from time import sleep
#from stepper_controller import StepperMotor
from verticalMotors import VerticalMotors
from horizontalMotor import HorizontalMotor
# Initialize GPIO
GPIO.setmode(GPIO.BCM)

# Set up pins
S1PINSTEP = 17
S1PINDIR = 27
S2PINSTEP = 24
S2PINDIR = 25
S3PINSTEP = 22
S3PINDIR = 23

#0.00625 mm/step (160 step/mm), 125/20000 = 0.00625, 20000/125 = 160
# Steps and delay
dist = 50
nstep = 160*dist
delay_time = 0.00035 #Rec Min delay up 0.0035 
# Create an instance of the StepperMotor class
vertical_steppers = VerticalMotors(S3PINSTEP, S3PINDIR, S2PINSTEP, S2PINDIR)
horizontal_motor = HorizontalMotor(S1PINSTEP, S1PINDIR)

# Start stepper motor 1 
vertical_steppers.move_down(nstep, delay_time)
#horizontal_motor.move_left(250, 0.001)

# Start stepper motor 2
#horizontal_motor.move_right(steps=nstep, delay=0.1*delay_time)

GPIO.cleanup()