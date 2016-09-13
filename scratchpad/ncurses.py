#!/usr/bin/env python3

from curses import wrapper


def main(stdscr):
	# clear screen
	stdscr.clear()

	stdscr.refresh()
	stdscr.getkey()

wrapper(main)
