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


            
# ------------------------------------------ #
# --------------- Automation --------------- #
# ------------------------------------------ #
class Automation(QMainWindow):
    def __init__(self):
        super(Automation, self).__init__()
        loadUi(os.path.join(script_directory, "GUI_prototype.ui"), self)
        # Define neccessary parameters
        self.positionCalibration = False
        self.vertical_delay = 0.001
        self.horizontal_delay = 0.001
        
        # Setup pins
        cradle = setup_cradle(V1_step=17, V1_dir=27, V2_step=22, V2_dir=23,
                                    H_step=24, H_dir=25, sensor_v1=26, sensor_v2=21,
                                    sensor_h1=13, vessel_sensor_y=19, vessel_sensor_x=20)
        vessel = setup_vessel(PIN1=18, PIN2=16, coord_x=268*5, coord_y=127*160)
        
        pocket1, pocket2 = setup_sensors(8,9,10,11, 127*5, 132*160, 0*5, 0*160)
        
        stirrer = setup_stirrer('/dev/serial0', 9600)
        # Step 1
        self.pickUp.clicked.connect(lambda: self.pickUpNewRBR(cradle, pocket1))
        # Step 2
        self.rbrToVessel.clicked.connect(lambda: self.moveRBRToVessel(cradle, vessel))
        # Step 3
        self.fillVessel.clicked.connect(lambda: self.fillTheVessel(vessel))
        # Step 4
        self.startMotor.clicked.connect(lambda: self.startStirrerMotor(stirrer))
        # Step 5
        self.stopMotor.clicked.connect(lambda: self.stopStirrerMotor(stirrer))
        # Step 6
        self.emptyVessel.clicked.connect(lambda: self.emptyTheVessel(vessel))
        # Step 7
        self.liftRbr.clicked.connect(lambda: self.liftRBRFromVessel(cradle))
        # Step 8
        self.leaveRbr.clicked.connect(lambda: self.leaveRBRInPocket(cradle, pocket1))
        
        # Set the initial value of the QLineEdit to the lowest value of the slider
        initial_value = self.stirrerSpeed.minimum()
        self.dispStirrerSpeed.setText(str(initial_value))
        
        # Connect the slider valueChanged signal to the text box setText slot
        self.stirrerSpeed.valueChanged.connect(self.on_slider_value_changed)
        
        # Initial state
        self.set_initial_button_color(self.pickUp, QColor(Qt.green))
        self.set_initial_button_color(self.leaveRbr, QColor(Qt.red))
        self.set_initial_button_color(self.rbrToVessel, QColor(Qt.red))
        self.set_initial_button_color(self.fillVessel, QColor(Qt.red))
        self.set_initial_button_color(self.startMotor, QColor(Qt.red))
        self.set_initial_button_color(self.stopMotor, QColor(Qt.red))
        self.set_initial_button_color(self.emptyVessel, QColor(Qt.red))
        self.set_initial_button_color(self.liftRbr, QColor(Qt.red))
    
    def toggle_button_color(self, button):
        # Toggle between green and red
        if button.styleSheet() == "background-color: #00ff00;":
            self.set_initial_button_color(button, QColor(Qt.red))
        else:
            self.set_initial_button_color(button, QColor(Qt.green))

    def set_initial_button_color(self, button, color):
        # Set the background color of the button
        button.setStyleSheet(f"background-color: {color.name()};")

        # Disable the button if the color is red
        button.setEnabled(color != QColor(Qt.red))

    def on_slider_value_changed(self, value):
        # Convert the integer value to a string and set it in the text box
        self.dispStirrerSpeed.setText(str(value))        
    
    # 1. Button for RBR pick-up
    def pickUpNewRBR(self, cradle, pocket1):
        # Run calibration
        if not self.positionCalibration:
            cradle.position_calibration()
            self.positionCalibration = True
            sleep(1.5)
        # 1.1 Locate new RBR using sensors
        # 1.2 Move cradle to horizontal position of RBR
        # 1.3 Move cradle to vertical position of RBR
        # 1.4 Move cradle back to top vertical position
        pos_x, pos_z = pocket1.get_position_retrive()
        cradle.move_to_x_coord(pos_x, self.horizontal_delay)
        cradle.move_to_z_coord(pos_z, self.vertical_delay)
        sleep(1)
        cradle.move_to_z_coord(0, self.vertical_delay)
        # Change color of buttons
        self.toggle_button_color(self.rbrToVessel)
        self.toggle_button_color(self.pickUp)

