#!/usr/bin/env python3

from KeyDispatcher import KeyDispatcher
from Display import Display
from DataLogger import SQLiteLogger
import time

# TODO: move to a separate class
import smbus
ADDRESS = 4
CMD_READ_ANALOG = 1
# TODO: end

DEVICE = "Arduino Nano"
DELAY = 1


class Handler:
    def __init__(self, display, logger):
        self.display = display
        self.logger = logger
        self.recording = False
        self.bus = smbus.SMBus(1)

    def record(self):
        self.recording = not self.recording

        if self.recording:
            self.logger.log(DEVICE, "recording", 1)
        else:
            self.logger.log(DEVICE, "recording", 0)

        return True

    def read(self):
        properties = []
        values = {}

        if self.recording:
            voltage = self.bus.read_word_data(ADDRESS, CMD_READ_ANALOG)
            properties.append("voltage")
            values["voltage"] = voltage
            self.logger.log(DEVICE, "voltage", voltage, time.time())
            self.display.show_properties(values, properties)
        else:
            values["recording"] = False
            self.display.show_properties(values)

        return True

    def quit(self):
        self.logger.log(DEVICE, "running", 0)

        return False


with KeyDispatcher() as dispatcher, SQLiteLogger() as logger:
    # setup display
    display = Display(DEVICE, "[r]ecord [q]uit")

    # create key handler
    handler = Handler(display, logger)

    # register keys
    dispatcher.add("r", handler, "record")
    dispatcher.add("q", handler, "quit")

    while True:
        if dispatcher.can_process_key():
            if not dispatcher.process_key():
                break
        else:
            handler.read()
            time.sleep(DELAY)

    display.clear()
