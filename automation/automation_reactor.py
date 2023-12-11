import RPi.GPIO as GPIO
import threading
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

def setup_vessel(PIN_reagent, PIN_acid, PIN_emptying, PIN_pump, PIN_liquid,coord_x, coord_y): # REVISION: 
    vessel = Vessel(PIN_reagent, PIN_acid, PIN_emptying, PIN_pump, PIN_liquid, coord_x, coord_y)
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
                 vessel_sensor_y, vessel_sensor_x): # REVISION:
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
        pocket1_y = int(131*160)
        pocket2_x = int(28.6*5)
        pocket2_y = int(131*160)
        
        # Other variables
        self.vesselVolume = 300
        self.acidVolume = 5
        self.emptyTime = 30
        self.dryingTime = 10
        self.is_running = False
        
        
        # Initiate sliders
        self.dispStirrerSpeed.setText(str(self.stirrerSpeed.minimum()))
        self.dispStirrerSpeed_3.setText(str(self.stirrerSpeed_3.minimum()))
        self.dispOperationalTime.setText(str(self.operationalTime.minimum()))
        self.dispOperationalTime_3.setText(str(self.operationalTime_3.minimum()))
        self.stirrerSpeed.valueChanged.connect(lambda: self.on_slider_value_changed(self.dispStirrerSpeed, self.stirrerSpeed.value()))
        self.stirrerSpeed_3.valueChanged.connect(lambda: self.on_slider_value_changed(self.dispStirrerSpeed_3, self.stirrerSpeed_3.value()))
        self.operationalTime.valueChanged.connect(lambda: self.on_slider_value_changed(self.dispOperationalTime, self.operationalTime.value()))
        self.operationalTime_3.valueChanged.connect(lambda: self.on_slider_value_changed(self.dispOperationalTime_3, self.operationalTime_3.value()))
        
        
        # Needs changing
        cradle = setup_cradle(V1_step=17, V1_dir=27, V2_step=24, V2_dir=25,
                                    H_step=22, H_dir=23, sensor_v1=26, sensor_v2=21,
                                    sensor_h1=13, vessel_sensor_x=19, vessel_sensor_y=11)
        vessel = setup_vessel(PIN_reagent=18, PIN_acid=16,
                              PIN_emptying=12, PIN_pump=7, PIN_liquid=10,
                              coord_x=vessel_x, coord_y=vessel_y)

        
        pocket2, pocket1 = setup_sensors(PIN1=3, PIN2=2,
                                         PIN3=9, PIN4=4, 
                                         coord_x1 = pocket1_x, coord_y1 = pocket1_y, 
                                         coord_x2 = pocket2_x, coord_y2 = pocket2_y)
        pockets = [pocket1, pocket2]
        
        stirrer = setup_stirrer('/dev/serial0', 9600)
        
        # Start process
        self.stopButton.setEnabled(False)
        self.startButton.clicked.connect(lambda: self.start_process(cradle, vessel, pockets, stirrer))
        self.stopButton.clicked.connect(self.stop_process)
    
    def on_slider_value_changed(self, var, value):
        # Convert the integer value to a string and set it in the text box
        #self.dispStirrerSpeed.setText(str(value))
        var.setText(str(value))    

    def start_process(self,cradle, vessel, pockets, stirrer):
        if not self.is_running:
            # Update UI
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(True)

            # Start process in a separate thread
            self.thread = threading.Thread(target= lambda:self.process_thread(cradle, vessel, pockets, stirrer))
            self.is_running = True
            self.thread.start()

    def stop_process(self):
        if self.is_running:
            # Stop the process
            self.is_running = False

            # Wait for the thread to finish
            self.thread.join()

            # Update UI
            self.startButton.setEnabled(True)
            self.stopButton.setEnabled(False)

    def process_thread(self, cradle, vessel, pockets, stirrer):
        # Your process code goes here
        while self.is_running:
            # Run your process
            QApplication.processEvents()  # Allow GUI updates
            while not pockets[0].detect_rbr() or pockets[1].detect_rbr():
                # Position calibration
                print("Hello1")
                if not self.positionCalibration:
                    cradle.position_calibration()
                    self.positionCalibration = True
                print("Hello2")
                for pocket in pockets:
                    if pocket.detect_rbr():
                        pocket_retrive_x, pocket_retrive_z = pocket.get_position_retrive()
                        pocket_leave_x, pocket_leave_z = pocket.get_position_leave()
                        break
            
                # Move to RBR position
                cradle.move_to_x_coord(pocket_retrive_x, self.horizontal_delay)
                cradle.move_to_z_coord(pocket_retrive_z, self.vertical_delay)
                
                # Move RBR to vessel
                vessel_x, vessel_z = vessel.get_position()
                cradle.move_to_z_coord(0, self.vertical_delay)
                cradle.move_to_x_coord(vessel_x, self.horizontal_delay)
                # Revision: add sensor check
                cradle.move_to_z_coord(vessel_z, self.vertical_delay)
                # Revision: add sensor check
                
                # Fill vessel with reagent
                vessel.fill_reagent(self.vesselVolume)
                
                # Fill vessel with acid
                vessel.fill_acid(self.acidVolume)
                
                # Start and stop stirrer
                stirrer_command(stirrer, 500, "Start")
                sleep(20)
                stirrer_command(stirrer, 500, "Stop")
                # Revision: Read from GUI
                
                # Empty the vessel
                vessel.empty(self.emptyTime)
                
                # Dry RBR
                stirrer_command(stirrer, 500, "Start")
                vessel.empty(self.dryingTime)
                stirrer_command(stirrer, 0, "Stop")
                
                # Leave RBR
                cradle.move_to_z_coord(0, self.vertical_delay)
                cradle.move_to_x_coord(pocket_leave_x, self.horizontal_delay)
                cradle.move_to_z_coord(pocket_leave_z, self.vertical_delay)
                cradle.move_to_z_coord(0, self.vertical_delay)
                

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
          