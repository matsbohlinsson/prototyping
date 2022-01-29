import csv
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

class EventBase:
    def __init__(self, *args, **kwargs):
        pass

class Event(EventBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callbacks = []
        self.last_value = None

    def notify(self, *args, **kwargs):
        self.last_value = args
        for callback in self.callbacks:
            callback(*args, **kwargs)

    def register(self, callback):
        self.callbacks.append(callback)
        return callback

    def __repr__(self):
        return str(self.last_value)

@dataclass
class Input:
    stop: Event = Event()
    value: float = 0
    delta_max: float = 4
    window_size: int = 3
    value_history: [float] = field(default_factory=list)

@dataclass
class Output:
    stop: Event = field(default_factory=Event)
    value: float = 0
    value_history:  [float] = field(default_factory=list)



if __name__ == "__main__":
    i = Input(Event())
    ii = Input(Event())
    i.stop=Event()
    ii.stop=Event()
    stop: Event = i.stop.register(lambda x,y,z: ii.stop.notify(x,y,z))
    ii.stop.register(lambda x,y,z: print("WW", x))
    i.stop.notify(a=7,b=8,c=9)
    
    print(i.stop)
    print(i.stop)





