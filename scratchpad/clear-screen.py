#!/usr/bin/env python3

import time

ESC = chr(27)
CLEAR = ESC + "[2J"
MOVE_HOME = ESC + "[H"
ERASE = CLEAR + MOVE_HOME

print("Hello")
time.sleep(2)
print(ERASE + "Hello again")
