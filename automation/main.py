import RPi.GPIO as GPIO
from valve import Valve
from pump import Pump
import time

GPIO.setmode(GPIO.BCM)

# Define GPIO pins for valve and pump
VALVE_PIN = 17
PUMP_PIN = 18

# Initialize valve and pump objects
valve = Valve(VALVE_PIN)
pump = Pump(PUMP_PIN)

# Open the valve
valve.open()

# Turn on the pump for a certain amount of time (e.g., 5 seconds)
pump.on()
time.sleep(5)
pump.off()

# Close the valve
valve.close()

# Clean up GPIO
GPIO.cleanup()
