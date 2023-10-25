import RPi.GPIO as GPIO
import time

class Valve:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.close()

    def open(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def close(self):
        GPIO.output(self.pin, GPIO.LOW)
