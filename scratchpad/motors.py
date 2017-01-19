#!/usr/bin/env python

from Adafruit_MotorHAT import Adafruit_MotorHAT
import atexit
import pygame

from Vector import Vector
from Interpolator import Interpolator

PRECISION = 3

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)
j2 = Vector()

# setup left joystick
j1 = Vector()
left_thruster = Interpolator()
left_thruster.addIndexValue(0.0, -1.0)
left_thruster.addIndexValue(90.0, 1.0)
left_thruster.addIndexValue(180.0, 1.0)
left_thruster.addIndexValue(270.0, -1.0)
left_thruster.addIndexValue(360.0, -1.0)
right_thruster = Interpolator()
right_thruster.addIndexValue(0.0, 1.0)
right_thruster.addIndexValue(90.0, 1.0)
right_thruster.addIndexValue(180.0, -1.0)
right_thruster.addIndexValue(270.0, -1.0)
right_thruster.addIndexValue(360.0, 1.0)


# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)


def setMotor(motor_number, value):
    motor = mh.getMotor(motor_number)

    if value < 0:
        motor.run(Adafruit_MotorHAT.BACKWARD)
        motor.setSpeed(-int(value))
    else:
        motor.run(Adafruit_MotorHAT.FORWARD)
        motor.setSpeed(int(value))


atexit.register(turnOffMotors)

motor1 = mh.getMotor(1)
motor3 = mh.getMotor(3)

pygame.init()
# screen = pygame.display.set_mode([500, 700])
# pygame.display.set_caption("G2X")
clock = pygame.time.Clock()
pygame.joystick.init()
stick = pygame.joystick.Joystick(0)
stick.init()

done = False

while done is False:
    for event in pygame.event.get():
        show_thrusters = False

        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                value = round(event.value, PRECISION)
                if j1.x != value:
                    j1.x = value
                    show_thrusters = True
            elif event.axis == 1:
                value = round(event.value, PRECISION)
                if j1.y != value:
                    j1.y = value
                    show_thrusters = True
            elif event.axis == 2:
                value = round(event.value, PRECISION)
                if j2.x != value:
                    j2.x = value
                    show_thrusters = True
            elif event.axis == 5:
                value = round(event.value, PRECISION)
                if j2.y != value:
                    j2.y = value
                    show_thrusters = True
            else:
                # pass
                print("unknown axis ", event.axis)
        elif event.type == pygame.JOYBUTTONDOWN:
            print("unhandled button down event")
        elif event.type == pygame.JOYBUTTONUP:
            print("unhandled button up event")
        elif event.type == pygame.JOYHATMOTION:
            print("unhandled hat event")
        elif event.type == pygame.JOYBALLMOTION:
            print("unhandled ball motion event")

        if show_thrusters:
            left_value = left_thruster.valueAtIndex(j1.angle)
            right_value = right_thruster.valueAtIndex(j1.angle)
            power = min(1.0, j1.length)
            print("left_thruster = {}, right_thruster = {}, power = {}".format(left_value, right_value, power))
            setMotor(1, left_value * power * 255.0)
            setMotor(3, right_value * power * 255.0)
