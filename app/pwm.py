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

    @property
    def duty_cycle(self):
        on_duration = abs(self.off - self.on)

        return round(100.0 * on_duration / 4096, 2)

    def on_duration(self, freq):
        one_cycle = 1.0 / freq
        on_percent = abs(self.off - self.on) / 4096.0

        return round(1000000 * one_cycle * on_percent, 2)

    def off_duration(self, freq):
        one_cycle = 1.0 / freq
        off_percent = 1.0 - (abs(self.off - self.on) / 4096.0)

        return round(1000000 * one_cycle * off_percent, 2)


class Handler:
    def __init__(self, logger):
        self.logger = logger
        self.pwm = PWMController()
        self.devices = []
        self.current_index = 0
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
        if self.pwm.frequency > 40:
            self.pwm.frequency -= 1
            self.logger.log(DEVICE, "frequency", self.pwm.frequency)

        return True

    def increase_frequency(self):
        if self.pwm.frequency < 1000:
            self.pwm.frequency += 1
            self.logger.log(DEVICE, "frequency", self.pwm.frequency)

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
            "off",
            "on_duration",
            "off_duration",
            "duty_cycle"
        ]

    def get_data(self):
        now = time.time()
        device = self.devices[self.current_index]
        frequency = self.pwm.frequency

        return [
            (now, "channel", device.channel),
            (now, "name", device.name),
            (now, "frequency", frequency),
            (now, "on", device.on),
            (now, "off", device.off),
            (now, "on_duration", device.on_duration(frequency)),
            (now, "off_duration", device.off_duration(frequency)),
            (now, "duty_cycle", device.duty_cycle)
        ]


def update(display, handler):
    values = {}

    for item in handler.get_data():
        values[item[1]] = item[2]

    display.show_properties(values, handler.get_properties())


with KeyDispatcher() as dispatcher, SQLiteLogger() as logger:
    # setup key handlers
    handler = Handler(logger)

    # [1100µs,1900µs] = [271,467] @ 60Hz
    handler.add_device("PWM Light", 0, 0, 467)
    handler.add_device("PWM Thruster", 1, 0, 271)

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
    display = Display(
        DEVICE,
        "[p]revious [n]ext [_/+] start [-/=] end [[/]] frequency [q]uit"
    )

    update(display, handler)

    while dispatcher.process_key():
        update(display, handler)
