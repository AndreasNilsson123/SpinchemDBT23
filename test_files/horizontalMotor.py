import time
import numpy as np
from stepper_controller import StepperMotor

class HorizontalMotor(StepperMotor):
    def __init__(self, step_pin, direction_pin):
        super().__init__(step_pin, direction_pin)
        self.set_direction("clockwise")
        self.conversion_factor = ...

    def move_right(self, steps, delay):
        """
        Moves the motors up by a certain number of steps with a specified delay.

        Parameters:
            steps (int): The number of steps to move the motors up.
            delay (float): The delay between each step.

        Returns:
            None
        """
        self.set_direction("clockwise")
        self.step(steps, delay)

    def move_left(self, steps, initial_delay, final_delay):
        """
        Moves the object down by a specified number of steps with a given delay.

        :param steps: The number of steps to move down (int).
        :param delay: The delay between each step (float).
        """
        self.set_direction("counterclockwise")
        self.step(steps, initial_delay, final_delay)
    
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