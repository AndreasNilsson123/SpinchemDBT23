import serial
import time

# Define the serial port and baud rate
ser = serial.Serial('COM5', 9600)  # Adjust the port and baud rate as needed
print("Successfully opened serial port!")
# Wait for a moment to ensure the connection is established
time.sleep(2)

print("Testing the stirrer...")
# Command 1: Disable front panel control and enable RS232 control
ser.write(b'1,WSM,1\r\n')  # Make sure to encode the string as bytes and terminate with '\r\n'

# Read the response from the stirrer (if any)
response = ser.readline()
print(response)

# Command 2: Set motor speed to 500 rpm
ser.write(b'1,WMS,500\r\n')  # Make sure to encode the string as bytes and terminate with '\r\n'

# Read the response from the stirrer (if any)
response = ser.readline()
print(response)

# Close the serial connection
ser.close()
