#!/usr/bin/env python3

from sqlite_logger import SQLiteLogger
import time

logger = SQLiteLogger()

for i in range(10):
    logger.log("Test", "property", i)
    time.sleep(1)

logger.close()
