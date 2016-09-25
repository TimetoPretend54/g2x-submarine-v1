#!/usr/bin/env python3

from DataLogger import SQLiteLogger

with SQLiteLogger("g2x.db") as logger:
    logger.log("Test", "property", 100)
