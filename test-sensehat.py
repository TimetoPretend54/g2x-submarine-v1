#!/usr/bin/env python3

from Sensor import SenseController
from DataLogger import ScreenLogger
import time

with SenseController() as sense_hat, ScreenLogger() as logger:
    sense_hat.show_message("ON")

    for _ in range(10):
        for reading in sense_hat.get_data():
            logger.log("SenseHat", reading[1], reading[2], reading[0])
        time.sleep(0.5)