# 2. Button for moving RBR to vessel
# 2.1 Move cradle to horizontal position of vessel
# 2.2 Move cradle to vertical position of vessel
    def moveRBRToVessel(self, cradle, vessel):
        pos_x, pos_z = vessel.get_position()
        # Move to horizontal position of vessel
        cradle.move_to_x_coord(pos_x, self.horizontal_delay)
        # Lower RBR intor vessel
        cradle.move_to_z_coord(pos_z, self.vertical_delay)

        
        self.toggle_button_color(self.fillVessel)
        self.toggle_button_color(self.liftRbr)
        self.toggle_button_color(self.startMotor)
        self.toggle_button_color(self.stopMotor)
        self.toggle_button_color(self.rbrToVessel)

# 3. Fill the vessel with reagnet
# 3.1 Open valve for filling vessel
# 3.2 Keep the valve opend for a certain amount of time
# 3.3 Close valve for filling vessel
# 3.4 CONDITIONS: Vessel is empty from liquid
    def fillTheVessel(self, vessel):
        vessel.open_filling()
        sleep(40)
        vessel.close_filling()
        
        self.toggle_button_color(self.fillVessel)
        self.toggle_button_color(self.emptyVessel)
        self.toggle_button_color(self.liftRbr)
# 4. Start stirrer motor
# 4.1 Start stirrer motor with defined speed
# 4.2 CONDITIONS: Motor must be in vessel
    def startStirrerMotor(self, stirrer):
        stirrer_command(stirrer,self.stirrerSpeed.value(), "Start")
# 5. Stop stirrer motor
# 5.1 Stop stirrer motor
    def stopStirrerMotor(self, stirrer):
        stirrer_command(stirrer,0, "Stop")
        
# 6. Empty vessel from reagent
# 6.1 Open valve for emptying vessel
# 6.2 Keep the valve opend for a certain amount of time
# 6.3 Close valve for emptying vessel
    def emptyTheVessel(self, vessel):
        vessel.open_emptying()
        sleep(60)
        vessel.close_emptying()
        self.toggle_button_color(self.emptyVessel)
        self.toggle_button_color(self.liftRbr)
# 7. Lift RBR from vessel
# 7.1 Lift cradle to top vertical position
    def liftRBRFromVessel(self, cradle):
        cradle.move_to_z_coord(0, self.vertical_delay)
        
        self.set_initial_button_color(self.pickUp, QColor(Qt.red))
        self.set_initial_button_color(self.leaveRbr, QColor(Qt.green))
        self.set_initial_button_color(self.rbrToVessel, QColor(Qt.red))
        self.set_initial_button_color(self.fillVessel, QColor(Qt.red))
        self.set_initial_button_color(self.startMotor, QColor(Qt.red))
        self.set_initial_button_color(self.stopMotor, QColor(Qt.red))
        self.set_initial_button_color(self.emptyVessel, QColor(Qt.red))
        self.set_initial_button_color(self.liftRbr, QColor(Qt.red))
# 8. Leave RBR into container
# 8.1 Move RBR into horizontal position of desired container
# 8.2 Move RBR into vertical position of desired container
# 8.3 Move RBR back to top vertical position
# 8.4 CONDITIONS: Container must be empty
    def leaveRBRInPocket(self, cradle, pocket1):
        pos_x, pos_z = pocket1.get_position_leave()
        cradle.move_to_x_coord(pos_x, self.horizontal_delay)
        cradle.move_to_z_coord(pos_z, self.vertical_delay)
        sleep(1)
        cradle.move_to_z_coord(0, self.vertical_delay)
        self.toggle_button_color(self.pickUp)
        self.toggle_button_color(self.leaveRbr)
      
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
