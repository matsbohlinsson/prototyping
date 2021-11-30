import logging
from dataclasses import dataclass, field
from typing import Callable
from examples.plugins.v6 import OutSpeed, InSpeed, InWindowSize, InDeltaMax, Plugin


@dataclass
class Input:
    speed: float = 0
    delta_max: float = 4
    window_size: int = 3
    speed_history: [float] = field(default_factory=list)


@dataclass
class Output:
    speed_history:  [float] = field(default_factory=list)
    speed: float = 0


def average(in_vars: Input, out_vars: Output, _log: logging.Logger):
    out_vars.speed_history.append(in_vars.speed)
    while len(out_vars.speed_history) > in_vars.window_size:
        out_vars.speed_history.pop(0)
    speed_avg = sum(out_vars.speed_history) / len(out_vars.speed_history)
    out_vars.speed = speed_avg if abs(in_vars.speed - speed_avg) < in_vars.delta_max else in_vars.speed
    if out_vars.speed>2: _log.info(f"FAST:{out_vars.speed}")
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
    #s = Smoother2(_input=Input(window_size=10, delta_max=3), _output=Output(), _function=average)
    #s._input = Input(window_size=10, delta_max=3)
    #s._output = Output()
    #s._input.speed = 1
    in_data = Input()
    out_data = Output()
    log = logging.getLogger()
    for speed in range(0,20):
        in_data.window_size=5
        in_data.speed=speed
        average(in_data, out_data, log)
        print(out_data)
