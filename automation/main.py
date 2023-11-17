import RPi.GPIO as GPIO
from valve import Valve
from stirrer_motor import StirrerMotor
from rbrDetection import rbrPocketDetection
from cradle import Cradle
from time import sleep
import sys
import os
from PyQt5.uic import loadUiType
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QDateEdit
from PyQt5.QtGui import QColor

GPIO.setmode(GPIO.BCM)
# ------------------------------------------ #
# ---------------- Setup GUI --------------- #
# ------------------------------------------ #
# Get the directory path where the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))
GUI_prototype, _ = loadUiType(os.path.join(script_directory, "GUI_prototype.ui"))

# ------------------------------------------ #
# ----------- Initialize objects ----------- #
# ------------------------------------------ #

def setup_valves(PIN1, PIN2):
    valve_filling = Valve(PIN1)
    valve_emptying = Valve(PIN2)
    return valve_filling, valve_emptying
# Define GPIO pins for valve and pump
#VALVE1_PIN = 17 ; VALVE2_PIN = 16

def setup_sensors(PIN1,PIN2,PIN3,PIN4):
    pocket1_detection = rbrPocketDetection(PIN1, PIN2)
    pocket2_detection = rbrPocketDetection(PIN3, PIN4)
    return pocket1_detection, pocket2_detection
# Sensor pins
#SENSOR_1_PIN = 10 ; SENSOR_2_PIN = 11 ; SENSOR_3_PIN = 12 ; SENSOR_4_PIN = 13
def setup_cradle(V1_step, V1_dir, V2_step, V2_dir, H_step, H_dir):
    cradle = Cradle(V1_step, V1_dir, V2_step, V2_dir, H_step, H_dir, 5,6,13,19,26)
    return cradle
# Define GPIO pins for the stepper motors
#VERTICAL_STEPPER_1_STEP_PIN = 22 ; VERTICAL_STEPPER_1_DIRECTION_PIN = 23
#VERTICAL_STEPPER_2_STEP_PIN = 24 ; VERTICAL_STEPPER_2_DIRECTION_PIN = 25
#HORIZONTAL_STEPPER_STEP_PIN = 4 ; HORIZONTAL_ 98 ++++++++++++++++STEPPER_DIRECTION_PIN = 5
# Initialize valve and pump objects
#valve_filling = Valve(VALVE1_PIN)
#valve_emptying = Valve(VALVE2_PIN)
# Pocket detection
#pocket1_detection = rbrPocketDetection(SENSOR_1_PIN, SENSOR_2_PIN)
#pocket2_detection = rbrPocketDetection(SENSOR_3_PIN, SENSOR_4_PIN)
# Stepper controllers
#vertical_steppers = VerticalMotors(VERTICAL_STEPPER_1_STEP_PIN, VERTICAL_STEPPER_1_DIRECTION_PIN
#                                  ,VERTICAL_STEPPER_2_STEP_PIN, VERTICAL_STEPPER_2_DIRECTION_PIN )
#horizontal_motor = HorizontalMotor(HORIZONTAL_STEPPER_STEP_PIN, HORIZONTAL_STEPPER_DIRECTION_PIN)

def setup_stirrer(SERIAL_PORT, BAUDRATE):
    stirrer = StirrerMotor(SERIAL_PORT, BAUDRATE)
    return stirrer
# Define the serial port and baudrate
#SERIAL_PORT = '/dev/ttyUSB0'  # Adjust based on your specific port
#BAUDRATE = 9600  # Adjust based on your motor's specifications

# Initialize the stirrer motor object
#stirrer = StirrerMotor(SERIAL_PORT, BAUDRATE)

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
class Automation(QDialog, GUI_prototype):
    def __init__(self):
        super(Automation, self).__init()
        self.setupUi(self)
        # Step 1
        self.pickUp.clicked.connect(self.pickUpNewRBR)
        # Step 2
        self.rbrToVessel.clicked.connect(self.moveRBRToVessel)
        # Step 3
        self.fillVessel.clicked.connect(self.fillTheVessel)
        # Step 4
        self.startMotor.clicked.connect(self.startStirrerMotor)
        # Step 5
        self.stopMotor.clicked.connect(self.stopStirrerMotor)
        # Step 6
        self.emptyVessel.clicked.connect(self.emptyTheVessel)
        # Step 7
        self.liftRbr.clicked.connect(self.liftRBRFromVessel)
        # Step 8
        self.leaveRbr.clicked.connect(self.leaveRBRInPocket)        
# 1. Button for RBR pick-up
# 1.1 Locate new RBR using sensors
# 1.2 Move cradle to horizontal position of RBR
# 1.3 Move cradle to vertical position of RBR
# 1.4 Move cradle back to top vertical position
    def pickUpNewRBR(self):
        print("Picking up new RBR")
# 2. Button for moving RBR to vessel
# 2.1 Move cradle to horizontal position of vessel
# 2.2 Move cradle to vertical position of vessel
    def moveRBRToVessel(self):
        print("Moving RBR to vessel")
# 3. Fill the vessel with reagnet
# 3.1 Open valve for filling vessel
# 3.2 Keep the valve opend for a certain amount of time
# 3.3 Close valve for filling vessel
# 3.4 CONDITIONS: Vessel is empty from liquid
    def fillTheVessel(self):
        print("Filling vessel")
# 4. Start stirrer motor
# 4.1 Start stirrer motor with defined speed
# 4.2 CONDITIONS: Motor must be in vessel
    def startStirrerMotor(self):
        print("Starting stirrer motor")
# 5. Stop stirrer motor
# 5.1 Stop stirrer motor
    def stopStirrerMotor(self):
        print("Stopping stirrer motor")
# 6. Empty vessel from reagent
# 6.1 Open valve for emptying vessel
# 6.2 Keep the valve opend for a certain amount of time
# 6.3 Close valve for emptying vessel
    def emptyTheVessel(self):
        print("Emptying vessel")
# 7. Lift RBR from vessel
# 7.1 Lift cradle to top vertical position
    def liftRBRFromVessel(self):
        print("Lifting RBR from vessel")
# 8. Leave RBR into container
# 8.1 Move RBR into horizontal position of desired container
# 8.2 Move RBR into vertical position of desired container
# 8.3 Move RBR back to top vertical position
# 8.4 CONDITIONS: Container must be empty
    def leaveRBRInPocket(self):
        print("Leaving RBR in pocket")
      
# ------------------------------------------ #
# --------------- Main --------------------- #
# ------------------------------------------ #
app = QApplication(sys.argv)
GUI = Automation()
widget = QtWidgets.QStackedWidget()
widget.addWidget(GUI)
widget.setFixedHeight(480)
widget.setFixedWidth(800)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting program")      
        
# Close the serial connection when done
#stirrer.serial.close()
# Clean up GPIO
GPIO.cleanup()

# More fixes
# Fix so that switches <- horizontalMotor
# Fix so that switches <- verticalSteppers
# And add calibration method to these classes
# First calibration on verticalSteppers then one the horizontalMotor 
