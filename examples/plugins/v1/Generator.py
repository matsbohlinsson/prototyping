import numbers
from typing import Callable

from plugins import Plugin
from examples.plugins.v1 import OutValue
from plugins.scheduler import on_scheduler_fast_loop


class Generator(Plugin, OutValue):

    def __init__(self, function: Callable[[float], None],  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.function = function

    @on_scheduler_fast_loop
    def main_loop(self, loop_index: int):
        self.out_value = self.function(loop_index)
