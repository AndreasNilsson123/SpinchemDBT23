import RPi.GPIO as GPIO
import threading
from agda_parts import *
from time import sleep
import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

GPIO.setmode(GPIO.BCM)
# ------------------------------------------ #
# ---------------- Setup GUI --------------- #
# ------------------------------------------ #
# Get the directory path where the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------ #
# ----------- Initialize objects ----------- #
# ------------------------------------------ #

def setup_vessel(PIN_reagent, PIN_acid, PIN_emptying, PIN_pump, PIN_liquid,coord_x, coord_y):
    """
    Initializes and returns a Vessel object.

    Args:
        PIN_reagent (int): The PIN of the reagent valve.
        PIN_acid (int): The PIN of the acid valve.
        PIN_emptying (int): The PIN of the emptying valve.
        PIN_pump (int): The PIN of the pump.
        PIN_liquid (int): The PIN of the liquid sensor.
        coord_x (float): The x-coordinate of the vessel.
        coord_y (float): The y-coordinate of the vessel.

    Returns:
        Vessel: The initialized Vessel object.
    """
    vessel = Vessel(PIN_reagent, PIN_acid, PIN_emptying, PIN_pump, PIN_liquid, coord_x, coord_y)
    return vessel

def setup_sensors(PIN1,PIN2,PIN3,PIN4, coord_x1, coord_y1, coord_x2, coord_y2):
    """
    Sets up the sensors for pocket detection.

    Parameters:
        PIN1 (int): The pin number for the first sensor.
        PIN2 (int): The pin number for the second sensor.
        PIN3 (int): The pin number for the third sensor.
        PIN4 (int): The pin number for the fourth sensor.
        coord_x1 (int): The x-coordinate for the first sensor.
        coord_y1 (int): The y-coordinate for the first sensor.
        coord_x2 (int): The x-coordinate for the second sensor.
        coord_y2 (int): The y-coordinate for the second sensor.

    Returns:
        tuple: A tuple containing the pocket detection results for the first and second sensors.
    """
    pocket1_detection = rbrPocketDetection(PIN1, PIN2, coord_x=coord_x1, coord_y=coord_y1, cycle_number=0)
    pocket2_detection = rbrPocketDetection(PIN3, PIN4, coord_x=coord_x2, coord_y=coord_y2, cycle_number=1)
    return pocket1_detection, pocket2_detection

