#!/usr/bin/env python3

import os
import time
import io
import re

import pystache
from PIL import Image
import cairosvg


class Data:
    def __init__(self, secs_since_epoch):
        self.time = time.localtime(secs_since_epoch)

    def frame_date(self):
        return time.strftime("%B %d, %Y", self.time)

    def frame_time(self):
        return time.strftime("%I:%M:%S %p", self.time)


# create renderer
renderer = pystache.Renderer()

# load template
template_file = open('./overlay.svg.mustache')
template = template_file.read()
template_file.close()

# process all files
frame_dir = '/Users/kevin/Desktop/Second Dive/g2x-1479068752/'
composite_dir = '/Users/kevin/Desktop/Second Dive/g2x-1479068752-composites/'

# create regex for extracting time data from file names
time_and_frame_pattern = re.compile(r"(\d+)-(\d+)$")

# process all frames in the frame directory
for frame_file in os.listdir(frame_dir):
    if frame_file == ".DS_Store":
        continue

    # extract frame's time from file name
    frame_no_ext = os.path.splitext(frame_file)[0]
    file_match = time_and_frame_pattern.search(frame_no_ext)
    base_time = float(file_match.group(1))
    frame_number = float(file_match.group(2))
    frame_time = base_time + frame_number / 24

    print("processing frame {0}...".format(str(int(frame_number))))

    # load frame
    frame_full_path = frame_dir + frame_file
    frame = Image.open(frame_full_path, 'r')

    # load data
    frame_data = Data(frame_time)

    # render SVG text
    svg = renderer.render(template, frame_data)

    # create overlay image from SVG
    overlay_bytes = cairosvg.svg2png(bytestring=svg)
    overlay = Image.open(io.BytesIO(overlay_bytes))

    # create composite image holder
    composite = Image.new('RGB', frame.size, (255, 255, 255))

    # composite images
    composite.paste(frame)
    composite.paste(overlay, (0, 0), overlay)

    # output result
    composite_full_path = composite_dir + frame_no_ext + ".png"
    composite.save(composite_full_path, optimize=False)
