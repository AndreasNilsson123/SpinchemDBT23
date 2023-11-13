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
stepperMotor = StepperMotor(27, 17)
stepperMotor.step(200,0.001)
stepperMotor.set_direction("counterclockwise")
stepperMotor.step(200,0.001)

GPIO.cleanup()