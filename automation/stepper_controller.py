import RPi.GPIO as GPIO
import time

class StepperMotor:
    def __init__(self, step_pin, direction_pin):
        self.step_pin = step_pin
        self.direction_pin = direction_pin
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)
        self.set_direction("clockwise")

    def set_direction(self, direction):
        if direction == "clockwise":
            GPIO.output(self.direction_pin, GPIO.HIGH)
        elif direction == "counterclockwise":
            GPIO.output(self.direction_pin, GPIO.LOW)

    def step(self, steps, delay):
        for _ in range(steps):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(delay)