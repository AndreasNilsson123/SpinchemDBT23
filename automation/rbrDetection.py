import RPi.GPIO as GPIO
import time
import numpy as np
from detection import ForceSensor
from position import Position

class rbrPocketDetection():
    def __init__(self, sensor1_pin, sensor2_pin, coord_x, coord_y, cycle_number):
        self.sensor1 = ForceSensor(sensor1_pin) # Top sensor
        self.sensor2 = ForceSensor(sensor2_pin) # Bottom sensor
        self.position = Position(coord_x, coord_y)
        factor = 6*100 # 6mm
        self.position_leave = Position(coord_x, coord_y+factor)
        self.cycle_number = cycle_number
        
    def detect_rbr(self):
        if self.sensor1.object_detected() and not self.sensor2.object_detected():
            return True
        else:
            return False
    
    def get_position_retrive(self):
        return self.position.get_position()
    
    def get_position_leave(self):
        return self.position_leave.get_position()
    
    def get_cycle_number(self):
        return self.cycle_number