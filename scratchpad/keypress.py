#!/usr/bin/env python3

import tty
import sys
import termios
import picamera

orig_settings = termios.tcgetattr(sys.stdin)
camera = picamera.PiCamera()

try:
    preview = False

    tty.setraw(sys.stdin)
    key = 0

    while True:
        key = sys.stdin.read(1)[0]
        
        if key == '-':
            if camera.brightness > 0:
                camera.brightness -= 1
        elif key == '=':
            if camera.brightness < 100:
                camera.brightness += 1
        elif key == '_':
            if camera.contrast > -100:
                camera.contrast -= 1
        elif key == '+':
            if camera.contrast < 100:
                camera.contrast += 1
        elif key == ' ':
            preview = not preview
            if preview:
                camera.start_preview()
            else:
                camera.stop_preview()
        elif key == chr(27):
            break
        else:
            print("You pressed", key)
finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
    camera.close()
