from switchButton import SwitchButton
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from time import sleep

switch_pin = 5
switch2_pin = 6
switch3_pin = 19
switchButton1 = SwitchButton(switch_pin)
switchButton2 = SwitchButton(switch2_pin)
switchButton3 = SwitchButton(switch3_pin)

while True:
    print(switchButton1.is_pressed())
    print(switchButton2.is_pressed())
    print(switchButton3.is_pressed())
    sleep(0.1)