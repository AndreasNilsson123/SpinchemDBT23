from cradle import Cradle
from vessel import Vessel
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
def setup_cradle(V1_step, V1_dir,
                 V2_step, V2_dir,
                 H_step, H_dir,
                 sensor_v1, sensor_v2, 
                 sensor_h1,
                 vessel_sensor_y, vessel_sensor_x): # REVISION:
    cradle = Cradle(V1_step, V1_dir, V2_step, V2_dir, H_step, H_dir,
                    sensor_v1, sensor_v2, sensor_h1,vessel_sensor_y, vessel_sensor_x)
    return cradle

def setup_vessel(PIN_reagent, PIN_acid, PIN_emptying, PIN_pump, PIN_liquid,coord_x, coord_y): # REVISION: 
    vessel = Vessel(PIN_reagent, PIN_acid, PIN_emptying, PIN_pump, PIN_liquid, coord_x, coord_y)
    return vessel


vessel_x = 5*290
vessel_y = 0
horizontal_delay = 0.002


cradle = setup_cradle(V1_step=17, V1_dir=27, V2_step=24, V2_dir=25,
                            H_step=23, H_dir=22, sensor_v1=26, sensor_v2=21,
                            sensor_h1=13, vessel_sensor_x=19, vessel_sensor_y=11)
vessel = setup_vessel(PIN_reagent=18, PIN_acid=16,
                        PIN_emptying=12, PIN_pump=7, PIN_liquid=10,
                        coord_x=vessel_x, coord_y=vessel_y)

# Position calibration
cradle.position_calibration()
pos_x, pos_y = vessel.get_position()
cradle.move_to_x_coord(pos_x, horizontal_delay)