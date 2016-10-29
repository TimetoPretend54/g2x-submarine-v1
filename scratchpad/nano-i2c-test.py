#!/usr/bin/env python3

import smbus
import time

# for RPI version 1, use “bus = smbus.SMBus(0)”
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04
cmd_read_analog = 1


while True:
    number = bus.read_word_data(address, cmd_read_analog)

    print("analog value =", "{0:4X}".format(number))

    # wait for a bit for next reading
    time.sleep(1)
