import RPi.GPIO as GPIO
from valve import Valve
from pump import Pump
from stepper_controller import StepperMotor
from stirrer_motor import StirrerMotor
from detection import ForceSensor
import time

GPIO.setmode(GPIO.BCM)
# ------------------------------------------ #
# ----------- Initialize objects ----------- #
# ------------------------------------------ #

# Define GPIO pins for valve and pump
VALVE1_PIN = 17
VALVE2_PIN = 16
PUMP1_PIN = 18
PUMP2_PIN = 19

# Sensor pins
SENSOR_1_PIN = 10
SENSOR_2_PIN = 11
SENSOR_3_PIN = 12
SENSOR_4_PIN = 13

# Define GPIO pins for the stepper motors
VERTICAL_STEPPER_1_STEP_PIN = 22
VERTICAL_STEPPER_1_DIRECTION_PIN = 23

VERTICAL_STEPPER_2_STEP_PIN = 24
VERTICAL_STEPPER_2_DIRECTION_PIN = 25

HORIZONTAL_STEPPER_STEP_PIN = 4
HORIZONTAL_STEPPER_DIRECTION_PIN = 5

# Initialize valve and pump objects
valve_filling = Valve(VALVE1_PIN)
pump_filling = Pump(PUMP1_PIN)
valve_emptying = Valve(VALVE2_PIN)
pump_emptying = Pump(PUMP2_PIN)

# Initialize sensor objects
sensor_1 = ForceSensor(SENSOR_1_PIN)
sensor_2 = ForceSensor(SENSOR_2_PIN)
sensor_3 = ForceSensor(SENSOR_3_PIN)
sensor_4 = ForceSensor(SENSOR_4_PIN)
sensors = [sensor_1, sensor_2, sensor_3, sensor_4] #Turn sensors into a list

# Initialize stepper motor objects
vertical_stepper_1 = StepperMotor(VERTICAL_STEPPER_1_STEP_PIN, VERTICAL_STEPPER_1_DIRECTION_PIN)
vertical_stepper_2 = StepperMotor(VERTICAL_STEPPER_2_STEP_PIN, VERTICAL_STEPPER_2_DIRECTION_PIN)
horizontal_stepper = StepperMotor(HORIZONTAL_STEPPER_STEP_PIN, HORIZONTAL_STEPPER_DIRECTION_PIN)

# Define the serial port and baudrate
SERIAL_PORT = '/dev/ttyUSB0'  # Adjust based on your specific port
BAUDRATE = 9600  # Adjust based on your motor's specifications

# Initialize the stirrer motor object
stirrer = StirrerMotor(SERIAL_PORT, BAUDRATE)

# ------------------------------------------ #
# ---------------- Methods ----------------- #
# ------------------------------------------ #

# Filling and emptying sequence 
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
    
def move_vertical_motors(stepperMotor: StepperMotor, direction: int, steps: int, delay: int) -> None:
    """
    Moves the vertical motors based on the given parameters.

    Args:
        stepperMotor (StepperMotor): The stepper motor object to control the vertical motors.
        direction (int): The direction of movement. 0 indicates clockwise (Up), 1 indicates counterclockwise (Down).
        steps (int): The number of steps to move the motors.
        delay (int): The delay between each step.

    Returns:
        None: This function does not return anything.
    """
    if direction == 0: # clockwise (Up)
        stepperMotor.set_direction(stepperMotor,"clockwise")
    elif direction == 1: # clockwise (Down)
        stepperMotor.set_direction(stepperMotor,"counterclockwise")
    stepperMotor.step(stepperMotor, steps, delay)
    
def move_horizotal_motors(stepperMotor: StepperMotor, direction: int, steps: int, delay: int) -> None:
    """
    Moves the horizontal motors in a specified direction by a certain number of steps with a given delay.

    Parameters:
        stepperMotor (StepperMotor): The stepper motor object.
        direction (int): The direction in which to move the motors. 0 for clockwise (Right), 1 for counterclockwise (Left).
        steps (int): The number of steps to move the motors.
        delay (int): The delay between each step.

    Returns:
        None
    """
    if direction == 0: # clockwise (Right)
        stepperMotor.set_direction(stepperMotor,"clockwise")
    elif direction == 1: # clockwise (Left)
        stepperMotor.set_direction(stepperMotor,"counterclockwise")
    stepperMotor.step(stepperMotor, steps, delay)

def activate_stirrer(stirrer: StirrerMotor, time: int, speed: int) -> None:
    """
    Activate the stirrer motor for a specified amount of time at a given speed.

    Args:
        stirrer (StirrerMotor): The stirrer motor object.
        time (int): The duration of stirring in seconds.
        speed (int): The speed of the stirrer motor.

    Returns:
        None
    """
    response = stirrer.send_command("\r\n") # Fix input command
    stirrer.turn_on() 

def detect_objects(sensors):
    """
    Detects objects using the given sensors.

    Parameters:
    - sensors (list): A list of sensor objects.

    Returns:
    - None
    """
    for idx, sensor in enumerate(sensors, start=1):
        if sensor.object_detected():
            print(f"Sensor {idx}: Object detected")
        else:
            print(f"Sensor {idx}: No object detected")

# ------------------------------------------ #
# --------------- Automation --------------- #
# ------------------------------------------ #


# Fill the vessel
execute_valve_pump_sequence(5, valve_filling, pump_filling)

# Example code for stirrer control

# Example Usage:
# Send commands to the stirrer motor
response = stirrer.send_command("START\r\n")
print(f"Response from stirrer motor: {response}")



# Close the serial connection when done
stirrer.serial.close()
# Clean up GPIO
GPIO.cleanup()
