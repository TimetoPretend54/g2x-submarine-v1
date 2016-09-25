from picamera import PiCamera
import time


class CameraController:
    def __init__(self, resolution=(1296, 972), framerate=24):
        self.camera = None
        self.resolution = resolution
        self.framerate = framerate

    def preview(self, state):
        if state:
            self.camera.start_preview()
        else:
            self.camera.stop_preview()

    def record(self, state):
        if state:
            timestamp = int(time.time())
            filename = "g2x-{}.h264".format(timestamp)
            self.camera.start_recording(filename)
        else:
            self.camera.stop_recording()

    @property
    def brightness(self):
        return self.camera.brightness

    @brightness.setter
    def brightness(self, value):
        value = max(0, min(value, 100))

        self.camera.brightness = value

    @property
    def contrast(self):
        return self.camera.contrast

    @contrast.setter
    def contrast(self, value):
        value = max(-100, min(value, 100))

        self.camera.contrast = value

    def __enter__(self):
        self.camera = PiCamera(resolution=self.resolution, framerate=self.framerate)
        return self

    def __exit__(self, type, value, traceback):
        self.camera.close()
        self.camera = None
