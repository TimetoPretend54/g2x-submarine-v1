#!/usr/bin/env python3

from PWM import PWMController
from KeyDispatcher import KeyDispatcher
from Display import Display
from DataLogger import SQLiteLogger
import sys
import time

DEVICE = "PWM/Servo"


class Handler:
    def __init__(self, logger, pwm, channel):
        self.logger = logger
        self.pwm = pwm
        self.channel = channel

        self.frequency = 60
        self.on = 0
        self.off = 512
        self.pwm.set_frequency(self.frequency)
        self.pwm.set_pwm(self.channel, self.on, self.off)

        self.logger.log(DEVICE, "running", 1)

    def decrease_frequency(self):
        if self.frequency > 40:
            self.frequency -= 1
            self.pwm.set_frequency(self.frequency)
            self.logger.log(DEVICE, "frequency", self.frequency)

        return True

    def increase_frequency(self):
        if self.frequency < 1000:
            self.frequency += 1
            self.pwm.set_frequency(self.frequency)
            self.logger.log(DEVICE, "frequency", self.frequency)

        return True

    def decrease_on(self):
        if self.on > 0:
            self.on -= 1
            self.pwm.set_pwm(self.channel, self.on, self.off)
            self.logger.log(DEVICE, "on", self.on)

        return True

    def increase_on(self):
        if self.on < 4095:
            self.on += 1
            self.pwm.set_pwm(self.channel, self.on, self.off)
            self.logger.log(DEVICE, "on", self.on)

        return True

    def decrease_off(self):
        if self.off > 0:
            self.off -= 1
            self.pwm.set_pwm(self.channel, self.on, self.off)
            self.logger.log(DEVICE, "off", self.off)

        return True

    def increase_off(self):
        if self.off < 4095:
            self.off += 1
            self.pwm.set_pwm(self.channel, self.on, self.off)
            self.logger.log(DEVICE, "off", self.off)

        return True

    def quit(self):
        self.logger.log(DEVICE, "running", 0)
        return False

    def get_properties(self):
        return [
            "channel",
            "frequency",
            "on",
            "off"
        ]

    def get_data(self):
        now = time.time()

        return [
            (now, "channel", self.channel),
            (now, "frequency", self.frequency),
            (now, "on", self.on),
            (now, "off", self.off)
        ]


def update(display, handler):
    values = {}

    for item in handler.get_data():
        values[item[1]] = item[2]

    display.show_properties(values, handler.get_properties())


if len(sys.argv) == 2:
    channel = int(sys.argv[1])
else:
    channel = 0

with KeyDispatcher() as dispatcher, SQLiteLogger() as logger:
    pwm = PWMController()

    # setup key handlers
    # TODO: get name and channel from command-line
    handler = Handler(logger, pwm, channel)

    dispatcher.add("[", handler, "decrease_frequency")
    dispatcher.add("]", handler, "increase_frequency")
    dispatcher.add("_", handler, "decrease_on")
    dispatcher.add("+", handler, "increase_on")
    dispatcher.add("-", handler, "decrease_off")
    dispatcher.add("=", handler, "increase_off")
    dispatcher.add("q", handler, "quit")

    # setup display and start processing key presses
    display = Display(DEVICE, "[_/+] start [-/=] end [[/]] frequency [q]uit")

    update(display, handler)

    while dispatcher.process_key():
        update(display, handler)
