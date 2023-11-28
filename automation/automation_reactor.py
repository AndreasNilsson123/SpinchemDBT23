import RPi.GPIO as GPIO
from vessel import Vessel
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
from PyQt5.QtCore import Qt

GPIO.setmode(GPIO.BCM)
# ------------------------------------------ #
# ---------------- Setup GUI --------------- #
# ------------------------------------------ #
# Get the directory path where the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------ #
# ----------- Initialize objects ----------- #
# ------------------------------------------ #

def setup_vessel(PIN1, PIN2, coord_x, coord_y):
    vessel = Vessel(PIN1,PIN2, coord_x, coord_y)
    return vessel

def setup_sensors(PIN1,PIN2,PIN3,PIN4, coord_x1, coord_y1, coord_x2, coord_y2):
    pocket1_detection = rbrPocketDetection(PIN1, PIN2, coord_x=coord_x1, coord_y=coord_y1)
    pocket2_detection = rbrPocketDetection(PIN3, PIN4, coord_x=coord_x2, coord_y=coord_y2)
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
# # ------------------------------------------ #
# # ------------- Help Methods --------------- #
# # ------------------------------------------ #
def stirrer_command(stirrer: StirrerMotor, speed: int, command: str) -> None:
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
    print(command)
    stirrer.send_command(command)
    
class Automation(QMainWindow):
    def __init__(self):
        super(Automation, self).__init__()
        loadUi(os.path.join(script_directory, "GUI_automation.ui"), self)
        # Define neccessary parameters
        self.positionCalibration = False
        self.vertical_delay = 0.001
        self.horizontal_delay = 0.002
        self.current_pocket = 0
        
        # Position of objects
        vessel_x = 268*5
        vessel_y = 122*160
        
        pocket1_x = int(128.4*5)
        pocket1_y = 131*160
        
        pocket2_x = int(28.6*5)
        pocket2_y = 131*160
        
        # setup pins
        cradle = setup_cradle(V1_step=17, V1_dir=27, V2_step=22, V2_dir=23,
                                    H_step=24, H_dir=25, sensor_v1=26, sensor_v2=21,
                                    sensor_h1=13, vessel_sensor_y=19, vessel_sensor_x=20)
        vessel = setup_vessel(PIN1=18, PIN2=16,
                              coord_x=vessel_x, coord_y=vessel_y)
        
        pocket2, pocket1 = setup_sensors(PIN1 = 8, PIN2 = 9,
                                         PIN3 = 10, PIN4 = 11, 
                                         coord_x1 = pocket1_x, coord_y1 = pocket1_y, 
                                         coord_x2 = pocket2_x, coord_y2 = pocket2_y)
        pockets = [pocket1, pocket2]
        
        stirrer = setup_stirrer('/dev/serial0', 9600)
        
        # Start process
        self.stopButton.setEnabled(False)
        self.startButton.clicked.connect(lambda: self.startProcess(cradle, vessel, pockets, stirrer))
        
        def startProcess(cradle, vessel, pockets, stirrer):
            # Initiate buttons
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(True)
            # Check possibility for multi threading