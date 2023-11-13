import time
from stepper_controller import StepperMotor
import numpy as np

class VerticalMotors:
    def __init__(self, step_pin_1, direction_pin_1, step_pin_2, direction_pin_2):
        """
        Initializes a new instance of the class.

        Parameters:
            step_pin_1 (int): The step pin for vertical motor 1.
            direction_pin_1 (int): The direction pin for vertical motor 1.
            step_pin_2 (int): The step pin for vertical motor 2.
            direction_pin_2 (int): The direction pin for vertical motor 2.

        Returns:
            None
        """
        self.vertical_motor_1 = StepperMotor(step_pin_1, direction_pin_1)
        self.vertical_motor_2 = StepperMotor(step_pin_2, direction_pin_2)

        # Set default direction for vertical motors
        self.vertical_motor_1.set_direction("clockwise")
        self.vertical_motor_2.set_direction("clockwise")
        
        self.conversion_factor = ...

    def move_up(self, steps, delay):
        """
        Moves the motors up by a certain number of steps with a specified delay.

        Parameters:
            steps (int): The number of steps to move the motors up.
            delay (float): The delay between each step.

        Returns:
            None
        """
        self.vertical_motor_1.set_direction("counterclockwise")
        self.vertical_motor_2.set_direction("counterclockwise")
        for _ in range(steps):
            self.vertical_motor_1.step(1, delay)
            self.vertical_motor_2.step(1, delay)

    def move_down(self, steps, delay):
        """
        Moves the object down by a specified number of steps with a given delay.

        :param steps: The number of steps to move down (int).
        :param delay: The delay between each step (float).
        """
        self.vertical_motor_1.set_direction("clockwise")
        self.vertical_motor_2.set_direction("clockwise")
        for _ in range(steps):
            self.vertical_motor_1.step(1, delay)
            self.vertical_motor_2.step(1, delay)
    
    def distance_to_steps(self, distance):
        """
        Calculate the number of steps required to move a given distance.

        Args:
            distance (float): The distance to be converted to steps.

        Returns:
            int: The number of steps required to move the given distance.
        """
        steps = np.round(self.conversion_factor * distance)
        return steps