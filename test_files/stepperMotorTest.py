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

# Steps and delay 
nstep = 200
delay_time = 0.01
# Create an instance of the StepperMotor class
vertical_steppers = VerticalMotors(S1PINSTEP, S1PINDIR, S2PINSTEP, S2PINDIR)
horizontal_motor = HorizontalMotor(S3PINSTEP, S3PINDIR)

# Move vertical motors
vertical_steppers.move_up(100,0.1)

# Move horizontal motors 
horizontal_motor.move_right(100,0.01)

GPIO.cleanup()