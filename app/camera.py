#!/usr/bin/env python3

from Camera import CameraController
from KeyDispatcher import KeyDispatcher
from Display import Display


class Handler:
    def __init__(self, camera):
        self.camera = camera

    def increase_brightness(self):
        self.camera.brightness += 1
        return True

    def decrease_brightness(self):
        self.camera.brightness -= 1
        return True

    def increase_contrast(self):
        self.camera.contrast += 1
        return True

    def decrease_contrast(self):
        self.camera.contrast -= 1
        return True

    def toggle_preview(self):
        self.camera.toggle_preview()
        return True

    def toggle_record(self):
        self.camera.toggle_record()
        return True

    def quit(self):
        return False


def update(display, camera):
    values = {}

    for item in camera.get_data():
        values[item[1]] = item[2]

    display.show_properties(values)


with CameraController() as camera:
    with KeyDispatcher() as dispatcher:
        display = Display("Camera")
        handler = Handler(camera)

        dispatcher.add("-", handler, "decrease_brightness")
        dispatcher.add("=", handler, "increase_brightness")
        dispatcher.add("_", handler, "decrease_contrast")
        dispatcher.add("+", handler, "increase_contrast")
        dispatcher.add("p", handler, "toggle_preview")
        dispatcher.add("r", handler, "toggle_record")
        dispatcher.add("q", handler, "quit")

        update(display, camera)

        while dispatcher.process_key():
            update(display, camera)
