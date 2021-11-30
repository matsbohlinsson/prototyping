import logging
from dataclasses import dataclass, field
from typing import Callable
from examples.plugins.v6 import OutSpeed, InSpeed, InWindowSize, InDeltaMax, Plugin


@dataclass
class Input:
    speed: float = 0
    delta_max: float = 2
    window_size: int = 3
    speed_history: [float] = field(default_factory=list)


@dataclass
class Output:
    speed_history:  [float] = field(default_factory=list)
    speed: float = 0


def average(self, _in: Input, _out: Output, _log: logging.Logger):
    _out.speed_history.append(_in.speed)
    while len(_out.speed_history) > _in.window_size:
        _out.speed_history.pop(0)
    speed_avg = sum(_out.speed_history) / len(_out.speed_history)
    _out.speed = speed_avg if abs(_in.speed - speed_avg) < _in.delta_max else _in.speed
    if _out.speed>2: _log.info(f"FAST:{_out.speed}")
    _log.info(f"Last line")



@dataclass
class Smoother2(Plugin):
    _input: Input
    _output: Output
    _function: Callable

    def __post_init__(self):
        super().__init__(self)

    def main_loop(self):
        average(self._input, self._output, self.log)


if __name__ == "__main__":
    s = Smoother2(_input=Input(window_size=10, delta_max=3), _output=Output(), _function=average)
    #s._input = Input(window_size=10, delta_max=3)
    #s._output = Output()
    #s._input.speed = 1
