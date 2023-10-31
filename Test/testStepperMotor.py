import RPi.GPIO as GPIO
import time
import unittest

# Import the StepperMotor class from the respective file
from automation.stepper_controller import StepperMotor

class TestStepperMotor(unittest.TestCase):
    def setUp(self):
        # Initialize the GPIO pins
        GPIO.setmode(GPIO.BOARD)
        
        # Create an instance of the StepperMotor class
        self.stepperMotor = StepperMotor(29, 31)
        
    def tearDown(self):
        # Clean up the GPIO pins
        GPIO.cleanup()
        
    def test_set_direction(self):
        # Test setting the direction to clockwise
        self.stepperMotor.set_direction("clockwise")
        self.assertEqual(GPIO.input(self.stepperMotor.direction_pin), GPIO.HIGH)
        
        # Test setting the direction to counterclockwise
        self.stepperMotor.set_direction("counterclockwise")
        self.assertEqual(GPIO.input(self.stepperMotor.direction_pin), GPIO.LOW)
        
    def test_step(self):
        # Test stepping the motor 5 times with a delay of 0.1 seconds
        self.stepperMotor.step(5, 0.1)
        
        # Add assertions here to check the expected behavior of the stepper motor
        
if __name__ == '__main__':
    unittest.main()