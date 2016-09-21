#!/usr/bin/env python3

from sense_hat import SenseHat
import sqlite3
import datetime

sense = SenseHat()
sense.clear()

connection = sqlite3.connect('test.db')


def log(device, property, value):
    now = datetime.datetime.utcnow()
    values = (now, device, property, value)

    cursor = connection.cursor()
    cursor.execute("INSERT INTO readings VALUES(?,?,?,?)", values)
    connection.commit()


while True:
    orientation = sense.get_orientation_radians()
    compass = sense.get_compass_raw()
    acceleration = sense.get_accelerometer_raw()

    # Environmental sensors
    log("SenseHat", "humidity", sense.get_humidity())
    log("SenseHat", "temperature_from_humidity", sense.get_temperature())
    log("SenseHat", "temperature_from_pressure", sense.get_temperature_from_pressure())
    log("SenseHat", "pressure", sense.get_pressure())

    # IMU sensors
    log("SenseHat", "orientation.pitch", orientation['pitch'])
    log("SenseHat", "orientation.roll", orientation['roll'])
    log("SenseHat", "orientation.yaw", orientation['yaw'])
    log("SenseHat", "compass.x", compass['x'])
    log("SenseHat", "compass.y", compass['y'])
    log("SenseHat", "compass.z", compass['z'])
    log("SenseHat", "accelerometer.x", acceleration['x'])
    log("SenseHat", "accelerometer.y", acceleration['y'])
    log("SenseHat", "accelerometer.z", acceleration['z'])

    # time.sleep(0.5)