def setup_cradle(V1_step, V1_dir,
                 V2_step, V2_dir,
                 H_step, H_dir,
                 sensor_v1, sensor_v2, 
                 sensor_h1,
                 vessel_sensor_y, vessel_sensor_x):
    """
	Creates a new cradle setup with the given parameters.
	Parameters:
	- V1_step (int): The step value for the V1 motor.
	- V1_dir (str): The direction for the V1 motor.
	- V2_step (int): The step value for the V2 motor.
	- V2_dir (str): The direction for the V2 motor.
	- H_step (int): The step value for the H motor.
	- H_dir (str): The direction for the H motor.
	- sensor_v1 (int): The sensor value for V1.
	- sensor_v2 (int): The sensor value for V2.
	- sensor_h1 (int): The sensor value for H1.
	- vessel_sensor_y (int): The vessel sensor value for Y.
	- vessel_sensor_x (int): The vessel sensor value for X.
	Returns:
	- cradle (Cradle): A new Cradle object with the given parameters.
	"""
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
        """
        Initializes an instance of the Automation class.

        This function sets up the necessary parameters and variables for the automation process.
        It initializes the position calibration, vertical and horizontal delays, and the current pocket.
        It also sets the position of objects such as the vessel and pockets.
        Additionally, it initializes other variables including vessel volume, acid volume, 
        empty time, drying time, is_running flag, and rest time.

        The function also initiates sliders and connects them to their corresponding signal handlers.
        Furthermore, it sets up the cradle, vessel, sensors, and stirrer for the automation process.

        Parameters:
        None

        Returns:
        None
        """
        super(Automation, self).__init__()
        loadUi(os.path.join(script_directory, "GUI_automation.ui"), self)
        # Define neccessary parameters
        self.positionCalibration = False
        self.vertical_delay_up = 0.002
        self.vertical_delay_down = 0.001
        self.horizontal_delay = 0.002
        self.current_pocket = 0
        
        # Position of objects
        vessel_x = 5*295
        vessel_y = 123*100
        pocket1_x = int(3.4*5)
        pocket1_y = int(131*100)
        pocket2_x = int(112.4*5)
        pocket2_y = int(131*100)
        
        # Other variables
        self.vesselVolume = 650
        self.acidVolume = 5
        self.emptyTime = 15
        self.dryingTime = 10
        self.is_running = False
        self.rest_time = 10
        
        
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
        cradle = setup_cradle(V1_step=17, V1_dir=27, V2_step=23, V2_dir=22,
                                    H_step=24, H_dir=25, sensor_v1=26, sensor_v2=21,
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
        """
        Set the value of the text box to the string representation of the given integer value.

        :param var: The text box widget that will display the value.
        :type var: QLineEdit

        :param value: The new value to be displayed in the text box.
        :type value: int
        """
        # Convert the integer value to a string and set it in the text box
        var.setText(str(value))    

    def start_process(self,cradle, vessel, pockets, stirrer):
        """
        Starts the process with the given parameters.

        Args:
            cradle (Cradle): The cradle object.
            vessel (Vessel): The vessel object.
            pockets (int): The number of pockets.
            stirrer (Stirrer): The stirrer object.

        Returns:
            None
        """
        if not self.is_running:
            # Update UI
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(True)

            # Start process in a separate thread
            self.thread = threading.Thread(target = lambda:self.process_thread(cradle, vessel, pockets, stirrer))
            self.is_running = True
            self.thread.start()

    def stop_process(self):
        """
        Stops the process if it is currently running.

        This function checks if the process is running and if so, stops it. It sets the `is_running` flag to False, which indicates that the process should stop. The function then waits for the thread to finish using the `join()` method. After the thread has finished, the function updates the UI by enabling the start button and disabling the stop button. Additionally, it sets the `positionCalibration` flag to False.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """
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
        """
        Move the cradle to the specified X and Z coordinates.

        Parameters:
            cradle (Cradle): The Cradle object used to control the movements.
            pos_x (float): The X coordinate to move the cradle to.
            pos_z (float): The Z coordinate to move the cradle to.

        Returns:
            None
        """
        cradle.move_to_x_coord(pos_x, self.horizontal_delay)
        cradle.move_to_z_coord(pos_z, self.vertical_delay_down)
        cradle.move_to_z_coord(0, self.vertical_delay_up)
    
    def move_to_vessel(self, cradle, pos_x, pos_z):
        """
        Move the cradle to the specified position in the vessel.

        Args:
            cradle (Cradle): The cradle object used to move the cradle.
            pos_x (float): The x-coordinate of the position to move to.
            pos_z (float): The z-coordinate of the position to move to.

        Returns:
            None
        """
        cradle.move_to_x_coord(pos_x, self.horizontal_delay)
        # Revision: add sensor check
        cradle.move_to_z_coord(pos_z, self.vertical_delay_down)

    def process_thread(self, cradle, vessel, pockets, stirrer):
        """
        Process a thread by performing a series of actions on a cradle, vessel, pockets, and stirrer.
        
        Parameters:
            cradle (Cradle): The cradle object to be used.
            vessel (Vessel): The vessel object to be used.
            pockets (list[Pocket]): A list of pockets to iterate through.
            stirrer (Stirrer): The stirrer object to be used.
        
        Returns:
            None
        """
        def retrieve_slider_speed(cycle_number):
            return self.stirrerSpeed.value() if cycle_number == 0 else self.stirrerSpeed_3.value()
        
        def retrieve_operational_time(cycle_number):
            return self.operationalTime.value() if cycle_number == 0 else self.operationalTime_3.value()
        
        def move_to_pocket_retrieve(pocket):
            pocket_retrieve_x, pocket_retrieve_z = pocket.get_position_retrive()
            self.move_to_pocket(cradle, pocket_retrieve_x, pocket_retrieve_z)
        
        def move_to_vessel_position():
            vessel_x, vessel_z = vessel.get_position()
            self.move_to_vessel(cradle, vessel_x, vessel_z)
        
        def fill_vessel_with_reagent():
            vessel.fill_reagent(self.vesselVolume)
        
        def fill_vessel_with_acid():
            vessel.fill_acid(self.acidVolume)
        
        def empty_vessel():
            vessel.empty_tank(self.emptyTime)
        
        def dry_rbr():
            stirrer_command(stirrer, 500, "Start")
            vessel.empty_tank(self.dryingTime)
            stirrer_command(stirrer, 0, "Stop")
            sleep(1)
        
        def move_to_pocket_leave(pocket):
            pocket_leave_x, pocket_leave_z = pocket.get_position_leave()
            self.move_to_pocket(cradle, pocket_leave_x, pocket_leave_z)
        
        self.slider_speed_values = [retrieve_slider_speed(cycle_number) for cycle_number in range(2)]
        self.operational_time_values = [retrieve_operational_time(cycle_number) for cycle_number in range(2)]
        
        while self.is_running:
            QApplication.processEvents()
            
            for pocket in pockets:
                if not self.positionCalibration:
                    cradle.position_calibration()
                    self.positionCalibration = True
                    sleep(1)
                
                cycle_number = pocket.get_cycle_number()
                stirrer_speed = self.slider_speed_values[cycle_number]
                operational_time = self.operational_time_values[cycle_number]
                
                move_to_pocket_retrieve(pocket)
                move_to_vessel_position()
                fill_vessel_with_reagent()     
                
                stirrer_command(stirrer, stirrer_speed, "Start")
                sleep(self.rest_time)
                fill_vessel_with_acid()
                sleep(operational_time)
                stirrer_command(stirrer, 0, "Stop")
                
                empty_vessel()
                
                dry_rbr()
                cradle.move_to_z_coord(0, self.vertical_delay_up)
                move_to_pocket_leave(pocket)
                cradle.move_to_z_coord(0, self.vertical_delay_up)
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
          