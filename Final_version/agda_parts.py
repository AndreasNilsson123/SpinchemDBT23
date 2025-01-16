from hardware import *
from time import sleep, time
import serial
########################
# ------ Cradle ------ #
########################
class Cradle:
    def __init__(self, step_v1, direction_v1, 
                 step_v2, direction_v2,
                 step_h1, direction_h1,
                 sensor_v1, sensor_v2, sensor_h1,
                 vessel_sensor_y, vessel_sensor_x):
        """
        Initializes the instance of the class with the given parameters.

        Parameters:
            step_v1 (int):          The step pin for vertical motor 1.
            direction_v1 (str):     The direction pin for vertical motor 1.
            step_v2 (int):          The step pin for vertical motor 2.
            direction_v2 (str):     The direction pin for vertical motor 2.
            step_h1 (int):          The step pin for horizontal motor 1.
            direction_h1 (str):     The direction pin for horizontal motor 1.
            sensor_v1 (int):        The sensor pin for vertical motor 1.
            sensor_v2 (int):        The sensor pin for vertical motor 2.
            sensor_h1 (int):        The sensor pin for horizontal motor 1.
            vessel_sensor_y (int):  The sensor pin for vessel Y.
            vessel_sensor_x (int):  The sensor pin for vessel X.

        Returns:
            None
        """
        
        self.vertical_motor_1 = StepperMotor(step_v1, direction_v1)
        self.vertical_motor_2 = StepperMotor(step_v2, direction_v2)
        self.horizontal_motor = StepperMotor(step_h1, direction_h1)
        self.vertical1_sensor = SwitchButton(sensor_v1)
        self.vertical2_sensor = SwitchButton(sensor_v2)
        self.horizontal_sensor = SwitchButton(sensor_h1)
        self.vessel_y_sensor = SwitchButton(vessel_sensor_y)
        self.vessel_x_sensor = SwitchButton(vessel_sensor_x)
        
        # Save pin number for stepperMotor2
        self.stepper_motor2_pin = step_v2

        # Set position of cradle
        self.position = Position(0, 0)
        
        # Set default direction for vertical motors
        self.vertical_motor_1.set_direction("clockwise")
        self.vertical_motor_2.set_direction("clockwise")
        self.horizontal_motor.set_direction("clockwise")
        
        # NOTE: 160*z = number of steps to move z mm for vertical steppers
        # NOTE: 5*x = number of steps to move x mm for horizontal steppers
        # 500 / 100.3 = 4.99 approx = 5 steps per mm 
    
    def move_up(self, steps, delay):
        """
        Move the object up by a specified number of steps with a given delay.

        Parameters:
            steps (int): The number of steps to move the object up.
            delay (float): The delay between each step in seconds.

        Returns:
            None
        """
        self.vertical_motor_1.set_direction("clockwise")
        self.vertical_motor_2.set_direction("clockwise")
        self.vertical_motor_1.step(steps, delay, self.stepper_motor2_pin)
        self.update_position(0, -steps)
        
    def move_down(self, steps, delay):
        """
        Move the object down by a certain number of steps at a specified delay.

        Parameters:
            steps (int):    The number of steps to move down.
            delay (float):  The delay between each step.

        Returns:
            None
        """
        self.vertical_motor_1.set_direction("counterclockwise")
        self.vertical_motor_2.set_direction("counterclockwise")
        self.vertical_motor_1.step(steps, delay, self.stepper_motor2_pin)
        self.update_position(0, steps)
        print("Test123")
    
    def move_left(self, steps, delay):
        """
        Move the object to the left by a specified number of steps with a given delay.

        Args:
            steps (int):    The number of steps to move the object.
            delay (float):  The delay in seconds between each step.

        Returns:
            None
        """
        self.horizontal_motor.set_direction("counterclockwise")
        self.horizontal_motor.step(steps, delay)
        self.update_position(steps, 0)
        self.vertical_motor_2.set_direction("clockwise")
    
    def move_right(self, steps, delay):
        """
        Move the object to the right by a given number of steps with a specified delay.

        Parameters:
            steps (int): The number of steps to move the object to the right.
            delay (float): The delay between each step in seconds.

        Returns:
            None
        """
        self.horizontal_motor.set_direction("counterclockwise")
        self.horizontal_motor.step(steps, delay)
        self.update_position(-steps, 0)
    
    def update_position(self, direction_x, direction_z):
        """
        Updates the position of the object based on the given direction values.

        Parameters:
            direction_x (float): The amount to move the object along the x-axis.
            direction_z (float): The amount to move the object along the z-axis.

        Returns:
            None
        """
        x,z = self.position.get_position()
        self.position.set_position(x+direction_x, z+direction_z)
    
    def move_to_x_coord(self, target_x, delay):
        """
        Moves the object to the specified x coordinate.

        Parameters:
            target_x (int): The target x coordinate to move to.
            delay (float): The delay between each step of the movement.

        Returns:
            None
        """
        no_steps = target_x - self.position.get_position_x()
        if(no_steps > 0):
            self.move_left(no_steps, delay)
        else: 
            self.move_right(abs(no_steps), delay)
            
    def move_to_z_coord(self, target_z, delay):
        """
        Moves the object to a specified z-coordinate.

        Parameters:
            target_z (float): The target z-coordinate to move the object to.
            delay (int): The delay in milliseconds between each step of the movement.

        Returns:
            None
        """
        no_steps = target_z - self.position.get_position_z()
        if(no_steps < 0):
            self.move_up(abs(no_steps), delay)
        else: 
            self.move_down(no_steps, delay)
    
    def get_position(self):
        """
        Retrieves the position of the object.

        Returns:
            Position: The position of the object.
        """
        return self.position.get_position()
        
    def position_calibration(self):
        """
        Calibrates the position of the motors.
        
        This function is responsible for calibrating the position of the motors. It sets the direction of the vertical motors to counterclockwise and the direction of the horizontal motor to clockwise. It also sets the position to (0, 0).
        
        Parameters:
        - self: The instance of the class.
        
        Returns:
        - None
        """
        self.vertical_motor_1.set_direction("clockwise")
        self.vertical_motor_2.set_direction("clockwise")
        self.horizontal_motor.set_direction("clockwise")
        self.position.set_position(0, 0)
        # Run vertical motors to top position
        while True:
            if not self.vertical1_sensor.is_pressed():
                self.vertical_motor_1.step(1, 0.00125)
            if not self.vertical2_sensor.is_pressed():
                self.vertical_motor_2.step(1, 0.00125)
            if self.vertical1_sensor.is_pressed() and self.vertical2_sensor.is_pressed():
                break
        
        # Run Horizontal motor to most right position
        while not self.horizontal_sensor.is_pressed():
           self.horizontal_motor.step(1, 0.002)
        
        
