#!/usr/bin/env python3

from PWM import PWMController
import time

SERVO_MIN = 150
SERVO_MAX = 600

pwm = PWMController()
pwm.set_frequency(60)

while True:
    pwm.set_pwm(0, 0, SERVO_MIN)
    pwm.set_pwm(1, 0, SERVO_MIN)
    time.sleep(1)
    pwm.set_pwm(0, 0, SERVO_MAX)
    pwm.set_pwm(1, 0, SERVO_MAX)
    time.sleep(1)
