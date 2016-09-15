#!/usr/bin/env python3

import sys
import platform
import signal
import shutil
import time
import curses
# from PIL import Image

if platform.system() == "Darwin":
    # use mock classes
    from mockcamera import PiCamera
else:
    # assume we're on a raspberry pi
    from picamera import PiCamera

# create access to camera
camera = PiCamera()

# create overlays
# img0 = Image.open('recording.png')
# pad0 = Image.new('RGB', (
#     ((img0.size[0] + 31) // 32) * 32,
#     ((img0.size[1] + 15) // 16) * 16))
# pad0.paste(img0, (0, 0), img0)
# o0 = camera.add_overlay(pad0.tostring(), size=img0.size)
# o0.layer = 3
# o0.alpha = 0

# img1 = Image.open('not-recording.png')
# pad1 = Image.new('RGB', (
#     ((img1.size[0] + 31) // 32) * 32,
#     ((img1.size[1] + 15) // 16) * 16))
# pad1.paste(img1, (0, 0), img1)
# o1 = camera.add_overlay(pad1.tostring(), size=img1.size)
# o1.layer = 4
# o1.alpha = 0

# create list of properties to display
properties = [
    "analog_gain",
    "annotate_text",
    "annotate_text_size",
    # "awb_gains",
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
    # the follwing is a read-only boolean property and it is not available on
    # the Pi 3
    # "led",
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

for property in properties:
    property_len = len(property)
    if max_len < property_len:
        max_len = property_len


def update_screen(stdscr):
    global max_len, properties
    row = 0
    col = 0
    max_col = 0

    # clear screen
    stdscr.clear()

    # display properties
    for key in properties:
        # just in case we have an invalid property, wrap this iteration in
        # a try/except statement
        try:
            # display key/value on screen
            # NOTE: we probably need to handle the case where the current
            # string cannot fit in the current row
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

    # move the cursor to a sensible location and update the screen
    stdscr.move(curses.LINES - 1, 0)
    stdscr.refresh()


def sigwinch_handler(n, frame):
    # based on example 5 at
    # http://www.programcreek.com/python/example/9546/curses.KEY_RESIZE
    size = shutil.get_terminal_size()
    curses.resizeterm(size.lines, size.columns)
    curses.ungetch(curses.KEY_RESIZE)


# display all current property values
def main(stdscr):
    preview = False
    recording = False

    while True:
        update_screen(stdscr)

        ch = stdscr.getch()

        # TODO: process keys here
        if ch == ord("q"):
            break
        elif ch == ord("-"):
            if camera.brightness > 0:
                camera.brightness -= 1
        elif ch == ord("="):
            if camera.brightness < 100:
                camera.brightness += 1
        elif ch == ord("_"):
            if camera.contrast > -100:
                camera.contrast -= 1
        elif ch == ord("+"):
            if camera.contrast < 100:
                camera.contrast += 1
        elif ch == ord("p"):
            preview = not preview
            if preview:
                camera.start_preview()
            else:
                camera.stop_preview()
        elif ch == ord("r"):
            recording = not recording
            if recording:
                timestamp = int(time.time())
                filename = "g2x-{}.h264".format(timestamp)
                camera.start_recording(filename)
                # o0.alpha = 255
                # o1.alpha = 0
                camera.annotate_text = "Recording"
            else:
                camera.stop_recording()
                # o0.alpha = 0
                # o1.alpha = 255
                camera.annotate_text = ""
        else:
            print("Unhandled key: " + str(ch), file=sys.stderr)


try:
    signal.signal(signal.SIGWINCH, sigwinch_handler)
    curses.wrapper(main)
finally:
    camera.close()
