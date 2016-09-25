#!/usr/bin/env python3

import Adafruit_PCA9685
import time

pwm = Adafruit_PCA9685.PCA9685()
servo_min = 150
servo_max = 600

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

print('Moving servo on channel 0, press Ctrl-C to quit...')
while True:
    # Move servo on channel O between extremes.
    pwm.set_pwm(0, 0, servo_min)
    pwm.set_pwm(1, 0, servo_min)
    time.sleep(1)
    pwm.set_pwm(0, 0, servo_max)
    pwm.set_pwm(1, 0, servo_max)
    time.sleep(1)
