from position import Position
from valve import Valve
from liquid_detection import LiquidDetection
from pump import Pump
from time import sleep

# OBS: 21 seconds for 200 ml 
class Vessel:
    def __init__(self, pin_filling_reagent, pin_filling_acid,
                 pin_emptying, pump_filling,
                 pin_liquid_detection,
                 coord_x, coord_y):
        self.valve_reagent = Valve(pin_filling_reagent)
        self.valve_acid = Valve(pin_filling_acid)
        self.valve_emptying = Valve(pin_emptying)
        self.pump = Pump(pump_filling)
        self.liquid_detection = LiquidDetection(pin_liquid_detection)
        self.position = Position(coord_x, coord_y)
        self.volume_to_time = 0.105
        
    def fill_reagent(self, volume):
        if self.liquid_detection.is_filled(): # Change back to not
            filling_time = volume * self.volume_to_time
            self.valve_reagent.open()
            sleep(filling_time)
            self.valve_reagent.close()
        
    
    def fill_acid(self, volume):
        filling_time = volume * self.volume_to_time
        self.valve_acid.open()
        self.pump.start()
        sleep(filling_time)
        self.pump.stop()
        self.valve_acid.close()
        
    def empty_tank(self, time):
        self.valve_emptying.open()
        sleep(time)
        self.valve_emptying.close()
        
    def get_position(self):
        return self.position.get_position()