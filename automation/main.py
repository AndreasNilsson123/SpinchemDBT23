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
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtGui import QColor

#GPIO.setmode(GPIO.BCM)
# ------------------------------------------ #
# ---------------- Setup GUI --------------- #
# ------------------------------------------ #
# Get the directory path where the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------ #
# ----------- Initialize objects ----------- #
# ------------------------------------------ #

def setup_valves(PIN1, PIN2):
    valve_filling = Valve(PIN1)
    valve_emptying = Valve(PIN2)
    return valve_filling, valve_emptying

def setup_sensors(PIN1,PIN2,PIN3,PIN4):
    pocket1_detection = rbrPocketDetection(PIN1, PIN2)
    pocket2_detection = rbrPocketDetection(PIN3, PIN4)
    return pocket1_detection, pocket2_detection

def setup_cradle(V1_step, V1_dir,
                 V2_step, V2_dir,
                 H_step, H_dir,
                 sensor_v1, sensor_v2, 
                 sensor_h1,
                 vessel_sensor_y, vessel_sensor_x):
    cradle = Cradle(V1_step, V1_dir, V2_step, V2_dir, H_step, H_dir,
                    sensor_v1, sensor_v2, sensor_h1,vessel_sensor_y, vessel_sensor_x)
    return cradle

def setup_stirrer(SERIAL_PORT, BAUDRATE):
    stirrer = StirrerMotor(SERIAL_PORT, BAUDRATE)
    return stirrer
# Define the serial port and baudrate
#SERIAL_PORT = '/dev/ttyUSB0'  # Adjust based on your specific port
#BAUDRATE = 9600  # Adjust based on your motor's specifications

# Initialize the stirrer motor object
#stirrer = StirrerMotor(SERIAL_PORT, BAUDRATE)

# # ------------------------------------------ #
# # ------------- Help Methods --------------- #
# # ------------------------------------------ #
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
class Automation(QMainWindow):
    def __init__(self):
        super(Automation, self).__init__()
        loadUi(os.path.join(script_directory, "GUI_prototype.ui"), self)
        # Define neccessary parameters
        self.positionCalibration = False
        
        
        # Setup pins
        cradle = setup_cradle(V1_step=1, V1_dir=2, V2_step=3, V2_dir=4,
                                    H_step=5, H_dir=6, sensor_v1=7, sensor_v2=8,
                                    sensor_h1=9, vessel_sensor_y=10, vessel_sensor_x=11)
        # Step 1
        self.pickUp.clicked.connect(lambda: self.pickUpNewRBR(cradle))
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
        
        # Set the initial value of the QLineEdit to the lowest value of the slider
        initial_value = self.stirrerSpeed.minimum()
        self.dispStirrerSpeed.setText(str(initial_value))
        
        # Connect the slider valueChanged signal to the text box setText slot
        self.stirrerSpeed.valueChanged.connect(self.on_slider_value_changed)

    def on_slider_value_changed(self, value):
        # Convert the integer value to a string and set it in the text box
        self.dispStirrerSpeed.setText(str(value))        
    
    # 1. Button for RBR pick-up
    def pickUpNewRBR(self, cradle):
        # Run calibration
        if not self.positionCalibration:
            cradle.position_calibration()
        # 1.1 Locate new RBR using sensors
        # 1.2 Move cradle to horizontal position of RBR
        # 1.3 Move cradle to vertical position of RBR
        # 1.4 Move cradle back to top vertical position
            
        
        
        
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
#GPIO.cleanup()

# More fixes
# Fix so that switches <- horizontalMotor
# Fix so that switches <- verticalSteppers
# And add calibration method to these classes
# First calibration on verticalSteppers then one the horizontalMotor 
