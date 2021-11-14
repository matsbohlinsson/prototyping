import numbers
from typing import Callable
from examples.plugins.v6 import OutValue, Plugin
from scratch2.scheduler import on_scheduler_fast_loop


class Generator(Plugin, OutValue):

    def __init__(self, expression: Callable[[int], numbers.Number], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.function = expression
        self.counter = 0

    @on_scheduler_fast_loop
    def main_loop(self):
        self.out_value=self.function(self.counter)
        self.counter=self.counter+1
