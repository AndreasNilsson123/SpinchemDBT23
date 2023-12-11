import RPi.GPIO as GPIO
from time import sleep
from switchButton import SwitchButton


# Declare pins
LEFT_VERTICAL = 21
RIGHT_VERTICAL = 10

button_left = SwitchButton(LEFT_VERTICAL)
button_right = SwitchButton(RIGHT_VERTICAL)

while True:
    print(button_left.is_pressed())
    print(button_right.is_pressed())
    sleep(0.5)
    
