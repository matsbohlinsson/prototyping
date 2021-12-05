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
    speed: float = 0
    speed_history:  [float] = field(default_factory=list)


def transfer_function(in_: Input, out: Output, _log: logging.Logger):
    #in_.speed_history.append(in_.speed)
    out.speed_history = in_.speed_history.copy()
    out.speed_history = out.speed_history[-int(in_.window_size-1):]
    out.speed_history.append(in_.speed)
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

    def run(self):
        transfer_function(self.in_, self.out, self.log)

    def run_post(self):
        self.in_.speed_history = self.out.speed_history.copy()


if __name__ == "__main__":
    in_data = Input()
    out_data = Output()
    log = logging.getLogger()
    s = Smoother2(in_=Input(window_size=10, delta_max=3), out=Output(), transfer_function=transfer_function, plugin_name='qqq', parent=None)
    s.csv.run_test_from_file(Path('../csv_testdata/Smoother.csv'))
