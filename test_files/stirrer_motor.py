import serial

class StirrerMotor:
    def __init__(self, port, baudrate):
        """
        Initializes a new instance of the class.

        Args:
            port (str): The port to connect to.
            baudrate (int): The baudrate for the serial connection.

        Returns:
            None
        """
        self.serial = serial.Serial(port, baudrate)
        
        self.serial.write("1,WSM,1\r\n".encode()) # Activate serial mode
        
        self.serial.timeout = 1  # Set timeout to 1 second (adjust as needed)
        
    def send_command(self, command):
        """
        Sends a command to the serial device and returns the response.

        Parameters:
            command (str): The command to send to the serial device.

        Returns:
            str: The response from the serial device.
        """
        self.serial.write(command.encode())
        
        # Read the response from the serial device
        response = self.serial.readline().decode().strip()

        return response

