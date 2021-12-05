import math
from typing import Callable
from examples.plugins.v6 import Plugin
from scratch2.scheduler import on_scheduler_fast_loop

import logging
from dataclasses import dataclass, field
from pathlib import Path
from examples.plugins import GeneralPlugin
from statistics import mean

PLUGIN_NAME= Path(__file__).name

@dataclass
class Input:
    start_value: float = 0
    function: callable = None


@dataclass
class Output:
    value: float = 0


def run(input: Input, output: Output, log: logging.Logger):
    output.value = input.function(input.start_value)

def run_post(input: Input, output: Output, log: logging.Logger):
    input.start_value = input.start_value+1


if __name__ == "__main__":
    in_data = Input()
    out_data = Output()
    s = GeneralPlugin(input=Input(function=lambda x: math.sin(x / 100)*100), output=Output(), run_function=run, run_post_function=run_post, plugin_name=PLUGIN_NAME, parent=None)
    s.csv.run_test_from_file(Path('../csv_testdata/GeneratorSin.csv'))



print(__name__, Path(__file__).name)




'''class Generator(Plugin, OutValue):

    def __init__(self, expression: Callable[[int], numbers.Number], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.function = expression
        self.counter = 0

    @on_scheduler_fast_loop
    def main_loop(self):
        self.out_value=self.function(self.counter)
        self.counter=self.counter+1
'''