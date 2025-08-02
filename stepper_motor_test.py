# Success! We used pints 24, 18, 4 to control A3A3B3B4
# Reading through
# https://www.waveshare.com/wiki/Stepper_Motor_HAT#Download_Sample_Demo
# Watched Dan Marcoux video https://www.youtube.com/watch?v=0WQNXruPaqg

from time import sleep
import sys
from RpiMotorLib import RpiMotorLib

import RPi.GPIO as GPIO

# GPIO setup
DIR = 24   # Direction GPIO Pin
STEP = 18  # Step GPIO Pin
ENABLE = 4  # Step GPIO Pin

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(ENABLE, GPIO.OUT)
GPIO.output(ENABLE, 1)

# Create stepper motor object
# Arguments: direction_pin, step_pin, step_type, motor_type
motor = RpiMotorLib.A4988Nema(DIR, STEP, (21, 22, 27), "A4988")

print('MAIN (1s period) with enable')

try:
    while True:
        print('Direction: CW')
        sleep(1)
        # motor_go(clockwise, steptype, steps, stepdelay, verbose, initdelay)
        motor.motor_go(False, "Full", 2000, 0.001, False, 0.05)
        
        print('Direction: CCW')
        sleep(1)
        motor.motor_go(True, "Full", 2000, 0.001, False, 0.05)

except KeyboardInterrupt:
    print("Stopping motor...")
    # RpiMotorLib handles cleanup automatically
