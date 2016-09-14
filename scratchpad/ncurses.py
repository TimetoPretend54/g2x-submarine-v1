#!/usr/bin/env python3

import curses
import platform

if platform.system() == "Darwin":
	# create mock class for Pi Camera
	class PiCamera:
		def __init__(self):
			self.brightness = 10
			self.contrast = 24

		def close():
			pass
else:
	# assumes we're running on Raspberry Pi
	from picamera import PiCamera

properties = [
	"analog_gain",
	"annotate_text",
	"annotate_text_size",
	"awb_gains",
	"awb_mode",
	"brightness",
	"color_effects",
	"contrast",
	"crop",
	"digital_gain",
	"drc_strength",
	"exposure_compensation",
	"exposure_mode",
	"exposure_speed",
	"flash_mode",
	"framerate",
	"framerate_delta",
	"hflip",
	"image_denoise",
	"image_effect",
	"iso",
	"led",
	"meter_mode",
	"resolution",
	"rotation",
	"saturation",
	"sensor_mode",
	"sharpness",
	"shutter_speed",
	"vflip",
	"video_denoise",
	"video_stabilization",
	"zoom"
]

camera = PiCamera()

try:
	def main(stdscr):
		# clear screen
		stdscr.clear()

		row = 0
		col = 0
		for key in properties:
			value = getattr(camera, key)
			string = key + ": " + str(value)
			stdscr.addstr(row, col, string)
			row = row + 1

			if row >= curses.LINES:
				row = 0
				col += 20

		stdscr.move(curses.LINES - 1, 0)
		stdscr.refresh()
		stdscr.getkey()

	curses.wrapper(main)
finally:
	camera.close()
