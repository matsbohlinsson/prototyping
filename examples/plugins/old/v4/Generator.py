import numbers
from typing import Callable

from plugins import Plugin
from examples.plugins.v4 import OutValue
from plugins.scheduler import on_scheduler_fast_loop


class Generator(Plugin, OutValue):

    def __init__(self, function: Callable[[int], numbers.Number], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.function = function
        self.counter = 0

    @on_scheduler_fast_loop
    def main_loop(self):
        self.out_value=self.function(self.counter)
        self.counter=self.counter+1
