# derived from https://github.com/ControlEverythingCommunity/MS5837-30BA01/blob/master/Python/MS5837_30BA01.py

import smbus
import time

ADDRESS = 0x76
RESET = 0x1E


class MS5837_30BA:
    def __init__(self):
        self.bus = smbus.SMBus(1)

        # reset
        self.bus.write_byte(ADDRESS, RESET)
        time.sleep(0.5)

        # Read 14 bytes of calibration data

        # Read crc
        data = self.bus.read_i2c_block_data(ADDRESS, 0xA0, 2)
        self.C0 = data[0] * 256 + data[1]

        # Read pressure sensitivity
        data = self.bus.read_i2c_block_data(ADDRESS, 0xA2, 2)
        self.C1 = data[0] * 256 + data[1]

        # Read pressure offset
        data = self.bus.read_i2c_block_data(ADDRESS, 0xA4, 2)
        self.C2 = data[0] * 256 + data[1]

        # Read temperature coefficient of pressure sensitivity
        data = self.bus.read_i2c_block_data(ADDRESS, 0xA6, 2)
        self.C3 = data[0] * 256 + data[1]

        # Read temperature coefficient of pressure offset
        data = self.bus.read_i2c_block_data(ADDRESS, 0xA8, 2)
        self.C4 = data[0] * 256 + data[1]

        # Read reference temperature
        data = self.bus.read_i2c_block_data(ADDRESS, 0xAA, 2)
        self.C5 = data[0] * 256 + data[1]

        # Read temperature coefficient of the temperature
        data = self.bus.read_i2c_block_data(ADDRESS, 0xAC, 2)
        self.C6 = data[0] * 256 + data[1]

    @property
    def pressure_raw(self):
        # Pressure conversion(OSR = 256) command
        self.bus.write_byte(0x76, 0x40)
        time.sleep(0.5)

        # Read digital pressure value
        # Read data back from 0x00(0), 3 bytes
        # D1 MSB2, D1 MSB1, D1 LSB
        value = self.bus.read_i2c_block_data(0x76, 0x00, 3)

        return value[0] * 65536 + value[1] * 256 + value[2]

    @property
    def temperature_raw(self):
        # Temperature conversion(OSR = 256) command
        self.bus.write_byte(0x76, 0x50)
        time.sleep(0.5)

        # Read digital temperature value
        # Read data back from 0x00(0), 3 bytes
        # D2 MSB2, D2 MSB1, D2 LSB
        value = self.bus.read_i2c_block_data(0x76, 0x00, 3)

        return value[0] * 65536 + value[1] * 256 + value[2]

    def get_properties(self):
        return [
             "pressure_raw",
             "temperature_raw"
        ]

    def get_data(self):
        return [
            (time.time(), "pressure_raw", self.pressure_raw),
            (time.time(), "temperature_raw", self.temperature_raw)
        ]
