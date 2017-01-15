#!/usr/bin/env python

from Adafruit_MotorHAT import Adafruit_MotorHAT
import atexit
import pygame

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)


# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)


atexit.register(turnOffMotors)

motor1 = mh.getMotor(1)
motor3 = mh.getMotor(3)

# set the speed to start, from 0 (off) to 255 (max speed)
# myMotor.setSpeed(150)
# myMotor.run(Adafruit_MotorHAT.FORWARD)
# turn on motor
# myMotor.run(Adafruit_MotorHAT.RELEASE)

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
                value = round(event.value, 2) * 255
                if value < 0:
                    motor1.run(Adafruit_MotorHAT.BACKWARD)
                    motor1.setSpeed(-int(value))
                    motor3.run(Adafruit_MotorHAT.BACKWARD)
                    motor3.setSpeed(-int(value))
                else:
                    motor1.run(Adafruit_MotorHAT.FORWARD)
                    motor1.setSpeed(int(value))
                    motor3.run(Adafruit_MotorHAT.FORWARD)
                    motor3.setSpeed(int(value))
            elif event.axis == 1:
                # print("axis 1 = ", round(event.value, 2))
                pass
            else:
                pass
                # print("unknown axis ", event.axis)
        elif event.type == pygame.JOYBUTTONDOWN:
            print("unhandled button down event")
        elif event.type == pygame.JOYBUTTONUP:
            print("unhandled button up event")
        elif event.type == pygame.JOYHATMOTION:
            print("unhandled hat event")
        elif event.type == pygame.JOYBALLMOTION:
            print("unhandled ball motion event")
        # clock.tick(20)


    # print("Forward! ")
    # myMotor.run(Adafruit_MotorHAT.FORWARD)

    # print("\tSpeed up...")
    # for i in range(255):
    #     myMotor.setSpeed(i)
    #     time.sleep(0.01)

    # print("\tSlow down...")
    # for i in reversed(range(255)):
    #     myMotor.setSpeed(i)
    #     time.sleep(0.01)

    # print("Backward! ")
    # myMotor.run(Adafruit_MotorHAT.BACKWARD)

    # print("\tSpeed up...")
    # for i in range(255):
    #     myMotor.setSpeed(i)
    #     time.sleep(0.01)

    # print("\tSlow down...")
    # for i in reversed(range(255)):
    #     myMotor.setSpeed(i)
    #     time.sleep(0.01)

    # print("Release")
    # myMotor.run(Adafruit_MotorHAT.RELEASE)
    # time.sleep(1.0)
