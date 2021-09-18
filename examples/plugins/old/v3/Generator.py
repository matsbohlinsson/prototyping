import numbers
from typing import Callable

from plugins import Plugin
from examples.plugins.v3 import OutValue
from plugins.scheduler import on_scheduler_fast_loop


class Generator(Plugin, OutValue):

    def __init__(self, function: Callable[[int, int], numbers.Number], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.function = function

    @on_scheduler_fast_loop
    def main_loop(self, loop_index_local: int, loop_index_system: int):
        self.out_value=self.function(loop_index_local, loop_index_system)
