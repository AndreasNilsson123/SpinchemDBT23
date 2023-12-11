import RPi.GPIO as GPIO
import time

class StepperMotor:
    def __init__(self, step_pin, direction_pin):
        """
        Initializes a new instance of the class.

        Args:
            step_pin (int): The GPIO pin number for the step signal.
            direction_pin (int): The GPIO pin number for the direction signal.

        Returns:
            None
        """
        self.step_pin = step_pin
        self.direction_pin = direction_pin
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)
        self.set_direction("clockwise")

    def set_direction(self, direction):
        """
        Set the direction of the motor.

        Args:
            direction (str): The direction in which to rotate the motor. Valid values are "clockwise" and "counterclockwise".

        Returns:
            None
        """
        if direction == "clockwise":
            GPIO.output(self.direction_pin, GPIO.HIGH)
        elif direction == "counterclockwise":
            GPIO.output(self.direction_pin, GPIO.LOW)

    def step(self, steps, delay, second_stepper_pin = 0):
        """
        Executes a specified number of steps with a specified delay between each step.

        Parameters:
            steps (int): The number of steps to execute.
            delay (float): The delay in seconds between each step.
            second_stepper_pin (int): The GPIO pin number for the second stepper motor.

        Returns:
            None
        """
        if second_stepper_pin == 0:
            for _ in range(steps):
                GPIO.output(self.step_pin, GPIO.HIGH)
                time.sleep(delay)
                GPIO.output(self.step_pin, GPIO.LOW)
                time.sleep(delay)
        elif not second_stepper_pin == 0:
            for _ in range(steps):
                GPIO.output(self.step_pin, GPIO.HIGH)
                GPIO.output(second_stepper_pin, GPIO.HIGH)
                time.sleep(delay)
                GPIO.output(self.step_pin, GPIO.LOW)
                GPIO.output(second_stepper_pin, GPIO.LOW)
                time.sleep(delay)
        