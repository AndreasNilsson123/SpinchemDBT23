from position import Position
from valve import Valve

class Vessel:
    def __init__(self, pin_filling, pin_emptying,coord_x, coord_y):
        self.valve_filling = Valve(pin_filling)
        self.valve_emptying = Valve(pin_emptying)
        self.position = Position(coord_x, coord_y)
        
    def open_filling(self):
        self.valve_filling.open()
        
    def close_filling(self):
        self.valve_filling.close()
        
    def open_emptying(self):
        self.valve_emptying.open()
        
    def close_emptying(self):
        self.valve_emptying.close()
        
    def get_position(self):
        return self.position