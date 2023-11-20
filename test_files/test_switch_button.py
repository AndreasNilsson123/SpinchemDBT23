from switchButton import SwitchButton
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from time import sleep

switch_pin = 19
SwitchButton = SwitchButton(switch_pin)

while True:
    print(SwitchButton.is_pressed())
    sleep(0.1)