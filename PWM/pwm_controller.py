import Adafruit_PCA9685


class PWMController:
    def __init__(self):
        self.pwm = Adafruit_PCA9685.PCA9685()

    def set_frequency(self, freq):
        self.pwm.set_pwm_freq(freq)

    def set_pwm(self, channel, on, off):
        self.pwm.set_pwm(channel, on, off)
