# From package hx711
import RPi.GPIO as GPIO
from hx711 import HX711

# Initialize GPIO
GPIO.setmode(GPIO.BCM)

# Define pins for each sensor
sensor_pins = [
    {'DT': 5, 'SCK': 6},
    {'DT': 13, 'SCK': 19},
    {'DT': 21, 'SCK': 20},
    {'DT': 16, 'SCK': 12}
]

# Initialize sensors
sensors = [HX711(dout=d['DT'], pd_sck=d['SCK']) for d in sensor_pins]

for sensor in sensors:
    sensor.set_reading_format("MSB", "MSB")
    sensor.set_reference_unit(1)  # Set reference unit to 1 (adjust as needed)
    sensor.reset()
    sensor.tare()

try:
    while True:
        for i, sensor in enumerate(sensors):
            weight = sensor.get_weight(5)
            print(f"Sensor {i + 1}: {weight} grams")
except KeyboardInterrupt:
    GPIO.cleanup()
