import RPi.GPIO as GPIO
from valve import Valve
from pump import Pump
from stirrer_motor import StirrerMotor
from horizontalMotor import HorizontalMotor
from verticalMotors import VerticalMotors
from rbrDetection import rbrPocketDetection
import time

GPIO.setmode(GPIO.BCM)
# ------------------------------------------ #
# ----------- Initialize objects ----------- #
# ------------------------------------------ #

# Define GPIO pins for valve and pump
VALVE1_PIN = 17
VALVE2_PIN = 16

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

valve_emptying = Valve(VALVE2_PIN)


pocket1_detection = rbrPocketDetection(SENSOR_1_PIN, SENSOR_2_PIN)
pocket2_detection = rbrPocketDetection(SENSOR_3_PIN, SENSOR_4_PIN)

vertical_steppers = VerticalMotors(VERTICAL_STEPPER_1_STEP_PIN, VERTICAL_STEPPER_1_DIRECTION_PIN
                                  ,VERTICAL_STEPPER_2_STEP_PIN, VERTICAL_STEPPER_2_DIRECTION_PIN )
horizontal_motor = HorizontalMotor(HORIZONTAL_STEPPER_STEP_PIN, HORIZONTAL_STEPPER_DIRECTION_PIN)

# Define the serial port and baudrate
SERIAL_PORT = '/dev/ttyUSB0'  # Adjust based on your specific port
BAUDRATE = 9600  # Adjust based on your motor's specifications

# Initialize the stirrer motor object
stirrer = StirrerMotor(SERIAL_PORT, BAUDRATE)

# ------------------------------------------ #
# ------------- Help Methods --------------- #
# ------------------------------------------ #
def stirrer_command(stirrer: StirrerMotor, time: int, speed: int, command: str) -> None:
    """
    A function that sends a command to a stirrer motor.
    
    Parameters:
        stirrer: A StirrerMotor object representing the stirrer motor.
        time: An integer representing the time (in seconds) to execute the command.
        speed: An integer representing the speed of the stirrer motor.
        command: A string representing the command to be sent to the stirrer motor.
                ("Start" or "Stop")
    Returns:
        None
    """
    if command == "Start":
        command = "1,WSE," + str(speed) + "\r\n"
    elif command == "Stop":
        command = "1,WSE,0\r\n" 
    response = stirrer.send_command(command) # Fix input command

    if not response == "1,HS,OK":
        raise Exception("Unexpected response from stirrer: " + response)

            
# ------------------------------------------ #
# --------------- Automation --------------- #
# ------------------------------------------ #

# 1. Button for RBR pick-up
# 1.1 Locate new RBR using sensors
# 1.2 Move cradle to horizontal position of RBR
# 1.3 Move cradle to vertical position of RBR
# 1.4 Move cradle back to top vertical position

# 2. Button for moving RBR to vessel
# 2.1 Move cradle to horizontal position of vessel
# 2.2 Move cradle to vertical position of vessel

# 3. Fill the vessel with reagnet
# 3.1 Open valve for filling vessel
# 3.2 Keep the valve opend for a certain amount of time
# 3.3 Close valve for filling vessel
# 3.4 CONDITIONS: Vessel is empty from liquid

# 4. Start stirrer motor
# 4.1 Start stirrer motor with defined speed
# 4.2 CONDITIONS: Motor must be in vessel

# 5. Stop stirrer motor
# 5.1 Stop stirrer motor

# 6. Empty vessel from reagent
# 6.1 Open valve for emptying vessel
# 6.2 Keep the valve opend for a certain amount of time
# 6.3 Close valve for emptying vessel

# 7. Lift RBR from vessel
# 7.1 Lift cradle to top vertical position

# 8. Leave RBR into container
# 8.1 Move RBR into horizontal position of desired container
# 8.2 Move RBR into vertical position of desired container
# 8.3 Move RBR back to top vertical position
# 8.4 CONDITIONS: Container must be empty


# Close the serial connection when done
stirrer.serial.close()
# Clean up GPIO
GPIO.cleanup()

# Tip change
# stepperMotor <- horizontalMotors
# stepperMotor <- verticalMotors
# sensor <- pocketSensor