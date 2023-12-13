#import RPi.GPIO as GPIO
import threading
from time import sleep
import sys
import os
from PyQt5.uic import loadUiType
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

# ------------------------------------------ #
# ---------------- Setup GUI --------------- #
# ------------------------------------------ #
# Get the directory path where the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

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
        pocket1_x = int(128.4*5)
        pocket1_y = int(131*160)
        pocket2_x = int(28.6*5)
        pocket2_y = int(131*160)
        
        # Other variables
        self.vesselVolume = 400
        self.acidVolume = 50
        self.emptyTime = 15
        self.dryingTime = 5
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
        
        # Create list of slider values
        self.slider_speed_values = [self.stirrerSpeed.value(), self.stirrerSpeed_3.value()]
        self.operational_time_values = [self.operationalTime.value(), self.operationalTime_3.value()]
        
        cradle = False; vessel = False; pockets = False; stirrer = False
        
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

    def process_thread(self, cradle, vessel, pockets, stirrer):
        # Your process code goes here
        while self.is_running:
            # Run your process
            for i in range(0, 2):
                QApplication.processEvents()  # Allow GUI updates
                print("Hello1")
                sleep(5)
                if not self.is_running:
                    break
                print("Hello2")
                sleep(5)
                if not self.is_running:
                    break
                print("Hello3")
                sleep(5)
                if not self.is_running:
                    break
                print("Hello4")
                sleep(5)
                if not self.is_running:
                    break

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
        
          