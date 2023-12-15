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

    def step(self, steps, initial_delay, final_delay):
        """
        Executes a specified number of steps with a speed ramping delay between each step.

        Parameters:
            steps (int): The number of steps to execute.
            initial_delay (float): The initial delay in seconds between each step.
            final_delay (float): The final delay in seconds between each step.

        Returns:
            None
        """
        # Determine the step size for the speed ramping
        delay_step = (initial_delay - final_delay) / steps

        # Determine the direction based on the number of steps
        direction = GPIO.HIGH if steps > 0 else GPIO.LOW
        GPIO.output(self.direction_pin, direction)

        # Execute the specified number of steps with speed ramping
        for _ in range(abs(steps)):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(initial_delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(initial_delay)
            
            # Adjust the delay for the next step
            initial_delay -= delay_step
            # Ensure the delay doesn't go below the final_delay
            initial_delay = max(initial_delay, final_delay)

        # Reset the direction pin after completing the steps
        GPIO.output(self.direction_pin, GPIO.LOW)