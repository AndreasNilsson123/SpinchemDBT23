import time
import RPi.GPIO as GPIO

class SwitchButton:
    def __init__(self, pin):
        """
        Initializes an instance of the class.

        Args:
            pin (int): The pin number to be initialized.

        Returns:
            None
        """
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def is_pressed(self):
        """
        Returns the current state of the button.

        :return: bool - True if the button is pressed, False otherwise.
        """
        return GPIO.input(self.pin)