#!/usr/bin/env python3

import curses
import platform

if platform.system() == "Darwin":
	from mockcamera import PiCamera
else:
	from picamera import PiCamera

# create access to camera
camera = PiCamera()

# create list of properties to display
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
	#"led",				# this is a read-only boolean property and it is not available on the Pi 3
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

# get maximum property name length for padding during display
max_len = 0
max_col = 0

for property in properties:
	property_len = len(property)
	if max_len < property_len:
		max_len = property_len

# display all current property values
try:
	def main(stdscr):
		global max_len, max_col, properties

		# clear screen
		stdscr.clear()

		row = 0
		col = 0
		for key in properties:
			# just in case we have an invalid property, wrap this iteration in
			# a try/except statement
			try:
				# display key/value on screen
				# NOTE: we probably need to handle the case where the current string
				# cannot fit in the current row
				value = getattr(camera, key)
				string = key.rjust(max_len) + ": " + str(value)
				stdscr.addstr(row, col, string)

				# update max_col
				current_end_col = col + len(string)

				if current_end_col > max_col:
					max_col = current_end_col

				# update current row
				row = row + 1

				if row >= curses.LINES:
					row = 0
					col = max_col + 2

					# we're off of the display
					if col >= curses.COLS:
						break
			except:
				print("An exception occurred", file=sys.stderr)
				pass

		# move the cursor to a sensible location and update the screen
		stdscr.move(curses.LINES - 1, 0)
		stdscr.refresh()

		# wait for a keypress
		# TODO: process key here
		stdscr.getkey()

	curses.wrapper(main)
finally:
	camera.close()
