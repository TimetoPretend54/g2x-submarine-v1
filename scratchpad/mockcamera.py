from fractions import Fraction

class PiCamera:
	def __init__(self):
		self.analog_gain           = 0
		self.annotate_text         = ""
		self.annotate_text_size    = 32
		self.awb_gains             = (Fraction(0,1), Fraction(0,1))
		self.awb_mode              = "auto"
		self.brightness            = 50
		self.color_effects         = None
		self.contrast              = 0
		self.crop                  = (0.0, 0.0, 1.0, 1.0)
		self.digital_gain          = 0
		self.drc_strength          = "off"
		self.exposure_compensation = 0
		self.exposure_mode         = "auto"
		self.exposure_speed        = 0
		self.flash_mode            = "off"
		self.framerate             = 30
		self.framerate_delta       = 0
		self.hflip                 = False
		self.image_denoise         = True
		self.image_effect          = "none"
		self.iso                   = 0
		self.meter_mode            = "average"
		self.resolution            = "1280x1024"
		self.rotation              = 0
		self.saturation            = 0
		self.sensor_mode           = 0
		self.sharpness             = 0
		self.shutter_speed         = 0
		self.vflip                 = False
		self.video_denoise         = True
		self.video_stabilization   = False
		self.zoom                  = (0.0, 0.0, 1.0, 1.0)

	def close():
		pass
