#!/usr/bin/env python3

from sense_hat import SenseHat
from pymongo import MongoClient
import time
import datetime

sense = SenseHat()
sense.clear()

client = MongoClient('localhost:27017')
db = client.g2x


def log(device, property, value):
    now = datetime.datetime.utcnow()
    print("[{0}] {1}:{2} = {3}".format(now, device, property, value))
    db.readings.insert({
        "timestamp": now,
        "device": device,
        "property": property,
        "value": value
    })


while True:
    temperature = sense.get_temperature_from_humidity()

    log("SenseHat", "temperature from humidity", temperature)

    time.sleep(0.5)
