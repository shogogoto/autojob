from contextlib import ExitStack

class Process:
    def __init__(self):
        self._processes = []
        self._stack = ExitStack()

    def num(self):
