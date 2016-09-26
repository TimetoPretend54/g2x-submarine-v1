#!/usr/bin/env python3

from Sensor import SenseController
from KeyDispatcher import KeyDispatcher
from Display import Display
from DataLogger import SQLiteLogger
import time


DEVICE = "PiSense"
DELAY = 0.0


class Handler:
    def __init__(self, display, logger, sensor):
        self.display = display
        self.logger = logger
        self.sensor = sensor
        self.logger.log(DEVICE, "running", 1)

    def read(self):
        values = {}

        for reading in self.sensor.get_data():
            values[reading[1]] = reading[2]
            self.logger.log(DEVICE, reading[1], reading[2], reading[0])

        display.show_properties(values, self.sensor.get_properties())
        return True

    def quit(self):
        self.logger.log(DEVICE, "running", 0)
        return False


with SenseController() as sensor, KeyDispatcher() as dispatcher, SQLiteLogger() as logger:
    # setup display
    display = Display("PiSense")

    # setup key handlers
    handler = Handler(display, logger, sensor)

    dispatcher.add("q", handler, "quit")

    # start processing key presses
    while True:
        if dispatcher.can_process_key():
            if not dispatcher.process_key():
                break
        else:
            handler.read()
            time.sleep(DELAY)
