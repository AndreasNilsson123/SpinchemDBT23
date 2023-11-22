import serial

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
        self.serial.timeout = 5
        
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
        response = self.serial.readline().decode('ascii').strip()

        return response

