#!/usr/bin/env python3

import socket
import atexit
import pygame


PRECISION = 3

# get local machine name                          
host = "192.168.0.1"
port = 9999

# create a socket object and connect to specified host/port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((host, port))


def close_socket():
    s.close()


def send_message(message):
    s.send(message.encode())
    response = s.recv(1024)                                     
    print(response.decode('ascii'))


atexit.register(close_socket)

pygame.init()
pygame.joystick.init()
stick = pygame.joystick.Joystick(0)
stick.init()

done = False

while done is False:
    for event in pygame.event.get():
        message = None

        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                value = round(event.value, PRECISION)
                message = "j1.x={0}".format(value)
            elif event.axis == 1:
                value = round(event.value, PRECISION)
                message = "j1.y={0}".format(value)
            elif event.axis == 2:
                value = round(event.value, PRECISION)
                message = "j2.x={0}".format(value)
            elif event.axis == 5:
                value = round(event.value, PRECISION)
                message = "j2.y={0}".format(value)
            elif event.axis == 3:
                value = round(event.value, PRECISION)
                message = "desent={0}".format(value)
            elif event.axis == 4:
                value = round(event.value, PRECISION)
                message = "ascent={0}".format(value)
            else:
                print("unknown axis ", event.axis)

        if message is not None:
            send_message(message)
