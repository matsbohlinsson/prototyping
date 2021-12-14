import csv
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable


class Event(object):
    def __init__(self):
        self.callbacks = []

    def notify(self, *args, **kwargs):
        for callback in self.callbacks:
            callback(*args, **kwargs)

    def register(self, callback):
        self.callbacks.append(callback)
        return callback

    def __get__(self, obj, objtype=None):
        print("WW", obj, objtype)

@dataclass
class Input:
    stop: Event
    value: float = 0
    delta_max: float = 4
    window_size: int = 3
    value_history: [float] = field(default_factory=list)

@dataclass
class Output:
    stop: float = Event()
    value: float = 0
    value_history:  [float] = field(default_factory=list)



if __name__ == "__main__":
    i = Input(Event())
    ii = Input(Event())
    i.stop=Event()
    ii.stop=Event()
    stop: Event = i.stop.register(lambda x: ii.stop.notify(x))
    ii.stop.register(lambda x: print("WW", x))
    i.stop.notify(7)
    print(i.stop)





