#!/usr/bin/env python3

import os
import time
import io
import re
import argparse
import sys

import pystache
from PIL import Image
import cairosvg

from DataManager import DataManager


class Data:
    def __init__(self, secs_since_epoch, depth_data):
        self.time = time.localtime(secs_since_epoch)
        self.depth_data = depth_data

    def frame_date(self):
        return time.strftime("%B %d, %Y", self.time)

    def frame_time(self):
        return time.strftime("%I:%M:%S %p", self.time)

    def frame_depth_data(self):
        return self.depth_data


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="The directory that contains the input frames")
    parser.add_argument("-o", "--output", help="The directory to write the composited frames")
    parser.add_argument("-s", "--start", type=int, help="The frame number to start processing")
    parser.add_argument("-e", "--end", type=int, help="The frame number to end processing")
    args = parser.parse_args()

    if args.input is None:
        raise ValueError('input directory must be defined')

    if args.output is None:
        raise ValueError('output directory must be defined')

    if args.start is None:
        start = 0
    else:
        start = args.start

    if args.end is None:
        end = sys.maxsize
    else:
        end = args.end

    return {
        "input": args.input,
        "output": args.output,
        "start": start,
        "end": end
    }


def map_range(x, in_min, in_max, out_min, out_max):
    out_delta = out_max - out_min
    in_delta = in_max - in_min

    return (x - in_min) * out_delta / in_delta + out_min


options = process_args()

# load data
data_manager = DataManager()
data_manager.load("../db/g2x-1479064727.db")

# create renderer
renderer = pystache.Renderer()

# load template
template_file = open('./overlay.svg.mustache')
template = template_file.read()
template_file.close()

# process all files
frame_dir = options["input"]
composite_dir = options["output"]
start_frame = options["start"]
end_frame = options["end"]

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

    if frame_number < start_frame or end_frame < frame_number:
        continue

    print("processing frame {0}".format(str(int(frame_number))))

    # load frame
    frame_full_path = frame_dir + "/" + frame_file
    frame = Image.open(frame_full_path, 'r')

    # load data
    def map_depth(item):
        return ",".join([
            str(round(map_range(item[0], frame_time - 60, frame_time, 0, 100), 3)),
            str(round(map_range(item[1], -2.5, 1000, 0, 300), 3))
        ])

    depth_data = data_manager.select_depths(frame_time - 60, frame_time)
    # print(depth_data)
    depth_path_data = "M" + " ".join(map(map_depth, depth_data))
    frame_data = Data(frame_time, depth_path_data)

    # render SVG text
    svg = renderer.render(template, frame_data)
    # print(svg)

    # create overlay image from SVG
    overlay_bytes = cairosvg.svg2png(bytestring=svg)
    overlay = Image.open(io.BytesIO(overlay_bytes))

    # create composite image holder
    composite = Image.new('RGB', frame.size, (255, 255, 255))

    # composite images
    composite.paste(frame)
    composite.paste(overlay, (0, 0), overlay)

    # output result
    composite_full_path = composite_dir + "/" + frame_no_ext + ".png"
    composite.save(composite_full_path, optimize=False)
