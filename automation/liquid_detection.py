import RPi.GPIO as GPIO


class LiquidDetection:
    def __init__(self, pin_sensor):
        self.pin = pin_sensor
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
    def is_filled(self):
        return GPIO.input(self.pin)

