import RPi.GPIO as GPIO
import time
import numpy as np
from detection import ForceSensor

class rbrPocketDetection():
    def __init__(self, sensor1_pin, sensor2_pin):
        self.sensor1 = ForceSensor(sensor1_pin) # Top sensor
        self.sensor2 = ForceSensor(sensor2_pin) # Bottom sensor
    
    def detect_rbr(self):
        if self.sensor1.object_detected and not self.sensor2.object_detected:
            return True
        else:
            return False