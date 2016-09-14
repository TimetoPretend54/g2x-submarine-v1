#!/usr/bin/env python3
"""
curses_resize.py -> run the program without hooking SIGWINCH
curses_resize.py 1 -> run the program with hooking SIGWINCH
"""

import sys
import curses
import signal
import time


def sigwinch_handler(n, frame):
    curses.endwin()
    curses.initscr()


def main(stdscr):
    """just repeatedly redraw a long string to reveal the window boundaries"""
    while 1:
        stdscr.insstr(0, 0, "abcd" * 5)
        stdscr.refresh()
        time.sleep(1)


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == "1":
        signal.signal(signal.SIGWINCH, sigwinch_handler)
    curses.wrapper(main)
