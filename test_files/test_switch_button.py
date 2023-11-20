from switchButton import SwitchButton
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from time import sleep

switch_pin = 5
#switch_pin = 26
#switch_pin = 19
switchButton = SwitchButton(switch_pin)
#switchButton2 = SwitchButton(switch2_pin)
#switchButton3 = SwitchButton(switch3_pin)

while True:
    print(switchButton.is_pressed())
#    print(switchButton.is_pressed())
#    print(switchButton.is_pressed())
    sleep(0.1)