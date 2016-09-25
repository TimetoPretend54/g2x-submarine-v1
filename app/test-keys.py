#!/usr/bin/env python3

from KeyDispatcher import KeyDispatcher


class Testing:
    def __init__(self):
        self.name = "test"

    def hello(self):
        print("hello from " + self.name, end="\x0a\x0d")
        return True

    def quit(self):
        return False


with KeyDispatcher() as dispatcher:
    handler = Testing()

    dispatcher.add("h", handler, "hello")
    dispatcher.add("q", handler, "quit")

    while dispatcher.process_key():
        pass
