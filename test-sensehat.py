#!/usr/bin/env python3

from Sensor import SenseController
import time

with SenseController() as sense_hat:
    sense_hat.show_message("ON")

    for _ in range(10):
        for reading in sense_hat.get_data():
            print("{0}: {1}".format(reading[1], str(reading[2])))
        time.sleep(0.25)
