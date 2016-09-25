import sys

ESC       = chr(27)
CLEAR     = ESC + "[2J"
MOVE_HOME = ESC + "[H"
ERASE     = CLEAR + MOVE_HOME

LINES = 24
COLS = 80


class Display:
    def __init__(self, title):
        self.title = title

    def clear(self):
        sys.stdout.write(ERASE)

    def show_properties(self, properties):
        self.clear()
        self.print(self.title)
        print()

        for k, v in properties.items():
            self.print("{0}: {1}".format(k, v))

    def print(self, message):
        print(message, end="\x0a\x0d")
