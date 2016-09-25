#!/usr/bin/env python3

from Display import Display

values = {
    "temperature": 93,
    "humidity": 50
}

d = Display("Sense Hat")

d.show_properties(values)
