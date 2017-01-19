#!/usr/bin/env python

from Adafruit_MotorHAT import Adafruit_MotorHAT
import atexit
import pygame

from Vector import Vector

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)
j1 = Vector()
j2 = Vector()


# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)


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
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                value = round(event.value, 2)
                if j1.x != value:
                    j1.x = value
                    print("j1 = {}".format(j1))
            elif event.axis == 1:
                value = round(event.value, 2)
                if j1.y != value:
                    j1.y = value
                    print("j1 = {}".format(j1))
            elif event.axis == 2:
                value = round(event.value, 2)
                if j2.x != value:
                    j2.x = value
                    print("j2 = {}".format(j2))
            elif event.axis == 5:
                value = round(event.value, 2)
                if j2.y != value:
                    j2.y = value
                    print("j2 = {}".format(j2))
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
