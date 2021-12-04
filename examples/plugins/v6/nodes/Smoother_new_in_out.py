import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable
from examples.plugins.v6 import OutSpeed, InSpeed, InWindowSize, InDeltaMax, Plugin
from statistics import mean

from examples.plugins.v6.nodes.Smoother import Smoother


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


def transfer_function(in_: Input, out: Output, _log: logging.Logger):
    in_.speed_history.append(in_.speed)
    out.speed_history = in_.speed_history[-in_.window_size:]
    speed_avg = mean(out.speed_history)
    out.speed = speed_avg if abs(in_.speed - speed_avg) < in_.delta_max else in_.speed
    # Log data
    if out.speed>2: _log.info(f"FAST:{out.speed}")
    _log.info(f"Last line")


class Smoother2(Plugin):
    in_: Input
    out: Output
    transfer_function: Callable

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def main_loop(out_vars):
        transfer_function(out_vars.in_, out_vars.out, out_vars.log)


if __name__ == "__main__":
    #s = Smoother2(_input=Input(window_size=10, delta_max=3), _output=Output(), _function=average)
    #s._input = Input(window_size=10, delta_max=3)
    #s._output = Output()
    #s._input.speed = 1
    in_data = Input()
    out_data = Output()
    log = logging.getLogger()
    '''
        for speed in range(0,20):
            in_data.window_size=5
            in_data.speed=speed
            transfer_function(in_data, out_data, log)
            print(out_data)
    '''
    s = Smoother2(in_=Input(window_size=10, delta_max=3), out=Output(), transfer_function=transfer_function, plugin_name='qq', parent=None)
    s.csv.run_test_from_file(Path('../csv_testdata/Smoother.csv'))
