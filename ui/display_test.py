#!/usr/bin/env python3

import signal
import shutil
import curses
from window import Window
from display import Display


def sigwinch_handler(n, frame):
    # based on example 5 at
    # http://www.programcreek.com/python/example/9546/curses.KEY_RESIZE
    size = shutil.get_terminal_size()
    curses.resizeterm(size.lines, size.columns)
    curses.ungetch(curses.KEY_RESIZE)


def main(stdscr):
    d = Display(stdscr)

    # add first window
    w1 = Window("Camera")
    d.add_window(w1)

    # add second window
    w2 = Window("Sense HAT")
    d.add_window(w2)

    # display results
    d.render()

    # process key presses
    while d.process_key():
        pass


signal.signal(signal.SIGWINCH, sigwinch_handler)
curses.wrapper(main)
