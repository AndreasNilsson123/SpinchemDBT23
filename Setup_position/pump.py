import RPi.GPIO as GPIO

class Pump:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.stop()
    
    def start(self):
        GPIO.output(self.pin, GPIO.HIGH)
    
    def stop(self):
        GPIO.output(self.pin, GPIO.LOW)