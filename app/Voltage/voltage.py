import smbus
import time

ADDRESS = 4
CMD_READ_ANALOG = 1


class Voltage:
    def __init__(self):
        self.bus = smbus.SMBus(1)

    def get_data(self):
        return [
            (time.time(), "voltage", self.bus.read_word_data(ADDRESS, CMD_READ_ANALOG))
        ]