########################
# ------ Vessel ------ #
########################
class Vessel:
    def __init__(self, pin_filling_reagent, pin_filling_acid,
                 pin_emptying, pump_filling,
                 pin_liquid_detection,
                 coord_x, coord_y):
        """
        Initializes the object with the given parameters.

        Parameters:
            pin_filling_reagent (int): The pin for filling the reagent.
            pin_filling_acid (int): The pin for filling the acid.
            pin_emptying (int): The pin for emptying.
            pump_filling (int): The pump for filling.
            pin_liquid_detection (int): The pin for liquid detection.
            coord_x (float): The x-coordinate.
            coord_y (float): The y-coordinate.

        Returns:
            None
        """
        self.valve_reagent = Valve(pin_filling_reagent)
        self.valve_acid = Valve(pin_filling_acid)
        self.valve_emptying = Valve(pin_emptying)
        self.pump = Pump(pump_filling)
        self.liquid_detection = LiquidDetection(pin_liquid_detection)
        self.position = Position(coord_x, coord_y)
        self.volume_to_time_reagent = 0.105
        self.volume_to_time_acid = 1.47
        
    def fill_reagent(self, volume):
        """
        Fills the reagent container with the specified volume.

        Parameters:
            volume (float): The volume of reagent to be filled.

        Returns:
            None
        """
        start_time = time()
        filling_time = volume * self.volume_to_time_reagent
        if not self.liquid_detection.is_filled():
            self.valve_reagent.open()
            while(time() - start_time < filling_time) and not self.liquid_detection.is_filled():
                sleep(0.1)    
            self.valve_reagent.close()
        
    
    def fill_acid(self, volume):
        """
        Fills the acid tank with the specified volume.

        Args:
            volume (float): The volume of acid to be filled in the tank.

        Returns:
            None
        """
        filling_time = volume * self.volume_to_time_acid
        self.valve_acid.open()
        self.pump.start()
        sleep(filling_time)
        self.pump.stop()
        self.valve_acid.close()
        
    def empty_tank(self, time):
        """
        Empties the tank for a given amount of time.

        Args:
            time (float): The amount of time to empty the tank in seconds.

        Returns:
            None
        """
        self.valve_emptying.open()
        sleep(time)
        self.valve_emptying.close()
        
    def get_position(self):
        """
        Get the position of the object.

        Returns:
            The position of the object.
        """
        return self.position.get_position()
   
