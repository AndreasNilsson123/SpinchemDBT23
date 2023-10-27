import RPi.GPIO as GPIO
from valve import Valve
from pump import Pump
from stepper_controller import StepperMotor
from stirrer_motor import StirrerMotor
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

# Initialize valve and pump objects
valve_filling = Valve(VALVE1_PIN)
pump_filling = Pump(PUMP1_PIN)
valve_emptying = Valve(VALVE2_PIN)
pump_emptying = Pump(PUMP2_PIN)

# Define GPIO pins for the stepper motors
VERTICAL_STEPPER_1_STEP_PIN = 22
VERTICAL_STEPPER_1_DIRECTION_PIN = 23

VERTICAL_STEPPER_2_STEP_PIN = 24
VERTICAL_STEPPER_2_DIRECTION_PIN = 25

HORIZONTAL_STEPPER_STEP_PIN = 4
HORIZONTAL_STEPPER_DIRECTION_PIN = 5

# Initialize stepper motor objects
vertical_stepper_1 = StepperMotor(VERTICAL_STEPPER_1_STEP_PIN, VERTICAL_STEPPER_1_DIRECTION_PIN)
vertical_stepper_2 = StepperMotor(VERTICAL_STEPPER_2_STEP_PIN, VERTICAL_STEPPER_2_DIRECTION_PIN)
horizontal_stepper = StepperMotor(HORIZONTAL_STEPPER_STEP_PIN, HORIZONTAL_STEPPER_DIRECTION_PIN)


# Stirr motor

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
    Activates the stirrer motor.

    Returns:
        None
    """
    response = stirrer.send_command("\r\n") # Fix input command
    stirrer.turn_on() 


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
