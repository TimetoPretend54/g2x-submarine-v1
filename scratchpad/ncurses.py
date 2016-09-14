#!/usr/bin/env python3

from curses import wrapper
import platform

if platform.system() == "Darwin":
	# create mock class for Pi Camera
	class PiCamera:
		def __init__(self):
			self.brightness = 10
			self.contrast = 24
else:
	from picamera import PiCamera

properties = [
	"brightness",
	"contrast"
]

camera = PiCamera()

def main(stdscr):
	# clear screen
	stdscr.clear()

	row = 0
	for key in properties:
		value = getattr(camera, key)
		string = key + ": " + str(value)
		stdscr.addstr(row, 0, string)
		row = row + 1

	stdscr.refresh()
	stdscr.getkey()

wrapper(main)