########################
# ------ Stirrer ----- #
########################
class StirrerMotor:
    def __init__(self, port = "/dev/serial0", baudrate=9600):
        """
        Initializes a new instance of the class.

        Args:
            port (str): The port to connect to.
            baudrate (int): The baudrate for the serial connection.

        Returns:
            None
        """
        self.serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,  # 8 data bits
            parity=serial.PARITY_NONE,  # No parity
            stopbits=serial.STOPBITS_ONE  # 1 stop bit
        )
        self.serial.write("1,WSM,1\r\n".encode()) # Activate serial mode
        self.serial.timeout = 5
    
    def is_connection_open(self):
        """
        Check if the connection is open.
        :return: bool - True if the connection is open, False otherwise.
        """
        # Check if the connection is open
        return self.serial.is_open
        
    def send_command(self, command):
        """
        Sends a command to the serial device and returns the response.

        Parameters:
            command (str): The command to send to the serial device.

        Returns:
            str: The response from the serial device.
        """
        self.serial.write(command.encode())


########################
# ------ Pockets ----- #
########################
class rbrPocketDetection():
    def __init__(self, sensor1_pin, sensor2_pin, coord_x, coord_y, cycle_number):
        """
        Initializes the object with the given parameters.

        Parameters:
            sensor1_pin (int): The pin number of the top sensor.
            sensor2_pin (int): The pin number of the bottom sensor.
            coord_x (float): The x-coordinate of the position.
            coord_y (float): The y-coordinate of the position.
            cycle_number (int): The number of cycles.

        Returns:
            None
        """
        self.sensor1 = ForceSensor(sensor1_pin) # Top sensor
        self.sensor2 = ForceSensor(sensor2_pin) # Bottom sensor
        self.position = Position(coord_x, coord_y)
        factor = 6*100 # 6mm
        self.position_leave = Position(coord_x, coord_y+factor)
        self.cycle_number = cycle_number
        
    def detect_rbr(self):
        """
        Detects if the right back sensor detects an object while the left back sensor does not.

        Returns:
            bool: True if the right back sensor detects an object and the left back sensor does not, False otherwise.
        """
        if self.sensor1.object_detected() and not self.sensor2.object_detected():
            return True
        else:
            return False
    
    def get_position_retrive(self):
        """
        Retrieves the position using the `position` object.

        Parameters:
            self: The current instance of the class.

        Returns:
            The position retrieved using the `position` object.
        """
        return self.position.get_position()
    
    def get_position_leave(self):
        """
        Get the position leave.

        Returns:
            The position leave.
        """
        return self.position_leave.get_position()
    
    def get_cycle_number(self):
        """
        Get the value of the cycle number.
        :return: The cycle number.
        """
        return self.cycle_number