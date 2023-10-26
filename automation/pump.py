import RPi.GPIO as GPIO
import time

class Pump:
    def __init__(self, pin):
        """
        Initializes an instance of the class with the specified pin.

        Parameters:
            pin (int): The pin number to be used for the GPIO setup.

        Returns:
            None
        """
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.off()

    def on(self):
        """
        Turn on the GPIO pin.
        """
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        """
        Turn off the specified GPIO pin.

        This function sets the specified GPIO pin to a low voltage level, effectively turning it off.

        Parameters:
            self (object): The object instance.
        
        Returns:
            None
        """
        GPIO.output(self.pin, GPIO.LOW)
