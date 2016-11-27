import re
import os

# create regex for extracting time data from file names
TIME_AND_FRAME_PATTERN = re.compile(r"^g2x-(\d+)-(\d+)$")


class Frame:
    def __init__(self, base_dir, frame_file):
        self.base_dir = base_dir
        self.frame_file = frame_file
        self.full_path = self.base_dir + "/" + self.frame_file
        self.base_name = os.path.splitext(frame_file)[0]
        file_match = TIME_AND_FRAME_PATTERN.search(self.base_name)

        if file_match is not None:
            base_time = float(file_match.group(1))

            self.frame_number = float(file_match.group(2))
            self.frame_time = base_time + self.frame_number / 24
        else:
            self.frame_number = -1
            self.frame_time = -1

    def in_range(self, low, high):
        return low <= self.frame_number <= high
