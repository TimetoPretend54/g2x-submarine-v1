import Adafruit_PCA9685


class PWMController:
    def __init__(self):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.frequency = 60

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, freq):
        # [40,1000] comes from Adafruit docs
        self._frequency = max(40, min(freq, 1000))

        self.pwm.set_pwm_freq(self._frequency)

    # on/off are in ticks (based on freq)
    def set_pwm(self, channel, on, off):
        # [0,15] comes from Adafruit docs
        channel = max(0, min(channel, 15))

        # [0,4095] comes from Adafruit docs
        on = max(0, min(on, 4095))
        off = max(0, min(off, 4095))

        self.pwm.set_pwm(channel, on, off)
