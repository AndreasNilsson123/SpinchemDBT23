import RPi.GPIO as GPIO
import time

#################################
# -------- Force Sensor ------- #
#################################
class ForceSensor:
    def __init__(self, pin):
        """
        Initializes an instance of the class.

        Parameters:
            pin (int): The pin number to be used for GPIO setup.

        Returns:
            None
        """
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)

    def object_detected(self):
        """
        Checks if an object is detected by reading the input from the GPIO pin.

        Returns:
            bool: True if an object is detected, False otherwise.
        """
        return GPIO.input(self.pin)

#################################
# -------- Position ----------- #
#################################
class Position:
    def __init__(self, x=0, z=0):
        """
        Initializes an instance of the class.

        Args:
            x (int): The x-coordinate of the point. Defaults to 0.
            z (int): The z-coordinate of the point. Defaults to 0.
        """
        self.x = x
        self.z = z

    def get_position(self):
        """
        Get the position of the object.

        Returns:
            Tuple: A tuple containing the x and z coordinates of the object.
        """
        return self.x, self.z
    
    def get_position_x(self):
        return self.x
    
    def get_position_z(self):
        return self.z
    
    def set_position(self, x, z):
        """
        Set the position of the object in the x and z coordinates.

        Parameters:
            x (int): The x coordinate of the object's position.
            z (int): The z coordinate of the object's position.
        """
        self.x = x
        self.z = z

#################################
# ---- Liquid Detection ------- #
#################################
class LiquidDetection:
    def __init__(self, pin_sensor):
        self.pin = pin_sensor
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
    def is_filled(self):
        return GPIO.input(self.pin)
    
#################################
# -------- Pump --------------- #
#################################
class Pump:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.stop()
    
    def start(self):
        GPIO.output(self.pin, GPIO.HIGH)
    
    def stop(self):
        GPIO.output(self.pin, GPIO.LOW)
        
#################################
# -------- Switch Button ------ #
#################################        
class SwitchButton:
    def __init__(self, pin):
        """
        Initializes an instance of the class.

        Args:
            pin (int): The pin number to be initialized.

        Returns:
            None
        """
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def is_pressed(self):
        """
        Returns the current state of the button.

        :return: bool - True if the button is pressed, False otherwise.
        """
        return GPIO.input(self.pin)   
    
#################################
# -------- Valve -------------- #
################################# 
class Valve:
    def __init__(self, pin):
        """
        Initializes an instance of the class.
        
        Args:
            pin (int): The pin number to be used for GPIO setup.
        
        Returns:
            None
        """
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.close()

    def open(self):
        """
        Sets the specified GPIO pin to HIGH.

        Parameters:
            self (object): The instance of the class.
        
        Returns:
            None
        """
        GPIO.output(self.pin, GPIO.HIGH)

    def close(self):
        """
        Closes the GPIO pin.

        This function sets the GPIO pin specified during object initialization to a LOW state,
        effectively closing the pin.

        Parameters:
        - self: The object instance.

        Returns:
        - None
        """
        GPIO.output(self.pin, GPIO.LOW)     

#################################
# -------- Stepper ------------ #
################################# 
class StepperMotor:
    def __init__(self, step_pin, direction_pin):
        """
        Initializes a new instance of the class.

        Args:
            step_pin (int): The GPIO pin number for the step signal.
            direction_pin (int): The GPIO pin number for the direction signal.

        Returns:
            None
        """
        self.step_pin = step_pin
        self.direction_pin = direction_pin
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)
        self.set_direction("clockwise")

    def set_direction(self, direction):
        """
        Set the direction of the motor.

        Args:
            direction (str): The direction in which to rotate the motor. Valid values are "clockwise" and "counterclockwise".

        Returns:
            None
        """
        if direction == "clockwise":
            GPIO.output(self.direction_pin, GPIO.HIGH)
        elif direction == "counterclockwise":
            GPIO.output(self.direction_pin, GPIO.LOW)

    def step(self, steps, delay, second_stepper_pin = 0):
        """
        Executes a specified number of steps with a specified delay between each step.

        Parameters:
            steps (int): The number of steps to execute.
            delay (float): The delay in seconds between each step.
            second_stepper_pin (int): The GPIO pin number for the second stepper motor.

        Returns:
            None
        """
        if second_stepper_pin == 0:
            for _ in range(steps):
                GPIO.output(self.step_pin, GPIO.HIGH)
                time.sleep(delay)
                GPIO.output(self.step_pin, GPIO.LOW)
                time.sleep(delay)
        elif not second_stepper_pin == 0:
            for _ in range(steps):
                GPIO.output(self.step_pin, GPIO.HIGH)
                GPIO.output(second_stepper_pin, GPIO.HIGH)
                time.sleep(delay)
                GPIO.output(self.step_pin, GPIO.LOW)
                GPIO.output(second_stepper_pin, GPIO.LOW)
                time.sleep(delay) 
