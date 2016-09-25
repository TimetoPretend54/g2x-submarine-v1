#!/usr/bin/env python3

from Camera import CameraController
import time

with CameraController() as camera:
    camera.preview(True)
    time.sleep(3)
    camera.record(True)
    time.sleep(1)
    camera.brightness += 5
    time.sleep(1)
    camera.brightness += 5
    time.sleep(1)
    camera.brightness += 5
    time.sleep(1)
    camera.contrast += 5
    time.sleep(1)
    camera.contrast += 5
    time.sleep(1)
    camera.contrast += 5
    time.sleep(1)
    camera.record(False)
    camera.preview(False)
