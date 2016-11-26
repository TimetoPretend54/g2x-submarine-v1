#!/usr/bin/env python3

import os
import time
import io
import re
import argparse
import sys

from PIL import Image
import cairosvg

from SVGGenerator import SVGGenerator
from DataManager import DataManager
from Data import Data
from Chart import Chart

# create regex for extracting time data from file names
TIME_AND_FRAME_PATTERN = re.compile(r"(\d+)-(\d+)$")


def process_args():
    start = 0
    end = sys.maxsize
    show_svg = False

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="The directory that contains the input frames")
    parser.add_argument("-o", "--output", help="The directory to write the composited frames")
    parser.add_argument("-s", "--start", type=int, help="The frame number to start processing")
    parser.add_argument("-e", "--end", type=int, help="The frame number to end processing")
    args = parser.parse_args()

    # check for required arguments
    if args.input is None:
        raise ValueError('input directory must be defined')

    if args.output is None:
        raise ValueError('output directory must be defined')

    # handle optional arguments
    if args.start is not None:
        start = args.start

    if args.end is not None:
        end = args.end

    # return dictionary of values
    # NOTE: what do we need here to be able to use dot notation for these properties?
    return {
        "input": args.input,
        "output": args.output,
        "start": start,
        "end": end,
        "show_svg": show_svg
    }


def map_range(x, in_min, in_max, out_min, out_max):
    out_delta = out_max - out_min
    in_delta = in_max - in_min

    return (x - in_min) * out_delta / in_delta + out_min


def frame_info(frame_file):
    frame_no_ext = os.path.splitext(frame_file)[0]
    file_match = TIME_AND_FRAME_PATTERN.search(frame_no_ext)
    base_time = float(file_match.group(1))
    frame_number = float(file_match.group(2))
    frame_time = base_time + frame_number / 24

    return (frame_no_ext, frame_number, frame_time)


def get_frame_data(frame_time, frame_full_path):
    # load data
    def map_depth(item):
        result = ",".join([
            str(round(map_range(item[0], frame_time - 60, frame_time, 0, 100), 3)),
            str(round(map_range(item[1], map_depth.start, map_depth.end, 0, 100), 3))
        ])

        # print("{0} became {1}".format(item, result))
        return result

    depth_data = data_manager.select_depths(frame_time - 60, frame_time)

    if len(depth_data) > 0:
        map_depth.start = depth_data[-1][1] - 50
        map_depth.end = depth_data[-1][1] + 50
        depth_text = "{0:0.2f} ft".format(depth_data[-1][1])
        depth_path_data = "M" + " ".join(map(map_depth, depth_data))
    else:
        depth_text = "-- ft"
        depth_path_data = ""

    def map_temperature(item):
        result = ",".join([
            str(round(map_range(item[0], frame_time - 60, frame_time, 0, 100), 3)),
            str(round(map_range(item[1], 40, 55, 100, 0), 3))
        ])

        # print("{0} became {1}".format(item, result))
        return result

    temperature_data = data_manager.select_temperatures(frame_time - 60, frame_time)

    if len(temperature_data) > 0:
        temperature_text = "{0:0.2f} °F".format(temperature_data[-1][1])
        temperature_path_data = "M" + " ".join(map(map_temperature, temperature_data))
    else:
        temperature_text = "-- °F"
        temperature_path_data = ""

    # for testing
    depth_chart = Chart("Depth", depth_text, depth_path_data)
    depth_chart.x = 5
    depth_chart.y = 972 - 5 - 110

    temperature_chart = Chart("Temperature", temperature_text, temperature_path_data)
    temperature_chart.x = 5 + 5 + 100 + 5 + 5
    temperature_chart.y = 972 - 5 - 110

    # print(depth_path_data)
    return Data(frame_time, depth_chart, temperature_chart, frame_full_path)


# process command line arguments
options = process_args()

frame_dir = options["input"]
composite_dir = options["output"]
start_frame = options["start"]
end_frame = options["end"]
show_svg = options["show_svg"]

# load data
data_manager = DataManager()
data_manager.load("../db/g2x-1479064727.db")

# make svg generator
generator = SVGGenerator('./overlay.svg.mustache')

# process all frames in the frame directory
for frame_file in os.listdir(frame_dir):
    if frame_file == ".DS_Store":
        continue

    # extract frame number and time from file name
    (frame_no_ext, frame_number, frame_time) = frame_info(frame_file)

    # skip frames we don't want to process
    if frame_number < start_frame or end_frame < frame_number:
        continue

    # let the user know which frame we're currently processing
    print("frame={0}, time={1}".format(str(int(frame_number)), str(round(frame_time, 3))))

    # load frame
    frame_full_path = frame_dir + "/" + frame_file
    frame = Image.open(frame_full_path, 'r')

    # get data for this frame
    frame_data = get_frame_data(frame_time, frame_full_path)

    # render SVG text
    svg = generator.to_svg(frame_data)
    if show_svg:
        print(svg)

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

    # cairosvg.svg2png(bytestring=svg, write_to=composite_full_path)
