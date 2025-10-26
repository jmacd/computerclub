#!/usr/bin/env python3

import time
import RPi.GPIO as GPIO

# Define GPIO pins for the DRV8825 controller
DIR_PIN = 20    # Direction GPIO Pin
STEP_PIN = 21   # Step GPIO Pin
ENABLE_PIN = 16 # Enable GPIO Pin (optional)
MODE_PINS = [14, 15, 18]  # Mode pins for step resolution (optional)

# Define the steps per revolution for your specific motor
STEPS_PER_REVOLUTION = 200  # Common for many stepper motors, adjust for your specific motor

# Define the delay between steps (seconds)
STEP_DELAY = 0.01  # Adjust for desired speed

# Microstep resolution
RESOLUTION = {
    'FULL': (0, 0, 0),
    'HALF': (1, 0, 0),
    '1/4': (0, 1, 0),
    '1/8': (1, 1, 0),
    '1/16': (0, 0, 1),
    '1/32': (1, 0, 1)
}

def setup():
    """
    Initialize GPIO pins for the DRV8825 controller
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR_PIN, GPIO.OUT)
    GPIO.setup(STEP_PIN, GPIO.OUT)
    
    # Optional - set up enable pin
    GPIO.setup(ENABLE_PIN, GPIO.OUT)
    GPIO.output(ENABLE_PIN, GPIO.LOW)  # Enable driver (active low)
    
    # Optional - set up mode pins for microstep resolution
    for pin in MODE_PINS:
        GPIO.setup(pin, GPIO.OUT)

def set_step_mode(mode):
    """
    Set the stepping mode (microstep resolution)
    
    Parameters:
    - mode: One of 'FULL', 'HALF', '1/4', '1/8', '1/16', '1/32'
    """
    if mode not in RESOLUTION:
        print(f"Warning: Mode {mode} not recognized. Using FULL step mode.")
        mode = 'FULL'
    
    print(f"Setting step mode to {mode}")
    for i, pin in enumerate(MODE_PINS):
        GPIO.output(pin, RESOLUTION[mode][i])

def spin_motor(direction, steps, step_mode='1/16'):
    """
    Spin the motor in the specified direction for the given number of steps.
    
    Parameters:
    - direction: True for clockwise, False for counterclockwise
    - steps: Number of steps to rotate
    - step_mode: Resolution mode ('FULL', 'HALF', '1/4', '1/8', '1/16', '1/32')
    """
    direction_text = "clockwise" if direction else "counterclockwise"
    print(f"Spinning {direction_text} for {steps} steps in {step_mode} mode")
    
    # Set the direction
    GPIO.output(DIR_PIN, GPIO.HIGH if direction else GPIO.LOW)
    
    # Set the step mode
    set_step_mode(step_mode)
    
    # Send pulses to the STEP pin
    for _ in range(steps):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(STEP_DELAY/2)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(STEP_DELAY/2)

try:
    # Setup GPIO pins
    setup()
    
    print("Starting motor control demonstration")
    
    # Spin motor clockwise for one revolution
    print("Spinning clockwise for one revolution...")
    spin_motor(True, STEPS_PER_REVOLUTION, '1/16')
    
    # Pause
    time.sleep(1)
    
    # Spin motor counterclockwise for one revolution
    print("Spinning counterclockwise one revolution...")
    spin_motor(False, STEPS_PER_REVOLUTION, '1/16')
    
    # Demonstrate different step modes
    print("\nDemonstrating different step modes")
    
    step_modes = ['FULL', 'HALF', '1/4', '1/8', '1/16']
    
    for mode in step_modes:
        print(f"\nUsing {mode} step mode")
        spin_motor(True, 50, mode)
        time.sleep(0.5)
    
    print("Motor demonstration complete!")

finally:
    # Cleanup GPIO to prevent issues on next run
    GPIO.output(ENABLE_PIN, GPIO.HIGH)  # Disable driver
    GPIO.cleanup()
    print("GPIO pins cleaned up")