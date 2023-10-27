import serial

class StirrerMotor:
    def __init__(self, port, baudrate):
        self.serial = serial.Serial(port, baudrate)
        self.serial.timeout = 1  # Set timeout to 1 second (adjust as needed)
        
    def send_command(self, command):
        self.serial.write(command.encode())
        response = self.serial.readline().decode().strip()
        return response

