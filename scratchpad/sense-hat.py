#!/usr/bin/env python3

from sense_hat import SenseHat
import time

sense = SenseHat()
sense.clear()

while True:
    t = sense.get_temperature()
    p = sense.get_pressure()
    h = sense.get_humidity()
    orientation = sense.get_orientation()
    pitch = orientation['pitch']
    roll = orientation['roll']
    yaw = orientation['yaw']
    acceleration = sense.get_accelerometer_raw()
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']

    print("Temperature = {0}, Pressure = {1}, Humidity = {2}".format(t, p, h))
    print("pitch={0}, yaw={1}, roll={2}".format(pitch, yaw, roll))
    print("x={0}, y={1}, z={2}".format(x, y, z))
    print()

    time.sleep(1)
