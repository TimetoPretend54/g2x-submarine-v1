# derived from the following libraries:
#   https://github.com/bluerobotics/BlueRobotics_MS5837_Library/blob/master/MS5837.cpp
#   https://github.com/ControlEverythingCommunity/MS5837-30BA01/blob/master/Python/MS5837_30BA01.py

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
        time.sleep(0.02)  # Max conversion time per datasheet

        # Read digital pressure value
        # Read data back from 0x00(0), 3 bytes
        # D1 MSB2, D1 MSB1, D1 LSB
        value = self.bus.read_i2c_block_data(0x76, 0x00, 3)

        return value[0] * 65536 + value[1] * 256 + value[2]

    @property
    def temperature_raw(self):
        # Temperature conversion(OSR = 256) command
        self.bus.write_byte(0x76, 0x50)
        time.sleep(0.02)  # Max conversion time per datasheet

        # Read digital temperature value
        # Read data back from 0x00(0), 3 bytes
        # D2 MSB2, D2 MSB1, D2 LSB
        value = self.bus.read_i2c_block_data(0x76, 0x00, 3)

        return value[0] * 65536 + value[1] * 256 + value[2]

    # pressure_raw is D1 in data sheet
    # temperature_raw is D2 in the data sheet
    def calculate_values(self, pressure_raw, temperature_raw):
        dT    = temperature_raw - self.C5 * 256
        SENS  = self.C1 * 32768 + (self.C3 * dT) / 256
        OFF   = self.C2 * 65536 + (self.C4 * dT) / 128

        TEMP  = 2000 + dT * self.C6 / 8388608

        T2    = 0
        OFF2  = 0
        SENS2 = 0

        if TEMP >= 2000:
            T2    = 2 * (dT * dT) / 137438953472
            OFF2  = ((TEMP - 2000) * (TEMP - 2000)) / 16
            SENS2 = 0
        elif TEMP < 2000:
            T2    = 3 * (dT * dT) / 8589934592
            OFF2  = 3 * ((TEMP - 2000) * (TEMP - 2000)) / 2
            SENS2 = 5 * ((TEMP - 2000) * (TEMP - 2000)) / 8
            if TEMP < -1500:
                OFF2  = OFF2 + 7 * ((TEMP + 1500) * (TEMP + 1500))
                SENS2 = SENS2 + 4 * ((TEMP + 1500) * (TEMP + 1500))

        OFF2       = OFF - OFF2
        SENS2      = SENS - SENS2

        pressure   = ((((pressure_raw * SENS2) / 2097152) - OFF2) / 8192) / 10.0

        TEMP       = TEMP - T2
        celsius    = TEMP / 100.0
        fahrenheit = celsius * 1.8 + 32

        return (pressure, celsius, fahrenheit)

    def get_properties(self):
        return [
            "pressure_raw",
            "temperature_raw",
            "mbars",
            "celcius",
            "fahrenheit"
        ]

    def get_data(self):
        pressure_time = time.time()
        pressure_raw = self.pressure_raw
        temperature_time = time.time()
        temperature_raw = self.temperature_raw
        values_time = time.time()
        pressure, celcius, fahrenheit = self.calculate_values(pressure_raw, temperature_raw)

        return [
            (pressure_time, "pressure_raw", pressure_raw),
            (temperature_time, "temperature_raw", temperature_raw),
            (values_time, "mbars", pressure),
            (values_time, "celcius", celcius),
            (values_time, "fahrenheit", fahrenheit)
        ]
