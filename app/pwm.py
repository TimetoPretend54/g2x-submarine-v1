#!/usr/bin/env python3

from PWM import PWMController
from KeyDispatcher import KeyDispatcher
from Display import Display
from DataLogger import SQLiteLogger
import time

DEVICE = "PWM/Servo"


class Device:
    def __init__(self, name, channel, on, off):
        self.name = name
        self.channel = channel
        self.on = on
        self.off = off


class Handler:
    def __init__(self, logger, pwm):
        self.logger = logger
        self.pwm = pwm
        self.devices = []
        self.current_index = 0
        self.frequency = 60
        self.pwm.set_frequency(self.frequency)
        self.logger.log(DEVICE, "running", 1)

    def add_device(self, name, channel, on, off):
        device = Device(name, channel, on, off)
        self.devices.append(device)
        self.pwm.set_pwm(device.channel, device.on, device.off)

    def previous_device(self):
        self.current_index = (self.current_index - 1) % len(self.devices)
        return True

    def next_device(self):
        self.current_index = (self.current_index + 1) % len(self.devices)
        return True

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
        device = self.devices[self.current_index]

        if device.on > 0:
            device.on -= 1
            self.pwm.set_pwm(device.channel, device.on, device.off)
            self.logger.log(device.name, "on", device.on)

        return True

    def increase_on(self):
        device = self.devices[self.current_index]

        if device.on < 4095:
            device.on += 1
            self.pwm.set_pwm(device.channel, device.on, device.off)
            self.logger.log(device.name, "on", device.on)

        return True

    def decrease_off(self):
        device = self.devices[self.current_index]

        if device.off > 0:
            device.off -= 1
            self.pwm.set_pwm(device.channel, device.on, device.off)
            self.logger.log(device.name, "off", device.off)

        return True

    def increase_off(self):
        device = self.devices[self.current_index]

        if device.off < 4095:
            device.off += 1
            self.pwm.set_pwm(device.channel, device.on, device.off)
            self.logger.log(device.name, "off", device.off)

        return True

    def quit(self):
        self.logger.log(DEVICE, "running", 0)
        return False

    def get_properties(self):
        return [
            "channel",
            "name",
            "frequency",
            "on",
            "off"
        ]

    def get_data(self):
        now = time.time()
        device = self.devices[self.current_index]

        return [
            (now, "channel", device.channel),
            (now, "name", device.name),
            (now, "frequency", self.frequency),
            (now, "on", device.on),
            (now, "off", device.off)
        ]


def update(display, handler):
    values = {}

    for item in handler.get_data():
        values[item[1]] = item[2]

    display.show_properties(values, handler.get_properties())


with KeyDispatcher() as dispatcher, SQLiteLogger() as logger:
    # setup PWM controller
    pwm = PWMController()

    # setup key handlers
    handler = Handler(logger, pwm)
    handler.add_device("PWM Light", 0, 0, 512)
    handler.add_device("PWM Motor", 1, 0, 512)

    dispatcher.add("p", handler, "previous_device")
    dispatcher.add("n", handler, "next_device")
    dispatcher.add("[", handler, "decrease_frequency")
    dispatcher.add("]", handler, "increase_frequency")
    dispatcher.add("_", handler, "decrease_on")
    dispatcher.add("+", handler, "increase_on")
    dispatcher.add("-", handler, "decrease_off")
    dispatcher.add("=", handler, "increase_off")
    dispatcher.add("q", handler, "quit")

    # setup display and start processing key presses
    display = Display(DEVICE, "[p]revious [n]ext [_/+] start [-/=] end [[/]] frequency [q]uit")

    update(display, handler)

    while dispatcher.process_key():
        update(display, handler)
