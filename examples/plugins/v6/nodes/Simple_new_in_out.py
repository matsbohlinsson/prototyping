import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable
from examples.plugins.v6 import Plugin
from statistics import mean

from examples.plugins.v6.nodes.Smoother import Smoother


@dataclass
class Input:
    speed_in: float = 0


@dataclass
class Output:
    speed_out: float = 0


def transfer_function(in_: Input, out: Output, _log: logging.Logger):
    out.speed = in_.speed_in +1

class Smoother2(Plugin):
    in_: Input
    out: Output
    transfer_function: Callable

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(out_vars):
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
    s = Smoother2(in_=Input(), out=Output(), transfer_function=transfer_function, plugin_name='qq', parent=None)
    s.csv.run_test_from_file(Path('../csv_testdata/Smoother_simple.csv'))
