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
    pocket1_detection = rbrPocketDetection(PIN1, PIN2, coord_x=coord_x1, coord_y=coord_y1, cycle_number=0)
    pocket2_detection = rbrPocketDetection(PIN3, PIN4, coord_x=coord_x2, coord_y=coord_y2, cycle_number=1)
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
        self.vertical_delay = 0.0013
        self.horizontal_delay = 0.002
        self.current_pocket = 0
        
        # Position of objects
        vessel_x = 5*295
        vessel_y = 125*100
        pocket1_x = int(3*5)
        pocket1_y = int(133*100)
        pocket2_x = int(111*5)
        pocket2_y = int(133*100)
        
        # Other variables
        self.vesselVolume = 500
        self.acidVolume = 50
        self.emptyTime = 15
        self.dryingTime = 15
        self.is_running = False
        
        
        # Initiate sliders
        self.dispStirrerSpeed.setText(str(self.stirrerSpeed.minimum()))
        self.dispStirrerSpeed_3.setText(str(self.stirrerSpeed_3.minimum()))
        self.dispOperationalTime.setText(str(self.operationalTime.minimum()))
        self.dispOperationalTime_3.setText(str(self.operationalTime_3.minimum()))
        
        # Change recorded movement of sliders
        self.stirrerSpeed.valueChanged.connect(lambda: self.on_slider_value_changed(self.dispStirrerSpeed, self.stirrerSpeed.value()))
        self.stirrerSpeed_3.valueChanged.connect(lambda: self.on_slider_value_changed(self.dispStirrerSpeed_3, self.stirrerSpeed_3.value()))
        self.operationalTime.valueChanged.connect(lambda: self.on_slider_value_changed(self.dispOperationalTime, self.operationalTime.value()))
        self.operationalTime_3.valueChanged.connect(lambda: self.on_slider_value_changed(self.dispOperationalTime_3, self.operationalTime_3.value()))
        

        
        # Needs changing
        cradle = setup_cradle(V1_step=17, V1_dir=27, V2_step=24, V2_dir=25,
                                H_step=23, H_dir=22, sensor_v1=26, sensor_v2=21,
                                sensor_h1=13, vessel_sensor_x=19, vessel_sensor_y=11)
        vessel = setup_vessel(PIN_reagent=18, PIN_acid=16,
                              PIN_emptying=12, PIN_pump=7, PIN_liquid=10,
                              coord_x=vessel_x, coord_y=vessel_y)

        
        pocket1, pocket2 = setup_sensors(PIN1=3, PIN2=2,
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
        var.setText(str(value))    

    def start_process(self,cradle, vessel, pockets, stirrer):
        if not self.is_running:
            # Update UI
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(True)

            # Start process in a separate thread
            self.thread = threading.Thread(target = lambda:self.process_thread(cradle, vessel, pockets, stirrer))
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
            self.positionCalibration = False
    
    def move_to_pocket(self, cradle, pos_x, pos_z):
        print("HELLLOOOO!!!")
        cradle.move_to_x_coord(pos_x, self.horizontal_delay)
        cradle.move_to_z_coord(pos_z, self.vertical_delay)
        cradle.move_to_z_coord(0, self.vertical_delay)
    
    def move_to_vessel(self, cradle, pos_x, pos_z):
        cradle.move_to_x_coord(pos_x, self.horizontal_delay)
        # Revision: add sensor check
        cradle.move_to_z_coord(pos_z, self.vertical_delay)

    def process_thread(self, cradle, vessel, pockets, stirrer):
        # Your process code goes here
        # Create list of slider values
        self.slider_speed_values = [self.stirrerSpeed.value(), self.stirrerSpeed_3.value()]
        self.operational_time_values = [self.operationalTime.value(), self.operationalTime_3.value()]
        while self.is_running:
            # Run your process
            QApplication.processEvents()  # Allow GUI updates
            for pocket in pockets:
                # Position calibration
                if not self.positionCalibration:
                    cradle.position_calibration()
                    self.positionCalibration = True

                pocket_retrive_x, pocket_retrive_z = pocket.get_position_retrive()
                pocket_leave_x, pocket_leave_z = pocket.get_position_leave()
                cycle_number = pocket.get_cycle_number()
                
                # Retrive arguments for cycle
                stirrer_speed = self.slider_speed_values[cycle_number]
                operational_time = self.operational_time_values[cycle_number]
                
                # Check stop button
                if not self.is_running: break
            
                # Move to RBR position
                self.move_to_pocket(cradle, pocket_retrive_x, pocket_retrive_z) 
                
                # Move RBR to vessel
                vessel_x, vessel_z = vessel.get_position()
                # cradle.move_to_z_coord(0, self.vertical_delay)
                self.move_to_vessel(cradle, vessel_x, vessel_z)
                # Revision: add sensor check
                
                # Fill vessel with reagent
                vessel.fill_reagent(self.vesselVolume)
                
                # Run for some time
                stirrer_command(stirrer, stirrer_speed, "Start")
                sleep(operational_time)
                stirrer_command(stirrer, 0, "Stop")
                
                # Fill vessel with acid
                vessel.fill_acid(self.acidVolume)
            
                # Start and stop stirrer
                stirrer_command(stirrer, stirrer_speed, "Start")
                sleep(operational_time)
                stirrer_command(stirrer, 0, "Stop")
                
                # Empty the vessel
                vessel.empty_tank(self.emptyTime)
                
                # Dry RBR
                stirrer_command(stirrer, 500, "Start")
                vessel.empty_tank(self.dryingTime)
                stirrer_command(stirrer, 0, "Stop")
                sleep(1)
                # Leave RBR
                cradle.move_to_z_coord(0, self.vertical_delay)
                self.move_to_pocket(cradle, pocket_leave_x, pocket_leave_z)
                cradle.move_to_z_coord(0, self.vertical_delay)
            self.is_running = False
                

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
          