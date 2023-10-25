import RPi.GPIO as GPIO
from valve import Valve
from pump import Pump
import time

GPIO.setmode(GPIO.BCM)

# Define GPIO pins for valve and pump
VALVE1_PIN = 17
VALVE2_PIN = 16
PUMP1_PIN = 18
PUMP2_PIN = 19

# Initialize valve and pump objects
valve_filling = Valve(VALVE1_PIN)
pump_filling = Pump(PUMP1_PIN)
valve_emptying = Valve(VALVE2_PIN)
pump_emptying = Pump(PUMP2_PIN)

#  ------- Filling sequence ------- #
def execute_valve_pump_sequence(wait_time: int, valve: Valve, pump: Pump) -> None:
    """
    Executes a sequence of actions involving a valve and a pump.

    Parameters:
        time (int): The amount of time to wait in seconds.
        valve (Valve): The valve object to be used.
        pump (Pump): The pump object to be used.

    Returns:
        None
    """
    valve.open()
    pump.turn_on()
    time.sleep(wait_time)
    pump.turn_off()
    valve.close()


# Fill the vessel
execute_valve_pump_sequence(5, valve_filling, pump_filling)

# Clean up GPIO
GPIO.cleanup()
