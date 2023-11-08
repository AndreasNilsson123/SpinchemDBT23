import RPi.GPIO as GPIO
import time

class ForceSensor:
    def __init__(self, pin):
        """
        Initializes an instance of the class.

        Parameters:
            pin (int): The pin number to be used for GPIO setup.

        Returns:
            None
        """
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)

    def object_detected(self):
        """
        Checks if an object is detected by reading the input from the GPIO pin.

        Returns:
            bool: True if an object is detected, False otherwise.
        """
        return GPIO.input(self.pin)
