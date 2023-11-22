from stepper_controller import StepperMotor
from switchButton import SwitchButton
from position import Position

class Cradle:
    def __init__(self, step_v1, direction_v1, 
                 step_v2, direction_v2,
                 step_h1, direction_h1,
                 sensor_v1, sensor_v2, sensor_h1,
                 vessel_sensor_y, vessel_sensor_x):
        """
        Initializes the instance of the class with the given parameters.

        Parameters:
            step_v1 (int): The step pin for vertical motor 1.
            direction_v1 (str): The direction pin for vertical motor 1.
            step_v2 (int): The step pin for vertical motor 2.
            direction_v2 (str): The direction pin for vertical motor 2.
            step_h1 (int): The step pin for horizontal motor 1.
            direction_h1 (str): The direction pin for horizontal motor 1.
            sensor_v1 (int): The sensor pin for vertical motor 1.
            sensor_v2 (int): The sensor pin for vertical motor 2.
            sensor_h1 (int): The sensor pin for horizontal motor 1.
            vessel_sensor_y (int): The sensor pin for vessel Y.
            vessel_sensor_x (int): The sensor pin for vessel X.

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
        self.vertical_motor_1.set_direction("counterclockwise")
        self.vertical_motor_2.set_direction("counterclockwise")
        self.vertical_motor_1.step(steps, delay, self.stepper_motor2_pin)
        self.update_position(0, -steps)
        
    def move_down(self, steps, delay):
        """
        Move the object down by a certain number of steps at a specified delay.

        Parameters:
            steps (int): The number of steps to move down.
            delay (float): The delay between each step.

        Returns:
            None
        """
        self.vertical_motor_1.set_direction("clockwise")
        self.vertical_motor_2.set_direction("clockwise")
        self.vertical_motor_1.step(steps, delay, self.stepper_motor2_pin)
        self.update_position(0, steps)
    
    def move_left(self, steps, delay):
        """
        Move the object to the left by a specified number of steps with a given delay.

        Args:
            steps (int): The number of steps to move the object.
            delay (float): The delay in seconds between each step.

        Returns:
            None
        """
        self.horizontal_motor.set_direction("clockwise")
        self.horizontal_motor.step(steps, delay)
        self.update_position(steps, 0)
    
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
        no_steps = target_z - self.position.get_position_z()
        if(no_steps < 0):
            self.move_up(abs(no_steps), delay)
        else: 
            self.move_down(no_steps, delay)
    
    def get_position(self):
        return self.position.get_position()
        
    def position_calibration(self):
        self.vertical_motor_1.set_direction("counterclockwise")
        self.vertical_motor_2.set_direction("counterclockwise")
        self.horizontal_motor.set_direction("counterclockwise")
        
        # Run vertical motors to top position
        while True:
            if not self.vertical1_sensor.is_pressed():
                self.vertical_motor_1.step(1, 0.0004)
            if not self.vertical2_sensor.is_pressed():
                self.vertical_motor_2.step(1, 0.0004)
            if self.vertical1_sensor.is_pressed() and self.vertical2_sensor.is_pressed():
                break
        
        # Run Horizontal motor to most right position
        while not self.horizontal_sensor.is_pressed():
           self.horizontal_motor.step(1, 0.002)
        
        
