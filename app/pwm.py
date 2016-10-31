#!/usr/bin/env python3

from PWM import PWMController
from KeyDispatcher import KeyDispatcher
from Display import Display
from DataLogger import SQLiteLogger
import time

DEVICE = "PWM/Servo"


class Handler:
    def __init__(self, logger):
        self.logger = logger
        self.pwm = PWMController()
        self.logger.log(DEVICE, "running", 1)
        self.logger.log(DEVICE, "frequency", self.pwm.frequency)

    def add_device(self, name, channel, on, off):
        device = self.pwm.add_device(name, channel, on, off)

        self.logger.log(device.name, "on", device.on)
        self.logger.log(device.name, "off", device.off)

    def previous_device(self):
        self.pwm.previous_device()

        return True

    def next_device(self):
        self.pwm.next_device()

        return True

    def decrease_off_small(self):
        return self.adjust_off(-1)

    def increase_off_small(self):
        return self.adjust_off(1)

    def decrease_off_large(self):
        return self.adjust_off(-5)

    def increase_off_large(self):
        return self.adjust_off(5)

    def adjust_off(self, delta):
        device = self.pwm.current_device
        new_value = device.off + delta

        if device is not None and 0 <= new_value < 4096:
            device.off = new_value
            self.logger.log(device.name, "off", device.off)

        return True

    def reset(self):
        device = self.pwm.current_device

        if device is not None:
            device.reset()

        return True

    def quit(self):
        for device in self.pwm.devices:
            device.reset()
            self.logger.log(device.name, "off", device.off)

        self.logger.log(DEVICE, "running", 0)

        return False

    def get_data(self):
        now = time.time()
        device = self.pwm.current_device

        return [
            (now, "channel", device.channel),
            (now, "name", device.name),
            (now, "ticks", device.off),
            (now, "on_duration", device.on_duration),
            (now, "off_duration", device.off_duration),
            (now, "duty_cycle", device.duty_cycle)
        ]


def update(display, handler):
    properties = []
    values = {}

    for item in handler.get_data():
        properties.append(item[1])
        values[item[1]] = item[2]

    display.show_properties(values, properties)


with KeyDispatcher() as dispatcher, SQLiteLogger() as logger:
    # setup key handlers
    handler = Handler(logger)

    # [1100µs,1900µs] = [271,467] @ 60Hz
    handler.add_device("PWM Light", 2, 0, 320)
    handler.add_device("PWM Thruster", 1, 0, 400)

    dispatcher.add("p", handler, "previous_device")
    dispatcher.add("n", handler, "next_device")
    dispatcher.add("-", handler, "decrease_off_small")
    dispatcher.add("=", handler, "increase_off_small")
    dispatcher.add("_", handler, "decrease_off_large")
    dispatcher.add("+", handler, "increase_off_large")
    dispatcher.add("r", handler, "reset")
    dispatcher.add("q", handler, "quit")

    # setup display and start processing key presses
    display = Display(
        DEVICE,
        "[p]revious [n]ext [-/=] increment 1 [_/+] increment 5 [r]eset [q]uit"
    )

    update(display, handler)

    while dispatcher.process_key():
        update(display, handler)

    display.clear()
