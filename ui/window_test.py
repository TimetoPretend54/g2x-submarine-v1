#!/usr/bin/env python3

import signal
import shutil
import curses
from window import Window


def sigwinch_handler(n, frame):
    # based on example 5 at
    # http://www.programcreek.com/python/example/9546/curses.KEY_RESIZE
    size = shutil.get_terminal_size()
    curses.resizeterm(size.lines, size.columns)
    curses.ungetch(curses.KEY_RESIZE)


def main(stdscr):
    w1 = Window("Camera", (1, 1), (10, 10))
    w1.render(stdscr)

    stdscr.getkey()


signal.signal(signal.SIGWINCH, sigwinch_handler)
curses.wrapper(main)
