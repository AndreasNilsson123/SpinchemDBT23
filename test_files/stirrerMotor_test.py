from stirrer_motor import StirrerMotor
import serial

stirrer = StirrerMotor("/dev/serial0", 9600)

stirrer.send_command("1,WSE,100\r\n")

print("Done!")
stirrer.serial.close()