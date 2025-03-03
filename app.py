import time
import Adafruit_ADS1x15

import RPi.GPIO as GPIO

# GPIO setup
DIR = 20   # Direction GPIO Pin
STEP = 21  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 200  # Steps per Revolution (360 / 1.8)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CW)

# ADC setup
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

# PID constants
Kp = 1.0
Ki = 0.1
Kd = 0.05

# Target pressure
target_pressure = 1000  # Example target pressure value

# PID variables
integral = 0
previous_error = 0

def read_pressure():
    # Read the ADC channel 0 value
    value = adc.read_adc(0, gain=GAIN)
    return value

def pid_control(current_pressure):
    global integral, previous_error
    error = target_pressure - current_pressure
    integral += error
    derivative = error - previous_error
    output = Kp * error + Ki * integral + Kd * derivative
    previous_error = error
    return output

def step_motor(steps, direction):
    GPIO.output(DIR, direction)
    for _ in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        time.sleep(0.01)
        GPIO.output(STEP, GPIO.LOW)
        time.sleep(0.01)

try:
    while True:
        current_pressure = read_pressure()
        control_signal = pid_control(current_pressure)
        
        if control_signal > 0:
            step_motor(int(control_signal), CW)
        else:
            step_motor(int(-control_signal), CCW)
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program stopped")

finally:
    GPIO.cleanup()