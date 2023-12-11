import RPi.GPIO as GPIO
import time

class Valve:
    def __init__(self, pin):
        """
        Initializes an instance of the class.
        
        Args:
            pin (int): The pin number to be used for GPIO setup.
        
        Returns:
            None
        """
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.close()

    def open(self):
        """
        Sets the specified GPIO pin to HIGH.

        Parameters:
            self (object): The instance of the class.
        
        Returns:
            None
        """
        GPIO.output(self.pin, GPIO.HIGH)

    def close(self):
        """
        Closes the GPIO pin.

        This function sets the GPIO pin specified during object initialization to a LOW state,
        effectively closing the pin.

        Parameters:
        - self: The object instance.

        Returns:
        - None
        """
        GPIO.output(self.pin, GPIO.LOW)
